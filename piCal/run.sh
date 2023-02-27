#!/bin/sh

# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd /home/pi/piCal/piCal
python3 display.py
cd /
sleep 10
sudo reboot now