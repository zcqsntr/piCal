#!/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from get_events import get_events
from get_weather import get_weather
from get_image import CalDraw

import sys
import os


picdir = os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),'RaspberryPi_JetsonNano', 'python', 'pic')))
libdir = os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),'RaspberryPi_JetsonNano', 'python', 'lib')))
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
#from waveshare_epd import epd7in5b_V2
from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback



calendar_ids = ['6e56207b41dd787f37a38aa0794de8dab5243c611088ca04ad54ac9c478abbdb@group.calendar.google.com', 'en.uk#holiday@group.v.calendar.google.com']

    

logging.basicConfig(level=logging.DEBUG)

update_t = 60 # mins
cal_draw = CalDraw()
while True:
    try:
        width = 800
        height = 480


        events, holidays = get_events(calendar_ids)
        weather = get_weather()
        
        cal_draw.draw_calendar(events, holidays)
        cal_draw.draw_weather(weather)

        # Drawing on the Horizontal image
        logging.info("1.Drawing on the Horizontal image...")
        image_black = Image.new('1', (width, height), 255)  # 255: clear the frame
        image_red = Image.new('1', (width, height), 255)  # 255: clear the frame

        logging.basicConfig(level=logging.DEBUG)
        epd = epd7in5_V2.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()

        epd.display(epd.getbuffer(cal_draw.image_black))
        time.sleep(update_t*60)

        
    except KeyboardInterrupt:
        epd.Clear()
        logging.info("ctrl + c:")
        epd7in5_V2.epdconfig.module_exit()
        exit()

    except Exception as e:
        logging.info(e)
        time.sleep(update_t * 60)
