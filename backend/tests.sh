#!/usr/bin/env bash

PYTHONPATH=solver  
export PYTHONPATH 
python -m unittest discover -p 'test_*.py'
