#!/bin/bash

if [[ $_ == $0 ]]; then
  echo "This script needs to be sourced!" >&2
  exit 1
fi

export LD_LIBRARY_PATH=/home/robot/compiled-for-robot/aruco/lib:/home/robot/compiled-for-robot/opencv/lib
export PATH=$PATH:/home/robot/compiled-for-robot/aruco/bin:/home/robot/compiled-for-robot/markermapper/bin
