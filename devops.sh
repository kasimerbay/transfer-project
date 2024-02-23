#!/bin/bash

if test -f ./transfer.sh; then
    ./transfer.sh
else python3 ./main.py
fi