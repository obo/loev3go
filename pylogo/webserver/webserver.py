#!/usr/bin/env python3
# a simple webserver serving just a HTML with textarea and responding by
# running the logo
#
# Based on ev3dev-lang-python/ev3dev/webserver.py

# Get the minimal web server from here:
# https://gist.github.com/bradmontgomery/2219997
#


from http.server import BaseHTTPRequestHandler, HTTPServer


# ==================
# Web Server classes
# ==================
class RobotWebHandler(BaseHTTPRequestHandler):
    """
    Base WebHandler class for various types of robots.

    RobotWebHandler's do_GET() will serve files, it is up to the child
    class to handle REST APIish GETs via their do_GET()

    self.robot is populated in RobotWebServer.__init__()
    """

    # File extension to mimetype
    mimetype = {
        'css'  : 'text/css',
        'gif'  : 'image/gif',
        'html' : 'text/html',
        'ico'  : 'image/x-icon',
        'jpg'  : 'image/jpg',
        'js'   : 'application/javascript',
        'png'  : 'image/png'
    }

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

        return False

    def log_message(self, format, *args):
        """
        log using our own handler instead of BaseHTTPServer's
        """
        # log.debug(format % args)
        pass


max_move_xy_seq = 0
motor_max_speed = None
medium_motor_max_speed = None
joystick_enaged = False

class LogoWebHandler(RobotWebHandler):

    def __str__(self):
        return "%s-LogoWebHandler" % self.robot

    def do_GET(self):
        """
        Returns True if the requested URL is supported
        """

        if RobotWebHandler.do_GET(self):
            return True

        global motor_max_speed
        global medium_motor_max_speed
        global max_move_xy_seq
        global joystick_engaged

        action = self.path

        if action == 'stop':
            log.debug("seq %d: stop" % seq)
            self.robot.left_motor.stop()
            self.robot.right_motor.stop()
        else:
            log.warning("Unsupported URL %s" % self.path)

        self.send_response(204)
        return True


class RobotWebServer(object):
    """
    A Web server so that 'robot' can be controlled via 'handler_class'
    """

    def __init__(self, robot, handler_class, port_number=8000):
        self.content_server = None
        self.handler_class = handler_class
        self.handler_class.robot = robot
        self.port_number = port_number

    def run(self):

        try:
            log.info("Started HTTP server (content) on port %d" % self.port_number)
            self.content_server = HTTPServer(('', self.port_number), self.handler_class)
            self.content_server.serve_forever()

        # Exit cleanly, stop both web servers and all motors
        except (KeyboardInterrupt, Exception) as e:
            log.exception(e)

            if self.content_server:
                self.content_server.socket.close()
                self.content_server = None

            for motor in list_motors():
                motor.stop()

tank=...XXXinicializuj-robota...
www=RobotWebServer(tank, LogoWebHandler, port_number)


# class WebControlledLogo(Tank):
#     """
#     A tank that is controlled via a web browser
#     """
# 
#     def __init__(self, left_motor, right_motor, polarity='normal', port_number=8000):
#         Tank.__init__(self, left_motor, right_motor, polarity)
#         self.www = RobotWebServer(self, TankWebHandler, port_number)
# 
#     def main(self):
#         # start the web server
#         self.www.run()
