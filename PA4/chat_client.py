#!/usr/bin/env python3

# Names: Alonso Vega, Daniel Letterman, Gabe Williams, & Nicholas Fotinakes
# Team: 10
# Date: 6-18-2022
# Title: PA4 - chat_client.py
# Description: This program acts as the TCP Client that establishes a connection with the TCP Server on host h4 to chat with
# another client via the server. The client uses an additional thread to handle message sending and the main thread
# to listen for messages. When the termination keyword 'bye' is sent/received, connection is closed

import time
from socket import *
import threading


# Create server and port, DNS will get local host IP
serverName = '10.0.2.2'
serverPort = 12000

# Create socket with IPv4 and SOCK_STREAM for TCP socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# Establish TCP connection and perform 'handshake'
clientSocket.connect((serverName, serverPort))
# Client waits to receive acceptance message from Server
print('Waiting for connection...')
serverMessage = clientSocket.recv(1024)
print(serverMessage.decode())


# Function to handle thread for sending chats
def send_message():
    send_flag = True
    # Wait in loop to send user input unless send bye
    # or daemon thread is killed
    while send_flag:
        sentence = input()
        clientSocket.send(sentence.encode())
        if sentence.lower() == 'bye':
            send_flag = False


# Create the sending thread as daemon to kill if other client
# decides to terminate
send_thread = threading.Thread(target=send_message)
send_thread.daemon = True
send_thread.start()

# Main thread listens for messages relayed through server from other client
flag = True
while flag:
    # Try to receive a message
    # if error or client sends terminate message, exit loop
    try:
        data = clientSocket.recv(1024)
        if not data:
            flag = False
        elif data.decode().lower() == 'from client x: bye' or data.decode().lower() == 'from client y: bye':
            print(data.decode())
            flag = False
        else:
            print(data.decode())
    except error as e:
        flag = False

# Close
print('\n...Closing connection...')
time.sleep(1)
clientSocket.close()



