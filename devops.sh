#!/bin/bash

if test -f ./source.txt; then
        echo "source file exists"
else touch ./source.txt
fi

if test -f ./target.txt; then
        echo "target file exists"
else touch ./target.txt
fi

if test -f ./transfer.sh; then
    ./transfer.sh
else python3 ./main.py
fi
