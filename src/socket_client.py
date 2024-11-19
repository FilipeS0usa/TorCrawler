import socket
import ssl
import json

def send_to_server(message):
    secure_client_socket.send(message)

def receive_from_server():
    response = secure_client_socket.recv(1024)
    print(f'Response from server: {response.decode()}')
    return response.decode()


def send_receive(message):
    send_to_server(message)
    response = receive_from_server()
    return response

def receive_send(message):
    response = receive_from_server()
    send_to_server(message)
    return response

def search():
    # number of results
    #number_of_results = input('Choose the amount of results: ')
    
    # searching term
    message = input('Choose your searching term: ')
    message = message.encode()
    
    message_send = []
    for i in range(0, len(message), 1024):
        message_send.append(message[i:i+1024])
    
    len_message = str(len(message_send))
    
    # send the amount of data that will be sent
    send_to_server(len_message.encode())

    # receive response from server and start sending query
    for i in range(len(message_send)):
        receive_send(message_send[i])
    
    # get the num_loop
    num_loop = receive_from_server()
    num_loop = int(num_loop)

    # send ok
    message = "Ok"
    send_to_server(message.encode())
    
    answer = ""
    for i in range(num_loop):
       
        # Receive information
        message = "Data Received"
        response = receive_send(message.encode())
        answer += response
    
    answer = json.loads(answer)   
    
    print('\n=================Results===================\n')
    print('title: ', answer[0]['title'])
    print('url: ', answer[0]['url'])
    #print('description: ', answer[0]['description'])



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 12345)

ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

secure_client_socket = ssl_context.wrap_socket(client_socket, server_hostname=server_address[0])
secure_client_socket.connect(server_address)
while True:
    print("Menu:"
          "\n1) Search"
          "\n0) Exit"
          )
    message = input("Chose your option: ")
    secure_client_socket.send(message.encode())

    response = secure_client_socket.recv(1024)
    print(f'Response from server: {response.decode()}')

    if response.decode() == 'Ok':
        match message:
            case "1":
                search()
            case "0":
                secure_client_socket.close()
                exit()
