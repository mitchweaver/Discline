#!/bin/bash

# see the README.md to find out how to get this
TOKEN="put your token here"

# you can put this anywhere
# if you use the .desktop, make sure to change its path too
FOLDER="/path/to/term_disc"

# if you have python3.5, change this
PYTHON="python3.6"

cd $FOLDER
$PYTHON $FOLDER/main.py "$TOKEN"

