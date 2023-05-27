# Inky Impression Weather Station

Inky Impression eInk display from Pimoroni driven by a Raspberry Pi Zero (or any other Raspberry Pi) to display a seven day weather forecast.

Based on the original work by [Rainer Bunger](https://github.com/rbunger/Inky-wHAT-Weather-Station)

![Example Screenshot](https://talktech.info/wp-content/uploads/2023/02/IMG_20230226_110708-scaled.jpg)

## Getting Weather information

The weather information is fetched from OpenWeather:

[OpenWeather](https://openweathermap.org)

Here you need to create an account and an API key. 

Put the code into a file called apikey.py 

You can use the sample file as follows

```
mv apikey.py.sample apikey.py
nano apikey.py
```

* api_key = 'your openweathermap API Key'
* lat="your latitude"
* lon="your longtitude"


## Setting up the screen

The Pimoroni Inky Impression display requires a bunch of software to be installed. My recommendation is to follow the description in a Pimoroni tutorial:

[Inky Impression](https://shop.pimoroni.com/products/inky-impression)

The installation is done by executing a bash script, and it takes a while. Everything is installed for Python 2 and 3 which isn't necessary from my point of view, so you might consider deselecting version 2 in the script before running it.

## Additional configuration

Please rename the file apikey.py.sample to apikey.py and paste in your API key from openWeatherMap.org
The Latitude and Longtitude are also now in the apikey file so that you do not accidentally share your location if you commit changes

# Running the script

There are two ways to run this code

```
python3 weather.py
```

Running this will run this application in a loop and never stop

```
python3 once.py
```

Running this will run the code, update the screen and stop. Use this version if you want to put the script in cron job.

## Running as a cron job

Run this the root cron as follows

```
sudo crontab -e
```

This will open the crontab file to be edited

```
* */6 * * * /home/pi/Inky-Impression-Weather-Station/once.py >/dev/null 2>&1
```

This example will run the update every 6 hours

## Credit

* The icons are provided by Erik Flowers.
* The font is from David Jonathan Ross.
* Original code by Rainer Bunger

## Thank you too:
Icons and code table are from Erik Flowers:

[Weather Icons](https://github.com/erikflowers/weather-icons)

For easy access to this tool, I have uploaded pre-convered images, but they are still the oringal authors work.

The font is from David Jonathan Ross:

[Bunjee](https://github.com/djrrb/bungee)


## Licensing

The weather icons and the font are licensed under [SIL OFL 1.1](http://scripts.sil.org/OFL).
