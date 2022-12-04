# Team: 10
# Names: Alonso Vega, Daniel Letterman, Gabe Williams, & Nicholas Fotinakes
# Date: 2022-05-31
# Assignment Title: PA #3 - TCP Client
# Description: This program acts as the TCP Client that establishes a connection with the server, sends
# a message, and then closes after receiving the message order from the server

from socket import *

# Create server and port, DNS will get local host IP
serverName = 'localhost'
serverPort = 12000

# Create socket with IPv4 and SOCK_STREAM for TCP socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# Establish TCP connection and perform 'handshake'
clientSocket.connect((serverName, serverPort))
# Client waits to receive acceptance message from Server
serverMessage = clientSocket.recv(1024)
# Print acceptance message
print('From server: ' + serverMessage.decode())
flag = True
while flag:
    # Send message to server
    sentence = input('Enter message to send to server: ')
    clientSocket.send(sentence.encode())

    # Receive closing message from server, print and then close socket
    serverResponse = clientSocket.recv(1024)
    print('From server: ' + serverResponse.decode())
    flag = False

clientSocket.close()
