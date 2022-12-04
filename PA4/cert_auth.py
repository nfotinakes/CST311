#!/usr/bin/env python3

# Names: Alonso Vega, Daniel Letterman, Gabe Williams, & Nicholas Fotinakes
# Team: 10
# Date: 6-18-2022
# Title: PA4 - ca_cer_auth.py
# Description: This script acts as the certificate authority to create the root CA and certificate as well
# as the Server certificate for the web server for a successful wget

import subprocess
import os

# Check if our folder for all certificates/keys exist, if so delete
if os.path.exists("/home/mininet/CST311/PA4/pa4certs"):
    subprocess.call(['sudo', 'rm', '-rf', '/home/mininet/CST311/PA4/pa4certs'])

# Other create directory and subdirectories
os.mkdir('/home/mininet/CST311/PA4/pa4certs')
os.mkdir('/home/mininet/CST311/PA4/pa4certs/newcerts')
os.mkdir('/home/mininet/CST311/PA4/pa4certs/private')

# Specify the working directory
working_dir = '/home/mininet/CST311/PA4/pa4certs'

# Generate CA private key
subprocess.call(['sudo', 'openssl', 'genrsa', '-aes256', '-out', 'pa4cakey.pem', '-passout', 'pass:1234', '2048'], cwd=working_dir)

# Create Root CA certificate
subprocess.call(['sudo', 'openssl', 'req', '-x509', '-new', '-nodes', '-key', 'pa4cakey.pem', '-sha256', '-days', '3', '-out', 'pa4cacert.pem', '-passin','pass:1234', '-subj', '/C=US/ST=CA/L=Seaside/O=CST311/OU=Networking/CN=ca.pa4.test'], cwd=working_dir)

# Move private key into private folder
subprocess.call(['sudo', 'mv', './pa4cakey.pem', './private'], cwd=working_dir)

# Copy Root CA into ca-certificates directory
subprocess.call(['sudo', 'cp', 'pa4cacert.pem', '/usr/local/share/ca-certificates/pa4cacert.crt'], cwd=working_dir)

# Update ca-certificates application
subprocess.call(['sudo', 'update-ca-certificates'])

# Generate Server private key
subprocess.call(['sudo', 'openssl', 'genrsa', '-out', 'webpa4.test-key.pem', '2048'], cwd=working_dir)

# Generate certificate signing request using server private key
subprocess.call(['sudo', 'openssl', 'req', '-nodes', '-new', '-config', '/etc/ssl/openssl.cnf', '-key', 'webpa4.test-key.pem', '-out', 'webpa4.test.csr', '-subj', '/C=US/ST=CA/L=Seaside/O=CST311/OU=Networking/CN=www.webpa4.test'], cwd=working_dir)

# Create server certificate
subprocess.call(['sudo', 'openssl', 'x509', '-req', '-days', '365', '-in', 'webpa4.test.csr', '-CA', 'pa4cacert.pem', '-CAkey', './private/pa4cakey.pem', '-CAcreateserial', '-out', 'webpa4.test-cert.pem', '-passin', 'pass:1234'], cwd=working_dir)

# Move certificate and key into subdirectories
subprocess.call(['sudo', 'mv', './webpa4.test-cert.pem', './newcerts'], cwd=working_dir)
subprocess.call(['sudo', 'mv', './webpa4.test-key.pem', './private'], cwd=working_dir)

# Add IP and domain of Root and Server and hosts
subprocess.call(["sudo", "sh", "-c", "echo \"127.0.0.1\tca.pa4.test\" >> /etc/hosts"])
subprocess.call(["sudo", "sh", "-c", "echo \"10.0.1.2\twww.webpa4.test\" >> /etc/hosts"])

# Change permissions of pa4certs/private folder to protect private keys
subprocess.call(["sudo", "chmod", "-R", "600", "private"], cwd=working_dir) 
