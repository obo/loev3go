#!/usr/bin/env python3
# LoEV3go web server.
# Launches the server on the given port
"""

"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from src.webserver import LoEV3goHandler

def run(server_class=HTTPServer, handler_class=LoEV3goHandler,
        port=8080,
        root="web/"):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Chdir to: %s" % root)
    os.chdir(root)
    print('Starting httpd...')
    httpd.serve_forever()

from sys import argv

if len(argv) == 2:
    run(port=int(argv[1]))
else:
    run()
