#!/usr/bin/env python3
"""
LoEV3go -- LOGO language interpreter running on EV3 LEGO brick
Ondrej Bojar, bojar@ufal.mff.cuni.cz

It is easier to start this using ../loev3go.sh wrapper because:
- headless X window server has to be provided
- PYTHONPATH has to be set correctly.

Based on:
  https://gist.github.com/bradmontgomery/2219997
  ev3dev-lang-python/ev3dev/webserver.py
"""
# dbg print
from __future__ import print_function
import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

import pdb

from http.server import BaseHTTPRequestHandler, HTTPServer
from shutil import copyfile
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
import json

previewfilename = "output.svg"

log = logging.getLogger(__name__)

class LoEV3goHandler(BaseHTTPRequestHandler):

    # File extension to mimetype
    mimetype = {
        'css'  : 'text/css',
        'svg'  : 'image/svg+xml',
        'gif'  : 'image/gif',
        'html' : 'text/html',
        'txt'  : 'text/plain',
        'ico'  : 'image/x-icon',
        'jpg'  : 'image/jpg',
        'js'   : 'application/javascript',
        'png'  : 'image/png',
        'avi'  : 'video/avi'
    }
    last_valid_code = None
    robot_thread = None

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """
        If the request is for a known file type serve the file (or send a 404)
        and return True.
        If the request does not contain '.' in the path, assume it is a
        command.
        """

        eprint("GOT:", self.path)
        # pdb.set_trace();

        if self.path == "/":
            self.path = "/index.html"

        # Serve a file (image, css, html, etc)
        extension = self.path.split('.')[-1]
        if extension in self.mimetype:
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
          request = re.split("[\?/]", self.path, 2)
          eprint("SPLIT:", request)
          action = request[1]
          if action == 'stop':
            if self.cmdline_args.do_robot:
              eprint("Stopping robot")
              self.robot_should_stop.set();
            else:
              eprint("Robot not attached, nothing to stop.")
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            return True # event has been handled
          elif action == 'save-last-previewed-as':
            args = urllib.parse.parse_qs(request[2])
            args2 = json.loads(args["data"][0])
            saveId = args2["saveId"]
            msg = None
            if LoEV3goHandler.last_valid_code is not None:
              with open(("saved/%i.txt"%saveId), "w") as text_file:
                text_file.write(LoEV3goHandler.last_valid_code)
              copyfile(previewfilename, ("saved/%i.svg"%saveId))
              msg = "Saved"
            else:
              msg = "Not saving, please first run Preview"
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            eprint(msg)
            self.wfile.write(msg.encode("utf-8"))
            return True # event has been handled
          elif action == 'run-last-valid-code':
            robotconfig = urllib.parse.parse_qs(request[2])
            eprint("GOT REQUEST CONFIG: ", robotconfig)
            robotconfigdata = json.loads(robotconfig["data"][0])
            # Interpret integers:
            for varname in ['polarity', 'scale', 'travel_speed',
                'angle_scale_travel']:
              robotconfigdata[varname] = int(robotconfigdata[varname])
            eprint("GOT REQUEST CONFIG DATA: ", robotconfigdata)
            if self.cmdline_args.do_robot:
              if LoEV3goHandler.last_valid_code is not None:
                if LoEV3goHandler.robot_is_stopped.is_set():
                  # the robot is not running
                  # join the previous thread, if needed
                  if LoEV3goHandler.robot_thread is not None:
                    LoEV3goHandler.robot_thread.join()
                  eprint("Starting logo ev3")
                  LoEV3goHandler.robot_should_stop.clear();
                    # so that anyone can notify the robot to stop
                  ## run without threads:
                  LoEV3goHandler.loc.run_logo_robot(LoEV3goHandler.last_valid_code)
                  ## threaded run:
                  #LoEV3goHandler.robot_thread = threading.Thread(
                  #  target=LoEV3goHandler.loc.run_logo_robot,
                  #  args = [LoEV3goHandler.last_valid_code, robotconfigdata])
                  #eprint("Starting robot thread")
                  #LoEV3goHandler.robot_thread.start()
                  msg = "Drawing..."
                else:
                  msg = "Cannot start, already running."
              else:
                msg = "No code has been successfully previewed."
            else:
              msg = "Robot not attached, nothing to do."
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            eprint(msg)
            self.wfile.write(msg.encode("utf-8"))
            return True # event has been handled

        return False

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # get LOGO source code
        # return one of:
        #   O...and.the.rendered.image...
        #   E...and.the.LOGO.error...
        eprint("GOT POST request, the only one is 'preview', so previewing...")
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        obj = urllib.parse.parse_qs(post_data)
        code = obj['code'][0]
        eprint(code)
        try:
          LoEV3goHandler.lis.run_logo_emit_svg(code, previewfilename)
          eprint("Saved into:", previewfilename)
          with open(previewfilename, 'r') as myfile:
            rawsvg = myfile.read()
          output = b"Odata:image/svg+xml;base64,"+stringToBase64(rawsvg);
          LoEV3goHandler.last_valid_code = code
        except Exception as e: #pylogo.common.LogoNameError as e:
          eprint("Error:", e)
          # pdb.set_trace()
          output = b"E"+str(e).encode("utf-8")
          LoEV3goHandler.last_valid_code = None
        self._set_headers()
        #self.wfile.write(output.encode("utf-8"))
        self.wfile.write(output)
        
class MyException(Exception):
    pass

def run(main_exit, server_class=HTTPServer, handler_class=LoEV3goHandler,
        port=8080,
        root="web/"):
    print("Port: ",  port)
    server_address = ('0.0.0.0', port) # accept connections to any of our IPs
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

  handler_class = LoEV3goHandler
  # set class variables, "global vars" for the class and input args for our
  # handler

  # main exit switch: everyone should listen to this and exit gracefully
  handler_class.main_exit = threading.Event() # set this to stop gracefully
  handler_class.robot_should_stop = threading.Event()
    # set this to stop running EV3 logo
  handler_class.robot_is_stopped = threading.Event()
    # read this to see if the robot is stopped

  handler_class.cmdline_args = args
  # Initialize drawing LOGO into SVG
  handler_class.lis = LogoIntoSVG.LogoIntoSVG()
  if args.do_robot:
    # Initialize handling IR requests for robot drawing:
    import SpeedableTrackerWithPen
    eprint("Creating tracker object")
    t = SpeedableTrackerWithPen.SpeedableTrackerWithPen(handler_class.main_exit)
    eprint("Creating tracker thread")
    tracker_thread = threading.Thread(target=t.run, args=())
    #t.run()
    eprint("Starting tracker thread")
    tracker_thread.start()
    # launch in a thread, it will finish after main_exit is set
  
    # Initialize handling LOGO scripts
    import LogoOntoCarpet
    handler_class.loc = LogoOntoCarpet.LogoOntoCarpet(
      handler_class.robot_should_stop,
      handler_class.robot_is_stopped)
  else:
    eprint("Robot disabled, not starting it")

  eprint("Starting web server.")
  try:
    run(handler_class.main_exit, port=args.port, handler_class=handler_class)
  finally:
    # everyone should totally stop, set the threading event
    handler_class.main_exit.set()
    if tracker_thread is not None:
      tracker_thread.join()
    if LoEV3goHandler.robot_thread is not None:
      LoEV3goHandler.robot_thread.join()
