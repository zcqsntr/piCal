#!/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import print_function


import json
import sys
import os

picdir = os.path.join(os.path.join(
    os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'RaspberryPi_JetsonNano', 'python',
                 'pic')))
libdir = os.path.join(os.path.join(
    os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'RaspberryPi_JetsonNano', 'python',
                 'lib')))
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
#from waveshare_epd import epd7in5b_V2
from waveshare_epd import epd7in5_V2

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone

from dateutil.parser import parse
from datetime import timedelta
import pytz

import time

def add_events(draw_black, events, event_counts, event_font, cal_pos, day_shape, event_h, title_h, holidays = False):
    cal_x, cal_y = cal_pos
    day_w, day_h = day_shape

    london_tz = pytz.timezone('Europe/London')
    now = datetime.now().astimezone(london_tz)



    for event in events:

        start = parse(event['start']).astimezone(london_tz)
        end = parse(event['end']).astimezone(london_tz)

        print(event['name'])
        # if event more than a week in the future we can break
        if start - now > timedelta(days=7):
            break
        else:
            d = start - now

            diff = d.days
            if diff < 4:
                pos_x = cal_x + diff * day_w + 1
                pos_y = cal_y + title_h + 1 + event_counts[diff] * event_h
            else:
                pos_x = cal_x + (diff-4) * day_w + 1
                pos_y = cal_y + title_h + 1 + event_counts[diff] * event_h + day_h
                

            if not holidays:
                print(start.hour)
                draw_black.text((pos_x, pos_y),
                            '{1}:{2}-{3}:{4} \n   {0}'.format(event['name'], start.hour, start.minute, end.hour, end.minute),
                            font=event_font)
                event_counts[diff] += 2
            else:
                draw_black.text((pos_x, pos_y),
                                '{}'.format(event['name']),
                                font=event_font)
                event_counts[diff] += 1




    return event_counts


def draw_calendar(image_black, image_red, events, holidays):
    # Returns the current local date
    london_tz = pytz.timezone('Europe/London')
    now = datetime.now().astimezone(london_tz)

    weekdays = ['Mon','Tue','Wed','Thu','Fri','Sat', 'Sun']
    months = ['Jan', 'Feb', 'March', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    draw_black = ImageDraw.Draw(image_black)

    day_w = 199
    day_h = day_w
    cal_x = 0
    cal_y = 50
    title_h = 35
    event_h = 35

    big_size = 36
    big_font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), big_size)

    day_size = 18
    day_font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), day_size)

    event_size = 16
    event_font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), event_size)

    draw_black.text((0, 0), '{} {} {} {}'.format(weekdays[now.weekday()], now.day, months[now.month-1], now.year), font=big_font)


    for i in range(7):

        day_ind = (i+now.weekday())%7
        day = weekdays[day_ind]
        if i < 4:
            draw_black.rectangle((cal_x+i*day_w, cal_y, cal_x+(i+1)*day_w, cal_y+day_h), fill=1, outline=0)
            draw_black.rectangle((cal_x+i*day_w, cal_y, cal_x+(i+1)*day_w, cal_y+title_h), fill=1, outline=0)
            draw_black.text((cal_x+i*day_w+25, cal_y),'{}  {}'.format(day, now.day + i),font = day_font)
            
        else:
            print((cal_x+(i-4)*day_w, cal_y + day_h, cal_x+(i-3)*day_w, cal_y+day_h))
            draw_black.rectangle((cal_x+(i-4)*day_w, cal_y + day_h, cal_x+(i-3)*day_w, cal_y+2*day_h), fill=1, outline=0)
            
            draw_black.rectangle((cal_x+(i-4)*day_w, cal_y + day_h, cal_x+(i-3)*day_w, cal_y+day_h+title_h), fill=1, outline=0)
            
            draw_black.text((cal_x+(i-4)*day_w+25, cal_y + day_h),'{}  {}'.format(day, now.day + i),font = day_font)
            

    event_counts = [0]*7
    event_counts = add_events(draw_black, holidays, event_counts, event_font, (cal_x, cal_y), (day_w,day_h), event_h, title_h,
                              holidays=True)
    event_counts = add_events(draw_black, events, event_counts, event_font, (cal_x, cal_y), (day_w,day_h), event_h, title_h)



    return image_black, image_red


font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
width = 800
height = 480

events = json.load(open('data/events.json', 'r'))
holidays = json.load(open('data/holidays.json', 'r'))
# Drawing on the Horizontal image
logging.info("1.Drawing on the Horizontal image...")
image_black = Image.new('1', (width, height), 255)  # 255: clear the frame
image_red = Image.new('1', (width, height), 255)  # 255: clear the frame

# draw_black.text((10, 0), 'hello world', font=font24, fill=0)
# draw_black.text((10, 20), '7.5inch e-Paper', font=font24, fill=0)
# draw_black.text((150, 0), u'微雪电子', font=font24, fill=0)
# draw_black.line((140, 75, 190, 75), fill=0)
# draw_black.arc((140, 50, 190, 100), 0, 360, fill=0)
# draw_black.chord((200, 50, 250, 100), 0, 360, fill=0)
# Drawing on the Horizontal image
logging.basicConfig(level=logging.DEBUG)
epd = epd7in5_V2.EPD()
logging.info("init and Clear")
epd.init()
epd.Clear()






image_black, image_red = draw_calendar(image_black, image_red, events, holidays)


epd.display(epd.getbuffer(image_black))
time.sleep(10)
#epd.Clear()

image_black.save('images/image_black.png')
image_red.save('images/image_red.png')
# epd.display(epd.getbuffer(image_black),epd.getbuffer(image_red))
# time.sleep(2)