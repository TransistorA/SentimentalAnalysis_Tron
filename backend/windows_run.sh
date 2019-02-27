#!/usr/bin/env bash

export FLASK_APP=app.py
export FLASK_ENV=development
echo $PYTHONPATH
flask run -p 8080
