#!/usr/bin/python3
import logging
from classes.classes import *
from classes.model import *
from classes.view import *
from classes.controller import *
from functions.functions import *

# Disable the logging of the SQLAlchemy
logging.disable(logging.CRITICAL)

if __name__ == '__main__':
    
    # This will be the first url of the database
    url_1 = "http://torlinksge6enmcyyuxjpjkoouw4oorgdgeo7ftnq3zodj7g2zxi3kyd.onion/"
    
    # Create the Mongo session
    db_mongo = get_mongo_session()

    # create the SQL session
    db_sql = get_sql_session()

    # create the tor session
    tor_session = get_tor_session()
    
    # create model
    model = Model(db_sql, db_mongo, tor_session)
    
    # create a view
    view = View()
    
    # create a controller
    controller = Controller(model, view)
    
    # Check if it is the first url in the database
    controller.first_url(url_1)

    # this is the scrapper
    while True:
    
        controller.grab_oldest_domain()
        
        


# TODO: Create function that serves as a debuger, if we receive an argument (like -v) it 
#       activates debugging mode (it will show prints so we know where is the bug)

# TODO: If the file is to big, zip it and store it in the local machine for later inspection

# TODO: Instead of associating the file to a domain, associate it with the link that discovered it

# TODO: Resolve bug title in search, some titles are ginormous!!!
