# Names: Alonso Vega, Daniel Letterman, Gabe Williams, & Nicholas Fotinakes
# Team: 10
# Title: PA1 - TCPServer
# Date: 2022-05-03
# Description: This program acts as the TCP Server and waits for the client to send a string
# and returns it uppercase

from socket import *

# Create port and TCP type socket for server
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)

# Associate port with this socket, and listen for TCP connection requests
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
while True:
    
    # When request from client, new socket is made for this client and message receieved
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    
    # Modify the message and send back to client
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()

