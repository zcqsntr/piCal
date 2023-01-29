#!/bin/sh

# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd /home/pi/piCal/piCal
sudo python3 display.py
cd /