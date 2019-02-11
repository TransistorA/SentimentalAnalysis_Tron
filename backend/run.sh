#!/usr/bin/env bash

export FLASK_APP=app.py
export FLASK_ENV=development
export PYTHONPATH=${PYTHONPATH}:src:solver
flask run -p 8080
