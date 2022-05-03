# Names: Alonso Vega, Daniel Letterman, Gabe Williams, & Nicholas Fotinakes
# Team: 10
# Title: PA1 - UDPServer
# Date: 2022-05-03
# Description: This program acts as the UDP server which waits for a message from the client
# and returns the string as an uppercase

from socket import *

# Create port and UDP type socket for server
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Bind the port and address to this socket
serverSocket.bind(('', serverPort))
print("The server is ready to receive")

# Wait in while loop for packet to arrive
while True:
    
    # Receive message from client and client information
    message, clientAddress = serverSocket.recvfrom(2048)
    
    # Modify message to uppercase and send back to client
    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)

    