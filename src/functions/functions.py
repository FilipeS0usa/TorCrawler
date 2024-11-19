import requests
import hashlib
import subprocess
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Function that creates the tor session
def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http': 'socks5h://127.0.0.1:9050',
                       'https': 'socks5h://127.0.0.1:9050'}
    return session

# Function that reconnects tor
def reload_tor():
    print("Trying to connect!")
    subprocess.run(["service", "tor", "reload"])
    

# Function that creates a Mongo Database session
def get_mongo_session():
    client = MongoClient("mongodb://localhost:27017")
    mongodb = client.mongo_e_corp
    return mongodb.urlContent

# Function that creates a SQL session
def get_sql_session():
    username = "ecorp"
    password = "cisco123"
    server = "localhost"
    database = "db_e_corp"
    engine = create_engine("mysql+pymysql://{}:{}@{}/{}".format(username, password, server, database), echo=True)
    DBsession = sessionmaker(bind=engine)
    db = DBsession()
    return db

# Function that creates a hash
def sha256_hash(data):
    # Create a new SHA256 hash object
    sha256 = hashlib.sha256()

    # Convert data to encoded utf-8 if it's in string
    if isinstance(data, str):
        data = data.encode('utf-8')
    # Update the hash object with the data
    sha256.update(data)

    # Generate the hexadecimal representation of the hash
    hash_value = sha256.hexdigest()

    return hash_value


# def check_size(size_content, url):
#     file = re.findall(r"\/\w+.\w+$", url)
#     file_name = file[0]
#     home = os.environ['HOME']
#     directory = '/downloads_crawler'
#     path = home + directory + file_name
#     if 10000000 < size_content < 1000000000:
#         subprocess.Popen(["proxychains4","curl","-o",path,url])
#         return True
#     else:
        
#         return True

