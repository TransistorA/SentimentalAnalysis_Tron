#!/usr/bin/env bash

export PYTHONPATH=$PYTHONPATH:solver
python -m unittest discover -p 'test_*.py'
