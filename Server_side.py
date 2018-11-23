import socket
import sqlite3
from threading import Thread
import pickle
from server_class import server
from client_class import client

def Main():



    palindrome_dict = {}
    palindrome_list = []
    host_server = "localhost"
    port_server = 5000
    print("Binding .....")
    s = socket.socket() #create a scoket object
    s.bind((host_server,port_server))
    s.listen(1) #listen for one connection at a time
    print("listening .....")

    while True:
        c, addr = s.accept()  # we have accepted a connection
        print("Connection from: " + str(addr))
        data = c.recv(1024)
        data_1 = pickle.loads(data)
        if data_1['code'] == 0:
            Thread(target = write_client, args = (c, addr,data_1,palindrome_dict,palindrome_list)).start()


    s.close()



def write_client(clientsocket,addr,data,palindrome_dict,palindrome_list):
    host_client = "localhost"

    user_input = input("How many peers would you want for verification \n ->")
    port_client_list = []
    for i in range(0,int(user_input)):


        port_client_list.append(5000 + i + 1)

    global_receive = [None]*len(port_client_list)



    while True:

        #do some checks and if msg == someWeirdSignal: break:
        if not data:  # if there is no data
            break;
        # print("data['message")
        print("From Connected user: " + data['message'])
        print("Checking if it is a Palindrome")
        yn = isPalindrome(data['message'])

        if yn:

            for i,v in enumerate(port_client_list):
                Thread(target=server, args=(v,)).start()
                Thread(target=client, args=(v,data)).start()

            # s2 = socket.socket()  # now it is time to act like a client
            # s2.connect((host_client, port_client)) #connect to the other server/s
            # message_to_send_2 = pickle.dumps(data)
            # s2.send(message_to_send_2)
            # data_rec = s2.recv(1024).decode('utf-8')
            # print("Received from server: " + data_rec)

            data_return = "A pallindrome was found"

            #now we ned to add the verification step
            if data['message'] not in palindrome_dict.keys():
                palindrome_dict[data['message']] = 1
                palindrome_list.append(data['message'])
            else:
                palindrome_dict[data['message']] += 1
        else:
            data_return = "Sorry not a Pallindrome"
        clientsocket.send(data_return.encode('utf-8'))
        data = clientsocket.recv(1024)
        data = pickle.loads(data)


    clientsocket.close()

def reverse(s):
    return s[::-1]

def isPalindrome(s):
    # Calling reverse function
    rev = reverse(s)

    # Checking if both string are equal or not
    if (s == rev):
        return True
    return False


if __name__ == "__main__":
    Main()
