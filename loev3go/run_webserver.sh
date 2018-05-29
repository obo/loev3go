#!/bin/bash

export PYTHONPATH=$(pwd):$PYTHONPATH
./src/webserver.py "$@"
