#!/bin/bash

export PYTHONPATH=$(pwd):$PYTHONPATH
export DISPLAY=
xvfb-run ./src/webserver.py "$@"
