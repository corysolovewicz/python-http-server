#!/bin/bash

#
# this script is meant to be called from the root directory of the project
# and requires imagemagick to be installed 
# this script takes a single argument $1 which is used as the filename for the output file
# a random 6 digit code is generated for the google verificatio code
# and the current time is used for the time stamps on the screenshot 
# files are written to the images directory 
# and lastly any extra exifdata is removed using exiftool
# to test the script call from the project folder root > ./spoof/iMessage_1.sh <filename>
# example: ./spoof/iMessage_1.sh IMG_9876.png
# 
# remove all exifdata from images in a directory
# exiftool -all:all= -overwrite_original -r <directory>
#

DIRECTORY='./images/'
EXTENSION='.png'
BLANK_TEMPLATE_PATH='./spoof/templates/ios/iMessage_1.png'
REGULAR_FONT_PATH='./spoof/fonts/SF-Pro-Text-Regular.otf'
SEMIBOLD_FONT_PATH='./spoof/fonts/SF-Pro-Text-Semibold.otf'

# placement here is as close as it will get while matching the font. 
#convert $BLANK_TEMPLATE_PATH -font $REGULAR_FONT_PATH -pointsize 49 -fill black -gravity center -annotate -355-647 "G-$(shuf -i 100000-999999 -n 1)" $DIRECTORY$1

#convert $DIRECTORY$1 -font $SEMIBOLD_FONT_PATH -pointsize 45 -fill black -gravity northeast -annotate +956+42 "$(date '+%_I:%M')" $DIRECTORY$1

#convert $DIRECTORY$1 -font $REGULAR_FONT_PATH -pointsize 34 -fill '#848486' -gravity center -annotate +0-747 "Today $(date '+%_I:%M %p')" $DIRECTORY$1

# one liner
convert $BLANK_TEMPLATE_PATH \
        \( -font $REGULAR_FONT_PATH -pointsize 49 -fill black -gravity center -annotate -355-647 "G-$(shuf -i 100000-999999 -n 1)" \) \
        \( -font $SEMIBOLD_FONT_PATH -pointsize 45 -fill black -gravity northeast -annotate +956+42 "$(date '+%_I:%M')" \) \
        \( -font $REGULAR_FONT_PATH -pointsize 34 -fill '#848486' -gravity center -annotate +0-747 "Today $(date '+%_I:%M %p')" \) \
        -flatten $DIRECTORY$1 && exiftool -all:all= -overwrite_original -q $DIRECTORY$1