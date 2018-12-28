#!/bin/bash

mkdir .config
python3 Discline.py --store-token $1
python3 Discline.py --copy-skeleton
python3 Discline.py
