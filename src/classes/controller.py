import re
import requests


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def first_url(self, url):
        """
        Check if it's the first url in the database

        :param url:
        :return Boolean:
        """
        if self.model.get_first_domain() is None:
            domain_url = self.model.get_domain_url(url)
            link_url = self.model.get_link_url(url)
            self.model.add_url(domain_url, link_url)
            return True

    def grab_oldest_domain(self):
        """
        Choose the url to scan
        :param:
        :return link:
        """
        domain = self.model.get_oldest_domain()
        links = domain.link

        counter = 0
        for link in links:
            counter += 1

        if counter > 10:
            for i in range(10):
                link = self.model.get_oldest_link_from_domain(domain)
                self.scan_link(link)
        else:
            for i in range(counter):
                link = self.model.get_oldest_link_from_domain(domain)
                self.scan_link(link)

        self.model.update_oldest_domain(domain)

    def scan_link(self, link):
        """
        Scan the url
        :param:
        :return String content_text:
        """
        try:
            link = link
            domain = link.domain
            url = domain.domain + link.link

            self.view.show_message(
                f"\nScanning: {url}"
                f"\nlink_id: {link.id}"
                f"\nDomain_id: {domain.id}\n")

            if link.disabled:
                raise Exception(f"This url is disabled: {url}")

            header_info = self.model.get_header_info(url)

            if self.model.check_header_content_length(header_info, link, domain):
                raise Exception("Content to large!\n")

            content = self.model.get_content(url)

            if self.model.check_status_code(content, link):
                raise Exception('Failed connection!\n')

            self.view.show_message("It connected :)")

            content_text = self.model.get_content_text(content)

            content_to_hash = self.model.html_to_text(content_text)

            hashed_content = self.model.create_hash(content_to_hash)

            if not self.model.check_hash(hashed_content, link):
                self.model.add_mongo_content(url, content_text)
            else:
                self.view.show_message("Hash already exists.")

            self.model.update_link(hashed_content, link)

            self.add_new_links(content_text)

        except requests.exceptions.ConnectionError as e:
            self.model.disable_link(link)
            self.view.show_error(e)

        except Exception as e:
            self.view.show_error(e)

    def add_new_links(self, content_text):
        """
        Adds new links to the db that are in the html
        :param:
        :return int:
        """
        content_text = content_text

        urls_list = self.model.get_new_urls(content_text)
        if len(urls_list) == 0:
            self.view.show_message("No urls added to db.\n")
            return 0

        counter_domain = 0
        counter_link = 0
        counter_file = 0

        for url in urls_list:
            # date_time = datetime.today()
            domain_url = self.model.get_domain_url(url)
            link_url = self.model.get_link_url(url)
            domain = self.model.get_specific_domain(domain_url)

            if domain is None:
                self.model.add_url(domain_url, link_url)
                counter_domain += 1
                counter_link += 1
                continue

            links = domain.link
            links_list = []

            for link in links:
                links_list.append(link.link)

            if link_url in links_list:
                continue

            pattern = '\/([A-Za-z0-9-_ ]+)?(.html?|.php|.xml|.json)?\/?$'

            if not re.search(pattern, link_url):
                self.model.add_new_file(link_url, domain)
                counter_file += 1
                continue

            self.model.add_new_link(link_url, domain)
            counter_link += 1

        self.view.show_message(f'{counter_domain} domains added\n'
                               f'{counter_link} links added\n'
                               f'{counter_file} files added\n')
        return 0
