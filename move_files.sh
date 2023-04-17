#!/bin/bash

# script moves all png files from a folder to a new folder named 'cam' and 
# the 'log.csv' file to a new folder named 'logs' with a new name 'raw.csv'

# Get the label parameter from the command line
label="${1:-sqr_01}"

# Create a new directory named "cam" inside the given label folder
mkdir "data/$label/cam"

# Move all PNG files from the given label folder to the "cam" directory
#mv "data/$label/*.png" "data/$label/cam/"
find data/$label -maxdepth 1 -type f -name '*.png' -exec mv {} data/$label/cam \;

# Create a new directory named "logs" inside the given label folder
mkdir "data/$label/logs"

# Move all csv file from the given label folder to the "logs" directory
mv "data/$label/log.csv" "data/$label/logs/raw.csv"
