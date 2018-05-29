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
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import argparse
import threading, signal
import LogoIntoSVG

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

    def __init__(self, main_exit, args):
      # Initialize drawing LOGO into SVG
      self.lis = LogoIntoSVG.LogoIntoSVG()

      if args.do_robot:
        # Initialize handling IR requests for robot drawing:
        import SpeedableTrackerWithPen
        t = SpeedableTrackerWithPen(main_exit)
        t.run() # launch in a thread, it will finish after main_exit is set
    
        # Initialize handling LOGO scripts
        # XXX

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """
        If the request is for a known file type serve the file (or send a 404) and return True
        """

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
          pass

        return False

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        
def run(server_class=HTTPServer, handler_class=LoEV3goHandler,
        port=8080,
        root="web/"):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Chdir to: %s" % root)
    os.chdir(root)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='LoEV3go: Webserver and turtle robot for EV3.')
  parser.add_argument('--no-robot', action='store_false', dest="do_robot",
    help="don't load robot modules")
  parser.add_argument('--port', type=int, default=8080, nargs=1,
    help='which port to use')
  args = parser.parse_args()

  # main exit switch: everyone should listen to this and exit gracefully
  main_exit = threading.Event() # set this to stop gracefully
  # gracefully die on signals
  def signal_handler(signal, frame):
    main_exit.set()
  signal.signal(signal.SIGINT,  signal_handler)
  signal.signal(signal.SIGTERM, signal_handler)

  ourhandler = LoEV3goHandler(main_exit, args)

  try:
    run(port=args.port, handler_class=ourhandler)
  finally:
    # everyone should totally stop, set the threading event
    main_exit.set()
