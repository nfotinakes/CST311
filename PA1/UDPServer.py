# Names: Alonso Vega, Daniel Letterman, Gabe Williams, & Nicholas Fotinakes
# Team: 10
# Title: PA1 - UDPServer
# Date: 2022-05-03
# Description: This program acts as the UDP server which waits for a message from the client
# and returns the string as an uppercase

from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("The server is ready to receive")
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)

    