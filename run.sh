#!/bin/bash
which sudo
if [ $? -eq 0 ]; then
    sudo pip install -e .
else
    pip install -e .
fi
export FLASK_APP=app/__init__.py

#if an argument is passed, then we are in production
#call this script as ./run.sh prod
#or something similar

if [ $# -eq 0 ]; then
    export FLASK_DEBUG=1
else
    export FLASK_DEBUG=0
fi

flask run --host=0.0.0.0
