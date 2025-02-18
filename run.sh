#!/bin/bash

pip install -r requirements.txt > /dev/null

if $1 == "-b"
  python exec-bot.py
else
  python exec.py
fi
