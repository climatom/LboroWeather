#!/bin/bash

# Exectute Python program to grab the latest Met Data. 
/home/lunet/gytm3/anaconda2/bin/python /home/lunet/gytm3/LboroWeather/campusMet.py

# Git: add and commit changes
cd /home/lunet/gytm3/LboroWeather && /usr/bin/git commit -a -m "15 min Campus Met Update... `date`"

# Send data to Git server
cd /home/lunet/gytm3/LboroWeather && /usr/bin/git push https://climatom:G3j18Rbp@github.com/climatom/LboroWeather.git

