# Names: Alonso Vega, Daniel Letterman, Gabe Williams, & Nicholas Fotinakes
# Team: 10
# Title: PA1 - TCPServer
# Date: 2022-05-03
# Description: This program acts as the TCP Server and waits for the client to send a string
# and returns it uppercase

from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()

