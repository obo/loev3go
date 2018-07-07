#!/bin/bash
# The main entry of LoEV3go.
# It sets PYTHONPATH to use the Pmw.1.3 here and optionally to use
# fake EV3 python interface for testing on a plain computer.

function die() { echo "$@" >&2; exit 1; }

if [ "$1" == "--fake3dev" ]; then
  # Instead of disabling ev3, use fake ev3 interface
  export PYTHONPATH=$(pwd)/src/fake3dev:$PYTHONPATH
  shift
fi

which  xvfb-run > /dev/null 2>/dev/null \
|| die "xvfb-run needed. Please install xvfb (sudo apt-get install xvfb)"

export PYTHONPATH=$(pwd):$PYTHONPATH
export DISPLAY=
xvfb-run ./src/loev3go.py "$@"

# final cleanup: stopping motors
if [ -e /sys/class/tacho-motor ]; then
  for f in /sys/class/tacho-motor/*; do
    echo -n "Stopping "; cat $f/address
    echo reset > $f/command
  done
fi
