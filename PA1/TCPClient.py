# Names: Alonso Vega, Daniel Letterman, Gabe Williams, & Nicholas Fotinakes
# Team: 10
# Title: PA1 - TCPClient
# Date: 2022-05-03
# Description: This program acts as the TCP client to send a string to the server which
# will return the string uppercase

from socket import *

# Create server and port, DNS will get local host IP
serverName = 'localhost'
serverPort = 12000

# Create socket with IPv4 and SOCK_STREAM for TCP socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# Establish TCP connection and perform 'handshake'
clientSocket.connect((serverName, serverPort))

# Send user message through TCP connection
sentence = input('Input lowercase sentence:')
clientSocket.send(sentence.encode())

# Receive modifed message from server, print and close
modifiedSentence = clientSocket.recv(1024)
print('From Server: ', modifiedSentence.decode())
clientSocket.close()

