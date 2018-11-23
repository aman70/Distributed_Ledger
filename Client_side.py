import socket
import sqlite3
import pickle

def  Main():
    host = "localhost"
    port = 5000


    host_server = "localhost"
    port_server = 5001

    s =  socket.socket()
    s.connect((host,port))

    message = input("enter the word to check here \n ->")
    code = 0
    data =  {}
    data['message'] = message
    data['code'] = code
    while message != 'q':
        message_to_send = pickle.dumps(data)
        s.send(message_to_send)
        data_rec = s.recv(1024).decode('utf-8')
        print("Received from server: " + data_rec)
        message = input("enter the word to check here \n ->")

        data['message'] = message
        data['code'] = code

    s.close()


if __name__ == "__main__":
    Main()
