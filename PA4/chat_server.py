#!/usr/bin/env python3

# Names: Alonso Vega, Daniel Letterman, Gabe Williams, & Nicholas Fotinakes
# Team: 10
# Date: 6-18-2022
# Title: PA4 - chat_server.py
# Description: This program acts as the TCP Server that accepts two client connections X and Y
# handles chat messaging between them using multithreading until one wants to close the connection using 'bye'
# which signals the server to close connections and send the termination word to the clients

import threading
from socket import *
import time


# Function to change thread condition
def set_close_condition():
    global close_connection
    close_connection = True


# Class for a new client thread to handle each connection
class NewClientThread(threading.Thread):

    # Initialize new client thread with client information
    def __init__(self, client_address, client_sock, name):
        threading.Thread.__init__(self)
        self.cli_socket = client_sock
        self.address = client_address
        self.clients_name = name

    # Run function handles messages received from clients
    def run(self):
        flag = True
        while flag:
            # Try to receive a message from a client, break if error occurs
            try:
                data = self.cli_socket.recv(1024).decode()
            except error:
                break

            # Determine which client sent message, and relay message to other client
            if data and self.clients_name == 'X':
                header = 'From Client X: ' + data
                message_to_send = header.encode()
                allThreads[1].cli_socket.send(message_to_send)
                print('Message from Client X to Client Y: ' + data)
            elif data and self.clients_name == 'Y':
                header = 'From Client Y: ' + data
                message_to_send = header.encode()
                allThreads[0].cli_socket.send(message_to_send)
                print('Message From Client Y to Client X: ' + data)

            # If message received is the termination word, exit loop
            if data.lower() == 'bye':
                flag = False

        # Change condition and notify main thread
        close_condition.acquire()
        set_close_condition()
        close_condition.notify()
        close_condition.release()

    # Function to send acceptance method to waiting client to begin chat
    def accept_connection(self):
        if self.clients_name == 'X':
            acceptance_message = 'Welcome Client X, you are chatting with Client Y:\n'
            self.cli_socket.send(acceptance_message.encode())
        else:
            acceptance_message = 'Welcome Client Y, you are chatting with Client X:\n'
            self.cli_socket.send(acceptance_message.encode())

    # close thread socket
    def send_closing(self):
        self.cli_socket.close()


# Create port and TCP type socket for server
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)

# Associate port with this socket, and listen for TCP connection requests
serverSocket.bind(('', serverPort))

print('The server is waiting to receive 2 connections....\n')

allThreads = []  # List to hold client threads
client_name = ''  # Initialize client name
close_connection = False

# Condition for lock and main thread wait
close_condition = threading.Condition()

# Max number of connections for the server
num_connections = 0
max_connections = 2
serverSocket.listen(max_connections)
while True:
    # Accept client, and set name based on order connected
    client_socket, client_addr = serverSocket.accept()
    if len(allThreads) == 0:
        client_name = 'X'
        new_thread = NewClientThread(client_addr, client_socket, client_name)
        allThreads.append(new_thread)
        print('Accepted first connection, calling it client ' + client_name)
    elif len(allThreads) == 1:
        client_name = 'Y'
        new_thread = NewClientThread(client_addr, client_socket, client_name)
        allThreads.append(new_thread)
        print('Accepted second connection, calling it client ' + client_name)

    # If the connections are equal to the number of expected threads
    # then send the both clients their acceptance message to unblock and start the
    # thread and allow messages to be sent
    if len(allThreads) == max_connections:
        for t in allThreads:
            t.accept_connection()
            t.start()
        print('\nWaiting to receive messages from client X and client Y....\n')
        break

# Main thread waits until clients decide to close
close_condition.acquire()
while not close_connection:
    close_condition.wait()
close_condition.release()

# When clients are done chatting, close sockets
print("\nWaiting a bit to for clients to close their connections")
for t in allThreads:
    t.send_closing()

# Allow 3 seconds to wait
time.sleep(3)

# Client threads complete
for t in allThreads:
    t.join()

# Server socket close and print done message
serverSocket.close()
print('Done.')
