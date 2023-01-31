#!/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import print_function


import json
import sys
import os

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'RaspberryPi_JetsonNano', 'python',
                 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'RaspberryPi_JetsonNano', 'python',
                 'lib')


if os.path.exists(libdir):
    sys.path.append(libdir)



from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone

from dateutil.parser import parse
from datetime import timedelta
import pytz

class CalDraw():

    def __init__(self):

        self.width = 800
        self.height = 480

        self.day_w = 199
        self.day_h = 238
        self.cal_x = 1
        self.cal_y = 1
        self.title_h = 67
        self.event_h = 28

        font = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts', 'l-sans', 'lucidasansdemibold.ttf')
        big_size = 40
        self.big_font = ImageFont.truetype(os.path.join(picdir, font), big_size)

        day_size = 32
        self.day_font = ImageFont.truetype(os.path.join(picdir, font), day_size)

        event_size = 27
        self.event_font = ImageFont.truetype(os.path.join(picdir, font), event_size)

        tiny_size = 12
        self.tiny_font = ImageFont.truetype(os.path.join(picdir, font), tiny_size)

        self.image_black = Image.new('1', (self.width, self.height), 255)  # 255: clear the frame
        self.image_red = Image.new('1', (self.width, self.height), 255)  # 255: clear the frame
    
    def format_time(self, time):
        if time < 10:
            return '0' + str(time)
        else:
            return str(time)

    def add_events(self, events, event_counts, holidays = False):


        london_tz = pytz.timezone('Europe/London')
        now = datetime.now().astimezone(london_tz)

        now = now.replace(hour=00, minute=00)

        draw_black = ImageDraw.Draw(self.image_black)
        max_length = 13
        for event in events:

            start = parse(event['start']).astimezone(london_tz)
            end = parse(event['end']).astimezone(london_tz)


            # if event more than a week in the future we can break
            if start - now > timedelta(days=7):
                break
            else:
                d = start - now

                diff = d.days
                if diff < 4:
                    pos_x = self.cal_x + diff * self.day_w - 6
                    pos_y = self.cal_y + self.title_h + 1 + event_counts[diff] * self.event_h
                else:
                    pos_x = self.cal_x + (diff-4) * self.day_w - 6
                    pos_y = self.cal_y + self.title_h + 1 + event_counts[diff] * self.event_h + self.day_h


                if not holidays:

                    draw_black.text((pos_x, pos_y),
                                ' {0}\n   {1}:{2}-{3}:{4}'.format(event['name'][:max_length], self.format_time(start.hour), self.format_time(start.minute), self.format_time(end.hour),self.format_time(end.minute)),
                                font=self.event_font)
                    event_counts[diff] += 2
                else:
                    draw_black.text((pos_x, pos_y),
                                    '{}'.format(event['name'][:max_length]),
                                    font=self.event_font)
                    event_counts[diff] += 1

        return event_counts


    def draw_calendar(self, events, holidays):
        # Returns the current local date
        london_tz = pytz.timezone('Europe/London')
        now = datetime.now().astimezone(london_tz)

        weekdays = ['Mon','Tue','Wed','Thu','Fri','Sat', 'Sun']
        months = ['Jan', 'Feb', 'March', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        draw_black = ImageDraw.Draw(self.image_black)


        linewidth = 1
        for i in range(7):

            day_ind = (i+now.weekday())%7
            day = weekdays[day_ind]
            new_date = now + timedelta(days = i)
            if i < 4:
                draw_black.rectangle((self.cal_x+i*self.day_w, self.cal_y, self.cal_x+(i+1)*self.day_w, self.cal_y+self.day_h), fill=1, outline=0, width = linewidth)
                draw_black.rectangle((self.cal_x+i*self.day_w, self.cal_y, self.cal_x+(i+1)*self.day_w, self.cal_y+self.title_h), fill=1, outline=0, width = linewidth)
                
                
                draw_black.text((self.cal_x+i*self.day_w, self.cal_y -3),' {1}\n {0}'.format(day, new_date.day),font = self.day_font)

            else:
                print((self.cal_x+(i-4)*self.day_w, self.cal_y + self.day_h, self.cal_x+(i-3)*self.day_w, self.cal_y+self.day_h))
                draw_black.rectangle((self.cal_x+(i-4)*self.day_w, self.cal_y + self.day_h, self.cal_x+(i-3)*self.day_w, self.cal_y+2*self.day_h), fill=1, outline=0, width = linewidth)
                draw_black.rectangle((self.cal_x+(i-4)*self.day_w, self.cal_y + self.day_h, self.cal_x+(i-3)*self.day_w, self.cal_y+self.day_h+self.title_h), fill=1, outline=0, width = linewidth)

                draw_black.text((self.cal_x+(i-4)*self.day_w, self.cal_y + self.day_h -3),' {1}\n {0}'.format(day, new_date.day),font = self.day_font)

        i = 7
        draw_black.text((self.cal_x+(i-4)*self.day_w+50, self.cal_y + self.day_h + 50),
                        '{}\n{} {}\n{}'.format(weekdays[now.weekday()], now.day, months[now.month - 1], now.year),
                        font=self.big_font)

        draw_black.text((767, 467),
                        '{}{}'.format(now.hour, now.minute),
                        font=self.tiny_font)

        event_counts = [0]*7
        event_counts = self.add_events(holidays, event_counts, holidays=True)
        event_counts = self.add_events(events, event_counts)




    def draw_weather(self, weather):

        print(weather)

        draw_black = ImageDraw.Draw(self.image_black)

        weather_ids = {'Clear': '01','clear sky': '01', 'few clouds': '02', 'scattered clouds': '03', 'broken clouds': '03',
                       'overcast clouds': '03', 'Drizzle': '09',
                       'Rain': '10', 'Thunderstorm': '11', 'Snow': '13', 'Mist': '03', 'Smoke': '03', 'Haze': '03',
                       'Dust': '03', 'Fog': '03',
                       'Sand': '03', 'Ash': '03', 'Squall': '03', 'Tornado': '03', 'light rain': '10',
                       'moderate rain': '10', 'heavy intensity rain': '10',
                       'very heavy rain': '10', 'extreme rain': '10', 'freezing rain': '13',
                       'light intensity shower rain': '09', 'shower rain': '09',
                       'heavy intensity shower rain': '09', 'ragged shower rain': '09'}

        for i in range(7):

            weather_img = Image.open('./images/weather_type_icons/' + weather_ids[weather[i]['description']] + '.png').convert('P')
            if i < 4:
                size = (int(weather_img.width * (self.title_h-4)/weather_img.height),self.title_h - 4)
                coord = (self.cal_x+i*self.day_w+int(self.day_w*1/2.5), self.cal_y + 2)


            else:
                size = (int(weather_img.width * (self.title_h-4)/weather_img.height) ,self.title_h - 4)
                coord = (self.cal_x+(i-4)*self.day_w+ int(self.day_w*1/2.5), self.cal_y + self.day_h + 2)




            weather_img = weather_img.resize(size)
            self.image_black.paste(weather_img, coord)

            draw_black.text((coord[0] + 79, coord[1] - 4),
                            '{0}\n{1}'.format(round(weather[i]['max_temp']), round(weather[i]['min_temp'])), font=self.day_font)


if __name__ == '__main__':

    events = json.load(open('data/events.json', 'r'))
    holidays = json.load(open('data/holidays.json', 'r'))
    weather = json.load(open('data/weather.json', 'r'))

    cal_draw = CalDraw()
    cal_draw.draw_calendar(events, holidays)
    cal_draw.draw_weather(weather)
    cal_draw.image_black.save('images/image_black.png')
    cal_draw.image_red.save('images/image_red.png')
    # epd.display(epd.getbuffer(image_black),epd.getbuffer(image_red))
    # time.sleep(2)