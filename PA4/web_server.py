#!/usr/bin/env python3

# Names: Alonso Vega, Daniel Letterman, Gabe Williams, & Nicholas Fotinakes
# Team: 10
# Date: 6-18-2022
# Title: PA4 - web_server.py
# Description: This program acts as TLS-enabled simple web server to launch on h2

import http.server
import ssl

## Variables you can modify
server_address = "www.webpa4.test"
server_port = 4443
ssl_key_file = "/home/mininet/CST311/PA4/pa4certs/private/webpa4.test-key.pem"
ssl_certificate_file = "/home/mininet/CST311/PA4/pa4certs/newcerts/webpa4.test-cert.pem"


## Don't modify anything below
httpd = http.server.HTTPServer((server_address, server_port),
http.server.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket,
                server_side=True,
                               keyfile=ssl_key_file,
                               certfile=ssl_certificate_file,
                ssl_version=ssl.PROTOCOL_TLSv1_2)

print("Listening on port", server_port)
httpd.serve_forever()
