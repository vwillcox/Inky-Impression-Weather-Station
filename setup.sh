cd icons
7za x erik_flowers_weather-icons.7z
find -name "*.svg" -exec vim -s script.vim {} \;
mogrify -background white -format PNG8 *.svg
#rm *.svg
