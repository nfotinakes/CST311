# Names: Alonso Vega, Daniel Letterman, Gabe Williams, & Nicholas Fotinakes
# Team: 10
# Date: 2022-05-17
# Title: PA#2 - UDP Pinger Server
# Description: This program acts as the server and to receive pings from the client and randomize
# a number of lost packets

# We will need the following module to generate
# randomized lost packets
import random
from socket import *

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('', 12000))
ping_num = 0
success_pings = 0
print("Waiting for Client...")
while True:
    # Count the pings received
    ping_num += 1
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)
    # Receive the client packet along with the
    # address it is coming from
    message, address = serverSocket.recvfrom(1024)
    modified_message = message.decode().upper()
    # If rand is less is than 4, and this not the
    # first "ping" of a group of 10, consider the
    # packet lost and do not respond
    if rand < 4 and ping_num % 10 != 1:
        print("Packet was lost\n")
        continue
    # Otherwise, the server responds
    success_pings += 1
    print("PING " + str(success_pings) + " Received")
    print("Mesg rcvd: " + message.decode())
    print("Mesg sent: " + modified_message)
    print()
    serverSocket.sendto(modified_message.encode(), address)
