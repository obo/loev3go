#!/usr/bin/env python3
"""
From https://gist.github.com/bradmontgomery/2219997
and from ev3dev-lang-python/ev3dev/webserver.py

Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
# dbg print
from __future__ import print_function
import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

import pdb

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib
import base64
def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))
import re
import argparse
import threading, signal
import LogoIntoSVG
import pylogo.common
import logging

log = logging.getLogger(__name__)

class LoEV3goHandler(BaseHTTPRequestHandler):

    # File extension to mimetype
    mimetype = {
        'css'  : 'text/css',
        'svg'  : 'image/svg+xml',
        'gif'  : 'image/gif',
        'html' : 'text/html',
        'ico'  : 'image/x-icon',
        'jpg'  : 'image/jpg',
        'js'   : 'application/javascript',
        'png'  : 'image/png'
    }

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """
        If the request is for a known file type serve the file (or send a 404) and return True
        """

        eprint("GOT:", self.path)

        if self.path == "/":
            self.path = "/index.html"

        # Serve a file (image, css, html, etc)
        if '.' in self.path:
            extension = self.path.split('.')[-1]
            mt = self.mimetype.get(extension)

            if mt:
                filename = os.curdir + os.sep + self.path

                # Open the static file requested and send it
                if os.path.exists(filename):
                    self.send_response(200)
                    self.send_header('Content-type', mt)
                    self.end_headers()

                    if extension in ('gif', 'ico', 'jpg', 'png'):
                        # Open in binary mode, do not encode
                        with open(filename, mode='rb') as fh:
                            self.wfile.write(fh.read())
                    else:
                        # Open as plain text and encode
                        with open(filename, mode='r') as fh:
                            self.wfile.write(fh.read().encode())
                else:
                    log.error("404: %s not found" % self.path)
                    self.send_error(404, 'File Not Found: %s' % self.path)
                return True
        else:
          # Handle request
          path = re.split("[\?/]", self.path)
          eprint("SPLIT:", path)
          action = path[1]
          if action == 'stop':
            if self.cmdline_args.do_robot:
              eprint("Stopping robot")
            else:
              eprint("Robot not attached, nothing to stop.")
            return True # event has been handled

        return False

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        obj = urllib.parse.parse_qs(post_data)
        code = obj['code'][0]
        eprint(code)
        outfile="output.svg"
        try:
          LoEV3goHandler.lis.run_logo_emit_svg(code, outfile)
          with open(outfile, 'r') as myfile:
            rawsvg = myfile.read()
          output = b"data:image/svg+xml;base64,"+stringToBase64(rawsvg);
        except pylogo.common.LogoNameError as e:
          eprint("Error:", e)
          output = b""
        self._set_headers()
        #self.wfile.write(output.encode("utf-8"))
        self.wfile.write(output)
        
class MyException(Exception):
    pass

def run(main_exit, server_class=HTTPServer, handler_class=LoEV3goHandler,
        port=8080,
        root="web/"):
    print("Port: ",  port)
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    print("Chdir to: %s" % root)
    os.chdir(root)

    # gracefully die on signals
    def signal_handler(signal, frame):
      eprint("Setting main_exit")
      main_exit.set()
      # should stop the motors!
      # raise an exception, that's the easiest way to interrupt the webserver
      raise MyException("User interrupt")
    signal.signal(signal.SIGINT,  signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print('Starting httpd...')
    httpd.serve_forever()
    # the following did not really work, it needed to get one more request:
    # while not main_exit.is_set():
      # eprint("Serving")
      # httpd.handle_request()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='LoEV3go: Webserver and turtle robot for EV3.')
  parser.add_argument('--no-robot', action='store_false', dest="do_robot",
    help="don't load robot modules")
  parser.add_argument('--port', type=int, default=8080,
    help='which port to use')
  args = parser.parse_args()

  # main exit switch: everyone should listen to this and exit gracefully
  main_exit = threading.Event() # set this to stop gracefully

  handler_class = LoEV3goHandler
  # set class variables, "global vars" for the class and input args for our
  # handler
  handler_class.main_exit = main_exit
  handler_class.cmdline_args = args
  # Initialize drawing LOGO into SVG
  handler_class.lis = LogoIntoSVG.LogoIntoSVG()
  if args.do_robot:
    # Initialize handling IR requests for robot drawing:
    import SpeedableTrackerWithPen
    t = SpeedableTrackerWithPen(main_exit)
    t.run() # launch in a thread, it will finish after main_exit is set
  
    # Initialize handling LOGO scripts
    # XXX
  else:
    eprint("Robot disabled, not starting it")

  try:
    run(main_exit, port=args.port, handler_class=handler_class)
  finally:
    # everyone should totally stop, set the threading event
    main_exit.set()
