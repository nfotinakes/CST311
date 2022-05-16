# Names: Alonso Vega, Daniel Letterman, Gabe Williams, & Nicholas Fotinakes
# Team: 10
# Date: 2022-05-17
# Title: PA#2 - UDP Pinger Client
# Description: This program acts as the client and sends 10 pings to the server host on h2
# and then calculates min/max and average RTT time, estimated RTT, RTT deviation, packet loss
# percentage, and the timeout interval

from socket import *
import time

# Set server name to h2 address and server port 12000
serverName = '10.0.0.2'
serverPort = 12000

# Create UDP Socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Set socket timeout to one second
clientSocket.settimeout(1)

# Define constants alpha and beta
ALPHA = 0.125
BETA = 0.25

# Variables to hold minimum, maximum, total rtt values, and total successful packets received
# Initial values set to 0
min_rtt = 0
max_rtt = 0
total_rtt = 0
rec_packets = 0

# Define variables to store values for calculations
# Initial values set to 0 (Timeout to one second in ms)
est_rtt = 0
dev_rtt = 0
sample_rtt = 0
timeout_int = 1000

# For loop to send 10 pings to the server
for i in range(1, 11):
    # Create the message to send to server with ping number
    ping_num = i
    message = 'Ping' + str(ping_num)

    # Log send time and send the message to server (time recorded in seconds)
    send_time = time.time()
    clientSocket.sendto(message.encode(), (serverName, serverPort))

    # Try/exception block to handle lost packets
    try:
        # Try to receive modified message from server, if successful log the time packet received (in seconds)
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        receive_time = time.time()

    # If packet is lost and timeout triggered print the timeout message
    except timeout:
        print('Mesg sent: ' + message)
        print('No Mesg rcvd')
        print('PONG ' + str(ping_num) + ' Request Timed out\n')

    # If packet received successfully print and calculate
    else:
        # Print received packet information
        print('Mesg sent: ' + message)
        print('Mesg rcvd: ' + modifiedMessage.decode())
        print('Start time: ' + str(send_time))
        print('Return time: ' + str(receive_time))
        rtt = (receive_time - send_time) * 1000  # Convert rtt from seconds to ms
        print('PONG ' + str(ping_num) + ' RTT: ' + str(rtt) + ' ms\n')
        rec_packets += 1  # Log a successfully received packet

        # If this is the first successful packet received
        # Set initial values based on first rtt value
        if rec_packets == 1:
            sample_rtt = rtt
            est_rtt = sample_rtt
            dev_rtt = sample_rtt / 2
            min_rtt = sample_rtt
            max_rtt = sample_rtt
            total_rtt = sample_rtt

        # For all the other successfully received packets
        else:
            # Check for min/max RTT times
            if rtt < min_rtt:
                min_rtt = rtt
            if rtt > max_rtt:
                max_rtt = rtt
            # Set the current sample RTT
            sample_rtt = rtt
            # Update RTT sum for average at end
            total_rtt += rtt
            # Calculate Estimated RTT, RTT Deviation, and timeout interval
            est_rtt = (1 - ALPHA) * est_rtt + (ALPHA * sample_rtt)
            dev_rtt = (1 - BETA) * dev_rtt + (BETA * abs(sample_rtt - est_rtt))

clientSocket.close()

# Calculate average RTT of all packets successfully received
avg_rtt = total_rtt / rec_packets

# Calculate percentage of lost packets
packet_loss_percent = ((10 - rec_packets) / 10) * 100

# Calculate timeout interval
timeout_int = est_rtt + (4 * dev_rtt)

# Print final statistics
print('Min RTT:         ' + str(min_rtt) + ' ms')
print('Max RTT:         ' + str(max_rtt) + ' ms')
print('Avg RTT:         ' + str(avg_rtt) + ' ms')
print('Packet Loss:     ' + str(packet_loss_percent) + '%')
print('Estimated RTT:   ' + str(est_rtt) + ' ms')
print('Dev RTT:         ' + str(dev_rtt) + ' ms')
print('Timeout Interval:' + str(timeout_int) + ' ms')
