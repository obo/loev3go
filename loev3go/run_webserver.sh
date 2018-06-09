#!/bin/bash

if [ "$1" == "--no-robot" ]; then
  # Instead of disabling ev3, use fake ev3 interface
  export PYTHONPATH=$(pwd)/src/fake3dev:$PYTHONPATH
  shift
fi

export PYTHONPATH=$(pwd):$PYTHONPATH
export DISPLAY=
xvfb-run ./src/webserver.py "$@"
