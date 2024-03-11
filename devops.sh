#!/bin/bash

if test -f ./source.txt; then
<<<<<<< HEAD
	echo "source file exists"
=======
        > source.txt
>>>>>>> feature
else touch ./source.txt
fi

if test -f ./target.txt; then
<<<<<<< HEAD
	echo "target file exists"
=======
        > target.txt
>>>>>>> feature
else touch ./target.txt
fi

if test -f ./transfer.sh; then
    rm ./transfer.sh && echo "Old transfer data has been deleted now.\nPlease update the source and target repos"
else python3 ./main.py
fi
<<<<<<< HEAD
=======

>>>>>>> feature
