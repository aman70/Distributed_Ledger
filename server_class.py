import socket
from threading import Thread
import pickle

class server:


    def __init__(self,port):
        self.port = port
        self.Main()

    def Main(self):
        palindrome_dict = {}
        palindrome_list = []
        host_server = "localhost"
        print("Binding .....")
        s = socket.socket()  # create a scoket object
        s.bind((host_server, self.port))
        s.listen(1)  # listen for one connection at a time
        print("listening .....")
        while True:
            c, addr = s.accept()  # we have accepted a connection
            print("Connection from: " + str(addr))
            data = c.recv(1024)
            data_1 = pickle.loads(data)
            if data_1['code'] == 0:
                Thread(target=self.write_client, args=(c, addr, data_1, palindrome_dict, palindrome_list, self.port)).start()

        s.close()

    def write_client(self,clientsocket, addr, data, palindrome_dict, palindrome_list, port):

        # if flag == 1:
        #     conn, dbc = create_database()

        while True:

            # do some checks and if msg == someWeirdSignal: break:
            if not data:  # if there is no data
                break;
            # print("data['message")
            print("From Connected user: " + data['message'])
            print("Checking if it is a Palindrome")
            yn = self.isPalindrome(data['message'])

            if yn:
                data_return = "Pallindrome was verified from server {}".format(port - 5000 + 1)
                # if flag == 1:
                #     dbc.execute("REPLACE INTO palindrome_ledger VALUES (?)", (data,))
                # else:  #if the flag is zero we will create a global dictionary and write to it
                if data['message'] not in palindrome_dict.keys():
                    palindrome_dict[data['message']] = 1
                    palindrome_list.append(data['message'])
                else:
                    palindrome_dict[data['message']] += 1
            else:
                data_return = "Upon verification it is not a pallindrome"
            clientsocket.send(data_return.encode('utf-8'))
            data = clientsocket.recv(1024)
            if data:
                data = pickle.loads(data)

        clientsocket.close()

    def reverse(self,s):
        return s[::-1]

    def isPalindrome(self,s):
        # Calling reverse function
        rev = self.reverse(s)

        # Checking if both string are equal or not
        if (s == rev):
            return True
        return False

if __name__ == "__main__":
    server(5000)