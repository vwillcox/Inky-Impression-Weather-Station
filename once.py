#!/usr/bin/python3
# -*- coding: utf-8 -*-
import copy, json,requests, pytz,time
from inky.inky_uc8159 import Inky, DESATURATED_PALETTE
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw
import io, apikey, os,signal, iconmap
import RPi.GPIO as GPIO

path = os.path.dirname(os.path.realpath(__file__))

ICON_SIZE = 100
TILE_WIDTH = 150
TILE_HEIGHT = 200
FONT_SIZE = 25
SPACE = 2
ROTATE = 0 # 180 = flip display
USE_INKY = True
SHOW_CLOCK = False
SLEEP_TIME = 3600
colours = ['Black', 'White', 'Green', 'Blue', 'Red', 'Yellow', 'Orange']
percipitation_colour = colours[0]
temp_colour = colours[4]
day_colour = colours[2]
presure_colour = colours[3]
LABELS = ['A','B','C','D']

time_colour = colours[4]

class Day:
    def __init__(self, min, max, pop, id, sunrise, sunset, pressure, dt):
        self.min = int(min + 0.5)
        self.max = int(max + 0.5)
        self.pop = pop
        self.id = id
        self.sunrise = sunrise
        self.sunset = sunset
        self.pressure = pressure
        self.dt = dt

def get_icon(name):
    return Image.open(name).convert("RGBA")


def day_lists_not_identical(days, other_days):
    if (len(days) != len(other_days)):
        return True
    for i in range(len(days)):
        if (days[i].min != other_days[i].min):
            return True
        if (days[i].max != other_days[i].max):
            return True
        if (days[i].pop != other_days[i].pop):
            return True
        if (days[i].id != other_days[i].id):
            return True
    return True


api_key = apikey.api_key
night_map = iconmap.night_map
day_map = iconmap.day_map
general_map = iconmap.general_map

if (api_key == "<your API key>"):
    print("You forgot to enter your API key")
    exit()
lat = apikey.lat
lon = apikey.lon
url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=hourly&appid=%s&units=metric" % (
    lat, lon, api_key)

palette_colors = [(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0) for c in DESATURATED_PALETTE[2:6] + [(0, 0, 0)]]

tile_positions = []
for i in range(2):
    for j in range(4):
        tile_positions.append((j * TILE_WIDTH, i * TILE_HEIGHT))

inky_display = Inky()
satuation = 0


y_top = int(inky_display.height)
y_bottom = y_top + int(inky_display.height * (4.0 / 10.0))

font = ImageFont.truetype(path+
    "/fonts/BungeeColor-Regular_colr_Windows.ttf", FONT_SIZE)

old_days = []


try:
    response = requests.get(url)
    data = json.loads(response.text)
except:
    None

days = []
daily = data["daily"]
for day in daily:
    min = day["temp"]["min"]
    max = day["temp"]["max"]
    pop = day["pop"]
    id = day["weather"][0]["id"]
    sunrise = int(day["sunrise"])
    sunset = int(day["sunset"])
    dt = int(day["dt"])
    pressure = int(day["pressure"])
    days.append(Day(min, max, pop, id, sunrise, sunset, pressure, dt))
if (day_lists_not_identical(days, old_days)):
    old_days = copy.deepcopy(days)
    img = Image.new("RGBA", inky_display.resolution, colours[1])
    draw = ImageDraw.Draw(img)
    for i in range(8):
       name = path+"/icons/wi-"
       if (i == 0):
           t = int(time.time())
           if (t < days[i].sunset):
               name += day_map[days[i].id]
           else:
               name += night_map[days[i].id]
       else:
           name += general_map[days[i].id]
       icon = get_icon(name)
       x = tile_positions[i][0] + (TILE_WIDTH - ICON_SIZE) // 2
       y = tile_positions[i][1]
       img.paste(icon, (x, y))
       text = str(int(100 * days[i].pop)) + "%"
       w, h = font.getsize(text)
       x = tile_positions[i][0] + (TILE_WIDTH - w) // 2
       y = tile_positions[i][1] + ICON_SIZE + SPACE
       draw.text((x, y), text, percipitation_colour, font)
       text = str(days[i].min) + "°"
       measuretext = str(days[i].min) + "°|" + str(days[i].max) + "°"
       w, h = font.getsize(measuretext)
       x = tile_positions[i][0] + (TILE_WIDTH - w) // 2
       y += FONT_SIZE
       draw.text((x, y), text, colours[3], font)
       text = str(days[i].max) + "°"
       #w, h = font.getsize(text)
       #y += FONT_SIZE
       #x += x+ font.getsize(maxtem)
       print(x)
       x+=45
       draw.text((x, y), "    " + text, colours[4], font)
       press = str(days[i].pressure)
       text = str(press)+"hPa"
       w, h = font.getsize(text)
       x = tile_positions[i][0] + (TILE_WIDTH - w) // 2
       y += FONT_SIZE
       draw.text((x, y), text, presure_colour, font)
       ts = time.gmtime(days[i].dt)
       day_name = time.strftime("%a", ts)
       text = day_name
       w, h = font.getsize(text)
       x = tile_positions[i][0] + (TILE_WIDTH - w) // 2
       y += FONT_SIZE
       draw.text((x, y), text, day_colour, font)
       img.rotate(180)
    inky_display.set_border(colours[4])
    inky_display.set_image(img.rotate(ROTATE), saturation=0)
    inky_display.show()
  
