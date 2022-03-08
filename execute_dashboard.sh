#!/bin/bash

export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="${PYTHONPATH}:${PWD}"
eval "./env/bin/python3 -u ./dashboard/server.py ${@:2}"