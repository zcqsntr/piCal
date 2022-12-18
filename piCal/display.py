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
events, holidays = get_events(calendar_ids)
weather = get_weather()
print(events, holidays, weather)
    

logging.basicConfig(level=logging.DEBUG)



try:
    logging.info("epd7in5b_V2 Demo")

    epd = epd7in5_V2.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    # Drawing on the Horizontal image
    logging.info("1.Drawing on the Horizontal image...")
    image_black = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    image_red = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw_Himage = ImageDraw.Draw(image_black)
    draw_other = ImageDraw.Draw(image_red)
    draw_Himage.text((10, 0), 'hello world', font = font24, fill = 0)
    draw_Himage.text((10, 20), '7.5inch e-Paper', font = font24, fill = 0)
    draw_Himage.text((150, 0), u'微雪电子', font = font24, fill = 0)    
    draw_other.line((20, 50, 70, 100), fill = 0)
    draw_other.line((70, 50, 20, 100), fill = 0)
    draw_other.rectangle((20, 50, 70, 100), outline = 0)
    draw_other.line((165, 50, 165, 100), fill = 0)
    draw_Himage.line((140, 75, 190, 75), fill = 0)
    draw_Himage.arc((140, 50, 190, 100), 0, 360, fill = 0)
    draw_Himage.rectangle((80, 50, 130, 100), fill = 0)
    draw_Himage.chord((200, 50, 250, 100), 0, 360, fill = 0)
    image_black.save('./image_black.png')
    image_red.save('./image_red.png')
    #epd.display(epd.getbuffer(image_black),epd.getbuffer(image_red))
    #time.sleep(2)




    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5b_V2.epdconfig.module_exit()
    exit()
