import socket
from _thread import *


connection_status = True


def read_message(connection):
    while True:
        try:
            message = connection.recv(1024).decode()
            print(message)
        except:
            print("Connection closed")
            break


HOST = '127.0.0.1'
PORT = 7926

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

start_new_thread(read_message, (client,))

while True:
    message = input()
    if (message == 'quit'):
        print("client connection closed")
        client.close()
        break
    client.send(message.encode())
