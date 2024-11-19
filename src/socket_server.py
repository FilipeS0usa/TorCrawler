import ssl
import json
import socket
from bson import json_util
from pymongo import MongoClient
from functions.functions import get_mongo_session

def send_to_client(message):
    secure_client_socket.send(message)
    

def receive_from_client(info):
    response = secure_client_socket.recv(1024)
    print(f'{info}: {response.decode()}')
    return response.decode()

def send_receive(info, message):
    send_to_client(message)
    response = receive_from_client(info)
    return response

def receive_send(info, message):
    response = receive_from_server(info)
    send_to_server(message)
    return response


def search():
    RESULTS_PER_PAGE = 1
    page = 2
    message = "Ok"
    info = "Amount of data to be received"
    # Receive the ammount of data that will be received
    data = send_receive(info, message.encode())

    data_len = int(data)
    print(f'DATA LEN => {data_len}')
    
    searching_term = ""
    # Send response and receive query
    for i in range(data_len):
        message = "Ok"
        info = "Received data"
        data = send_receive(info, message.encode())
        searching_term += data
    
    print(f'Searching term => {searching_term}')
    
    pattern = '(\w+[ ]?)+'
    mongo_db_result = collection.aggregate([
                {
                    '$match': {
                        'content': {'$regex': searching_term, '$options': 'i'}
                    }
                },
                {
                    '$addFields': {
                        'word_count': {
                            '$size': {
                                '$split': ['$content', searching_term]
                            }
                        }
                    }
                },
                {
                    '$sort': {'word_count': -1}
                },
                {
                    '$skip': (page - 1) * RESULTS_PER_PAGE
                },
                {
                    '$limit': RESULTS_PER_PAGE
                },
                {
                    '$project':{
                        '_id': 0,
                        'description': 0,
                        'content': 0,
                        }
                }
            ])
    print('Finished searching')

    # TODO: make the query for the mongo db!
    # mongo_db_result = "This message is a result from mongoDB"
    print(type(mongo_db_result))
    mongo_db_result = list(mongo_db_result)
    # from dictionary to string
    search_result = json.dumps(mongo_db_result, default=json_util.default)

    # encode the result from query
    search_result = search_result.encode()
    
    # will store result of search in pieces of 1024bytes
    result_array = []
    for i in range(0, len(search_result), 1024):
        result_array.append(search_result[i:i+1024])
        
    # send the ammount of information that will be sent
    message = str(len(result_array)).encode()
    info = "Client response"
    
    send_receive(info, message)
    
    # send information
    for i in range(len(result_array)):
        # send pieces of the result of query
        info = "Client response"
        message = result_array[i]
        send_receive(info, message)


collection = get_mongo_session()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 12345)

server_socket.bind(server_address)

server_socket.listen(1)

print('Server is listening for connections...')


ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')

while True:
    client_socket, client_address = server_socket.accept()
    print(f'Client{client_address} connected.')

    secure_client_socket = ssl_context.wrap_socket(client_socket, server_side=True)
    data = secure_client_socket.recv(1024)
    

    if data:
        print(f'Received data: {data.decode()}')

        match data.decode():
            case "1":
                search()
            case "0":
                message = "Ok"
                secure_client_socket.send(message.encode())
                secure_client_socket.close()
