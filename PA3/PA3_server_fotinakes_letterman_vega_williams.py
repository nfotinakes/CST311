# Team: 10
# Names: Alonso Vega, Daniel Letterman, Gabe Williams, & Nicholas Fotinakes
# Date: 2022-05-31
# Assignment Title: PA #3 - TCP Server
# Description: This program acts as the TCP Server that accepts two client connections X and Y
# using multithreading and handles a message between the two, keeping track of the order, and then closes connections

# Criteria 11: Explain why you need multithreading to solve this problem
#
# Multithreading is needed to solve this problem of handling connection-oriented sessions between
# multiple clients and a server. Accepting a client connection using the .accept() will only allow the socket to
# work with one connection at a time unless called multiple times. In order to handle multiple clients concurrently,
# additional threads must be created to delegate the work and create a separate socket for each thread/client after
# accepting a connection. This behaves like a common TCP connection, where there is one "welcome socket" that handles
# the three-way handshake when a client initiates contact with the server. Then the server can create a new thread for
# each connection and create a unique "connection socket" for that thread to handle communication between every
# concurrent client and the server.


import threading
from socket import *
import time


# Function to track order of messages received
def message_tracker(client, message):
    message_order.append(client + ": " + message)


# Function to increment message received count
def message_counter():
    global message_count
    message_count = message_count + 1


# Class for a new client thread to handle each connection
class NewClientThread(threading.Thread):

    # Initialize new client thread with client information
    def __init__(self, client_address, client_sock, name):
        threading.Thread.__init__(self)
        self.cli_socket = client_sock
        self.address = client_address
        self.clients_name = name

    # Run function handles messages received from client
    def run(self):
        # Block and wait to receive message from client
        data = self.cli_socket.recv(1024).decode()
        # When received acquire condition
        message_condition.acquire()
        # Update the message tracker list and increment message counter
        message_tracker(self.clients_name, data)
        message_counter()
        # Print message from client on server side
        print("Client " + self.clients_name + " sent message " + str(message_count) + ": " + data)
        # Notify main thread
        message_condition.notify()
        message_condition.release()

    # Function to send acceptance method to waiting client to begin sending message
    def accept_connection(self):
        acceptance_message = 'Client ' + self.clients_name + ' connected'
        self.cli_socket.send(acceptance_message.encode())

    # Function to send closing message to client about message order
    # Then close thead client socket
    def send_closing(self):
        server_message = message_order[0] + ' received before ' + message_order[1]
        self.cli_socket.send(server_message.encode())
        self.cli_socket.close()


# Create port and TCP type socket for server
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)

# Associate port with this socket, and listen for TCP connection requests
serverSocket.bind(('', serverPort))

print('The server is waiting to receive 2 connections....\n')

allThreads = []     # List to hold client threads
message_order = []  # Array to hold client messages received/order

# Condition for lock and main thread wait using number of messages
message_condition = threading.Condition()
message_count = 0

# Max number of connections for the server
max_connections = 2
serverSocket.listen(max_connections)
while True:
    # Accept client connection
    client_socket, client_addr = serverSocket.accept()

    # If first connection, name it X and create client instance with client attributes
    if len(allThreads) == 0:
        client_name = 'X'
        new_thread = NewClientThread(client_addr, client_socket, client_name)
        allThreads.append(new_thread)
        print('Accepted first connection, calling it client ' + client_name)

    # If second connection, name it Y and create client instance with client attributes
    elif len(allThreads) == 1:
        client_name = 'Y'
        new_thread = NewClientThread(client_addr, client_socket, client_name)
        allThreads.append(new_thread)
        print('Accepted second connection, calling it client ' + client_name)

    # When the length of the thread list is equal to max connections (2 in this case) then send both clients
    # their acceptance message to unblock, start the threads, and allow messages to be sent. Exit loop
    if len(allThreads) == max_connections:
        for t in allThreads:
            t.accept_connection()
            t.start()
        print('\nWaiting to receive messages from client X and client Y....\n')
        break

# Main thread waits for total of two messages to be sent (protected by condition/locks) before proceeding
message_condition.acquire()
while message_count != 2:
    message_condition.wait()
message_condition.release()

# When both messages received send the closing message to clients and client threads close connections
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
