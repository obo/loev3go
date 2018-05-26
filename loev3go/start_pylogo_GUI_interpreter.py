#!/usr/bin/python
#
# BROKEN
# This script should run the traditional pylogo user inferface.
# It worked well while pylogo was in python2 and relying on python mega widgets
# (Pmw) version 1.3. Pmw1.3 is for python2 only and I don't have the time to
# try getting Pmw2 running (https://pypi.org/project/Pmw/)
#
# remember that PYTHONPATH must include two directories:
#   export PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/Pmw.1.3
import pylogo.script
pylogo.script.main()

