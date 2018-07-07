#!/bin/bash

if [ "$1" == "--no-robot" ]; then
  # Instead of disabling ev3, use fake ev3 interface
  export PYTHONPATH=$(pwd)/src/fake3dev:$PYTHONPATH
  shift
fi

export PYTHONPATH=$(pwd):$PYTHONPATH
export DISPLAY=
xvfb-run ./src/webserver.py "$@"

# final cleanup: stopping motors
if [ -e /sys/class/tacho-motor ]; then
  for f in /sys/class/tacho-motor/*; do
    echo -n "Stopping "; cat $f/address
    echo reset > $f/command
  done
fi
