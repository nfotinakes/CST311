# Names: Alonso Vega, Daniel Letterman, Gabe Williams, & Nicholas Fotinakes
# Team: 10
# Title: PA1 - UDPClient
# Date: 2022-05-03
# Description: This program acts as the UDP client to send a string to the server which
# will return the string uppercase

from socket import *

# Set server and port. DNS will will look up local host IP
serverName = 'localhost'
serverPort = 12000

# Create client socket, AF_INET for IPv4 and SOCK_DGRAM for UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Get message, encode to byte and attach destination host address and send to socket
message = input('Input lowercase sentence:')
clientSocket.sendto(message.encode(), (serverName, serverPort))

# Receive modified message from server with buffer 2048
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

# Decode and print capitalized message, then close socket
print(modifiedMessage.decode())
clientSocket.close()

