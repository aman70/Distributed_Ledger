import socket
from threading import Thread
import pickle

class client:


    def __init__(self,port,data):
        self.port = port
        self.data = data
        self.Main()

    def Main(self):
        host_client = "localhost"
        s2 = socket.socket()  # now it is time to act like a client
        s2.connect((host_client, self.port))  # connect to the other server/s
        message_to_send_2 = pickle.dumps(self.data)
        s2.send(message_to_send_2)
        data_rec = s2.recv(1024).decode('utf-8')
        print("Received from server: " + data_rec)

