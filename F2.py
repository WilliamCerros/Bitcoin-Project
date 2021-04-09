from socket import *
from sys import getsizeof
serverPort = 20000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('The server is ready to receive')
turn = 0
while 0 != 1:


    message, clientAddress = serverSocket.recvfrom(2048)
    print(getsizeof(message))
    print(message)
    if getsizeof(message) <= 58:
        print("The message received is a Tx.")
        turn+=1
        f = open("Temp_T.txt","a+")
        message = message.decode("utf-8")
        f.write(message)
    else:
        print("The message received is a block.")
        f = open("Blockchain.txt", "a+")
        message = message.decode("utf-8")
        f.write(message)

