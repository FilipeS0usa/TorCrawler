import re
import hashlib
import random
import subprocess
from bs4 import BeautifulSoup
from classes.classes import *
from datetime import datetime

class Model:
    def __init__(self, db_sql, db_mongo, tor_session):
        self.db_sql = db_sql
        self.db_mongo = db_mongo
        self.tor_session = tor_session

    # def get_oldest_link(self):
    #     """
    #     Return the oldest scanned link
    #     :param:
    #     :return object link:
    #     """
    #     return self.db_sql.query(Link).order_by(Link.date_last_scan.asc()).first()
    
    def get_oldest_domain(self):
        """
        Return the oldest scanned domain
        :param:
        :return object domain:
        """
        return self.db_sql.query(Domain).order_by(Domain.date_last_scan.asc()).first()
    
    def update_oldest_domain(self, domain):
        """
        Updates the date_last_scan of domain
        :param domain:
        :return:
        """
        domain.update_last_scan()
        self.db_sql.commit()
    
    def get_oldest_link_from_domain(self, domain):
        """
        return the oldest link from a specific domain
        :return object link
        """
        return self.db_sql.query(Link).filter_by(idDomain=domain.id).order_by(Link.date_last_scan.asc()).first()

    def get_specific_domain(self, domain_url):
        """
        Gets a specific domain
        :param domain_url:
        :return domain object:
        """
        return self.db_sql.query(Domain).filter_by(domain=domain_url).first()

    def get_first_domain(self):
        """
        Gets the first domain
        :param:
        :return object:
        """
        return self.db_sql.query(Domain.id).order_by(Domain.id.asc()).first()

    # def get_url(self):
    #     """
    #     Returns the oldest scanned url
    #     :return url:
    #     """
    #     link = self.db_sql.query(Link).order_by(Link.date_last_scan.asc()).first()
    #     domain = link.domain
    #     return domain.domain + link.link

    def get_domain_url(self, url):
        """
        Separates the domain of the link and returns the domain
        :param url:
        :return domain_url:
        """
        domain_url = re.findall(r"https?\:\/\/\w+\.onion", url)
        return domain_url[0]

    def get_link_url(self, url):
        """
        Separates the link of the domain and returns the link
        :param url:
        :return link_url:
        """
        link_url = re.findall(r"(?:https?\:\/\/\w+\.onion)(\/[\w\.\-\/]*)(?=\")?", url)
        return link_url[0]

    def add_url(self, domain_url, link_url):
        """
        Add  url to the database
        If we don't add it the rest doesn't work
        :param domain_url:
        :param link_url:
        :return:
        """
        domain = Domain(domain=domain_url)  # create object domain
        link = Link()  # create object link
        link.new_link(link_url)  # update link
        domain.link.append(link)  # domain as this link
        self.db_sql.add(domain)
        self.db_sql.commit()

    def create_large_link(self, link, header_info):
        """
        Creates a large link object
        :param link:
        :param header_info:
        :return object:
        """
        large_link = LargeLink(
            link=link.link,
            header=header_info
        )
        return large_link

    def add_large_link(self, link, domain, header_info):
        """
        Adds large link to database
        :param link:
        :param domain:
        :param header_info:
        :return:
        """
        date_time = datetime.today()
        large_link = self.create_large_link(link, header_info)
        domain.large_link.append(large_link)
        link.large = 1
        link.date_last_scan = date_time
        self.db_sql.add(domain)
        self.db_sql.commit()

    def get_header_info(self, url):
        """
        Gets header info from the url using tor session
        :param url:
        :return:
        """
        header = self.tor_session.head(url)
        header_info = header.headers
        return header_info

    def check_header_content_length(self, header_info, link, domain):
        """
        Check if the header has content-Length and returns it
        :param header_info:
        :param link:
        :param domain:
        :return Boolean:
        """
        location_file = None
        if 'Location' in header_info:
            pattern = ".exe$"
            location = header_info['Location']
            location_file = re.search(pattern, location)
        if 'Content-Length' in header_info:
            content_length = int(header_info['Content-Length'])
        else:
            content_length = 1

        if content_length > 10000000 or link.large or not location_file == None:
            self.add_large_link(link, domain, header_info)
            return True

    def get_content(self, url):
        """
        Gets the content of the url from the tor session
        :param url:
        :return content:
        """
        content = self.tor_session.get(url)
        return content

    def get_content_text(self, content):
        """
        Get html from content
        :param content:
        :return:
        """
        content_text = content.text
        return content_text
    
    
    def disable_link(self, link):
        """
        Disables the link
        :param link:        
        :return:
        """
        link.disable_link()
        self.db_sql.commit()
    
    def reload_tor(self):
        """
        Reloads tor service to receive a new IPs
        :param:
        :return:
        """
        subprocess.run(["service", "tor", "reload"])

    def check_status_code(self, content, link):
        """
        Checks if the status code received is between 200 and 299
        :param content:
        :param link:
        :return Boolean:
        """
        while True:
            status_code = content.status_code
            if status_code < 200 or status_code > 299:
                self.reload_tor()
                tries = link.tries
                if tries == 10:
                    link.disable_link()
                    self.db_sql.commit()
                    return True
                else:
                    link.add_tries()
                    self.db_sql.commit()
            else:
                return False

    def add_mongo_content(self, url, content_text):
        """
        Insert url, description and content into MongoDB
        :param url:
        :param content:
        :return:
        """
        soup = BeautifulSoup(content_text, features="lxml")
        metas = soup.find_all('meta')
        title = str(soup.find('title'))
        #pattern = '^[A-Za-z0-9= "-]+>'
        title = title.strip('<title>/>')
        #title = re.sub(pattern, "", title)
        description = [ meta.attrs['content'] for meta in metas 
                if 'name' in meta.attrs and meta.attrs['name'] == 'description' ]
        
        if len(description) == 0 or len(description) > 1:
            description_final = "There's no description available!"
        else:
            description_final = description[0]

        url_content = {
            "url": url,
            "title": title,
            "description": description_final,
            "content": content_text
        }
        self.db_mongo.insert_one(url_content)

    def create_hash(self, content):
        """
        Creates the hash of the content
        :param content:
        :return:
        """
        sha256 = hashlib.sha256()

        if isinstance(content, str):
            content = content.encode('utf-8')

        sha256.update(content)

        hashed_content = sha256.hexdigest()

        return hashed_content
    
    def check_hash(self, hashed_content, link):
        """
        Checks if the hash already exists
        :param hashed_content:
        :return Boolean:
        """

        if self.db_sql.query(Hash).filter_by(hash = hashed_content).first() is not None:
            link.update_last_scan()
            self.db_sql.commit()
            return True
        else:
            return False
        
    def html_to_text(self, content_text):
        """
        Converts the html to text
        :param content_text:
        :return content_to_hash:
        """
        content_to_hash = BeautifulSoup(content_text, "lxml")
        content_to_hash = content_to_hash.get_text()
        return content_to_hash

    def update_link(self, hashed_content, link):
        """
        Final update the link with the hash
        :param hashed_content:
        :param link:
        :return:
        """
        date_time = datetime.today()
        link.date_last_scan = date_time
        hash = Hash(hash=hashed_content)
        link_hash = LinkHash(date=date_time)
        hash.link_hash.append(link_hash)
        link.link_hash.append(link_hash)
        self.db_sql.add(link)
        self.db_sql.commit()

    def get_new_urls(self, content_text):
        """
        Make a list with the new urls found in the content
        :param content_text:
        :return list of new_urls:
        """
        new_urls = re.findall(
            r'https?\:\/\/\w+\.onion\/[\w\.\-\/]*(?=\")?',
            content_text
        )
        return new_urls

    def create_name(self, date_time):
        """
        Creates a name for a file
        :param date_time:
        :return string name:
        """
        date_time = str(date_time)
        date_time = re.sub("[-:. ]", "", date_time)
        random_number = str(random.randint(0, 1000000))
        name = date_time + random_number
        return name

    def get_file_name(self, link_url, type_of_file):
        """
        get the name of the file present in whe url link
        :param link_url:
        :param type_of_file:
        :return:
        """
        pattern = f'[A-Za-z0-9-_ ]+(?={type_of_file})'
        name = re.search(pattern, link_url)
        if name[0]:
            name = "Name is not available"
        else:
            name = name[0]
        return name

    def get_type_of_file(self, link_url):
        """
        get the type of file present in the url link
        :param link_url:
        :return:
        """
        pattern = '\.\w+\/?$'
        type_of_file = re.search(pattern, link_url)
        return type_of_file[0]

    def add_new_file(self, link_url, domain):
        """
        Creates a new file in database
        :param link_url:
        :param domain:
        :return:
        """
        date_time = datetime.today()
        name = self.create_name(date_time)
        type_of_file = self.get_type_of_file(link_url)
        original_name = self.get_file_name(link_url, type_of_file)
        file = File(
            name=name,  # name will be generated (can be a date with a random number)
            original_name=original_name,  # original name will be the name of the file
            type_of_file=type_of_file,  # Will be the end of the file
            date_of_discovery=date_time,
            link=link_url  # will be the link that it came from
        )
        domain.file.append(file)
        self.db_sql.add(domain)
        self.db_sql.commit()

    def add_new_link(self, link_url, domain):
        """
        Adds a new link to database
        :param link_url:
        :param domain:
        :return:
        """
        link = Link()
        link.new_link(link_url)
        domain.link.append(link)
        self.db_sql.add(domain)
        self.db_sql.commit()

