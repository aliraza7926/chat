import socket
from _thread import *
import time


def print_user():
    while True:
        print(user_dict)
        time.sleep(5)


def handel_threaded_client(connection):
    flag = True
    user_name = ''
    if flag:
        user_name = connection.recv(1024).decode().strip()
        user_dict[user_name] = connection
        print("{} joined the chat".format(user_name))
        flag = False

    while True:
        try:
            data = connection.recv(1024)
            if data:
                data = data.decode().strip()
                if data == 'quit':
                    print("{} left the chat".format(user_name))
                    del user_dict[user_name]
                    connection.close()

                else:
                    data = user_name+': '+data
                    for user in user_dict:
                        if user != user_name:
                            user_socket = user_dict[user]
                            user_socket.send(data.encode())
        except Exception as reason:
            print("client connection closed: {}".format(reason))
            break


HOST = '127.0.0.1'
PORT = 7926

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
user_dict = {}
#start_new_thread(print_user, ())

print("start listening on {}:{}".format(HOST, PORT))
while True:
    print("waiting for new connection...")
    client_socket, client_address = server_socket.accept()
    print("Accepted connection from {}:{}".format(
        client_address[0], client_address[1]))
    client_socket.send(b'Welcome to the server!')
    client_socket.send(b'Please enter your name: ')
    start_new_thread(handel_threaded_client, (client_socket,))
