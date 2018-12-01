#!/usr/bin/env bash

PYTHONPATH=solver:src python -m unittest discover -p 'test_*.py'
