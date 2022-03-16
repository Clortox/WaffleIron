#!/bin/bash
sudo pip install -e .
export FLASK_APP=app/__init__.py

#if an argument is passed, then we are in production
#call this script as ./run.sh prod
#or something similar

if [ $# -eq 0 ]; then
    export FLASK_DEBUG=1
else
    export FLASK_DEBUG=0
fi

flask run
