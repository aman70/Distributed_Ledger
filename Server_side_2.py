import socket
import sqlite3
from threading import Thread
import pickle

def Main():



    palindrome_dict = {}
    palindrome_list = []
    host = "localhost"
    port = 5001
    print("Binding .....")
    s = socket.socket() #create a scoket object
    s.bind((host,port))
    s.listen(1) #listen for one connection at a time
    print("listening .....")

    while True:
        c, addr = s.accept()  # we have accepted a connection
        print("Connection from: " + str(addr))
        data = c.recv(1024)
        data_1 = pickle.loads(data)
        if data_1['code'] == 0:
            Thread(target = write_client, args = (c, addr,data_1,palindrome_dict,palindrome_list,port)).start()


    s.close()



def write_client(clientsocket,addr,data,palindrome_dict,palindrome_list,port):


    # if flag == 1:
    #     conn, dbc = create_database()

    while True:

        #do some checks and if msg == someWeirdSignal: break:
        if not data:  # if there is no data
            break;
        # print("data['message")
        print("From Connected user: " + data['message'])
        print("Checking if it is a Palindrome")
        yn = isPalindrome(data['message'])

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
            data_return = "Upon verification not a pallindrome"
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
