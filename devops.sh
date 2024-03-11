#!/bin/bash

if test -f ./source.txt; then
        > source.txt
else 
	touch ./source.txt
fi

if test -f ./target.txt; then
        > target.txt
else 
	touch ./target.txt
fi

if test -f ./transfer.sh; then
    	> transfer.sh && echo "Old transfer data has been deleted now.\nPlease update the source and target repos"
else 
	python3 ./main.py
fi
