# Inky-wHAT-Weather-Station

Inky wHAT e-ink display driven by a Raspberry Pi Zero (or any other Raspberry Pi).

![Display Preview](http://i.imgur.com/Ed5dWCQ.png)

Icons are from Erik Flowers (GitHub):

[Weather Icons](https://github.com/erikflowers/weather-icons)

The weather information is fetched from OpenWeather:

[OpenWeather](https://openweathermap.org)

Here you need to create an account and an API key. Put the code into the "weather.py" file ("api_key" variable). You also need to set your position ("lat" and "lon" variables).

## Setup

The Pimoroni Inky wHAT display requires a bunch of software to be installed. My recommendation is to follow the description in a corresponding tutorial:

[Getting Started with Inky wHAT](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-what)

We need to convert Erik's icons to 8 bit PNGs. We use the Imagemagick "mogrify" command for the bulk convert. This would give 8 bit PNGs with a 30 x 30 pixel resolution with Erik's original SVGs. But for the weather display we need larger icons. I have chosen 95 x 95 pixels. My approach was to give widths and heights in the SVG files. So I run a Vim script over all the SVGs in the icons folder. The original SVGs are stored in a 7z-file in the "icons" folder. In the install script "install.sh" there a line to remove the converted SVGs after PNG creation but the line is commented out for security reasons.

The main Python file to drive the display is "weather.py".

Here is the contents of the install script (last line commented out):

```
cd icons
7za x erik_flowers_weather-icons.7z
find -name "*.svg" -exec vim -s script.vim {} \;
mogrify -background white -format PNG8 *.svg
#rm *.svg
```

## Credit

The icons are provided by Erik Flowers.

## Licensing

* Erik's weather icons are licensed under [SIL OFL 1.1](http://scripts.sil.org/OFL).
* Font: [Bunjee](https://github.com/djrrb/bungee).
