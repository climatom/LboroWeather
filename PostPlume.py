#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 11:54:05 2018

@author: gytm3
"""
from pylab import*
import urllib2
import numpy as np
import re
import pandas as pd
import requests
import time as ptime
from datetime import datetime

#=============================================================================#
# Parameters 
#=============================================================================#
url="http://158.125.175.200/?command=NewestRecord&table=Public"
url_post="http://plumeplotter.com/newhurst/obs.php"
freq=20. # Seconds to scan - should factor in to 60
post_freq=120 # Seconds to send - any frequency. 
#=============================================================================#

#=============================================================================#
# Functions
#=============================================================================#
def getWeather():
    response = urllib2.urlopen(url)
    html = response.readlines(); n=len(html)-3
    temp=np.float(re.search("td>(.*)</td",html[8]).group(1))
    rh=np.float(re.search("td>(.*)</td",html[9]).group(1))
    ws=np.float(re.search("td>(.*)</td",html[19]).group(1))
    wdir=np.float(re.search("td>(.*)</td",html[18]).group(1))
    solar=np.float(re.search("td>(.*)</td",html[21]).group(1))*1000.
    net=np.float(re.search("td>(.*)</td",html[23]).group(1))
    press=np.float(re.search("td>(.*)</td",html[26]).group(1))
    time=re.search("</b>(.*)<br",html[6]).group(1)
    
    response.close()
    return temp,rh,ws,wdir,solar,net,press,time

def meanDir(u,v):
    mu_dir=np.degrees(np.arctan2(u,v))+180
    return mu_dir

def postData(ws,wdir):
    tstamp="%s"%datetime.now()
    topost = {"key": "319274", "obs":"%s,%.2f,%.2f" %(tstamp,ws,wdir)}
    resp = requests.post(url_post, params=topost)
    return resp
#=============================================================================#

#=============================================================================#
# MAIN
#=============================================================================#

# Run continuous while loop to retrieve data every 20 seconds. 
# Note that we: 
# - store data every 20 seconds
# - take a running average of the last 180 measurements (1 hour)
# - send the running average every 2 minutes 
## NB. We can avoid the need to purge by overwriting the hour's array: 
## pseudo-code: if ii >179; ii=0; data[ii,0]=wspd; data[ii,1]=wdir; ii+=1

# Preallocate the "hour" array: 
hourData=np.zeros((np.int(60*60/freq),3)) * np.nan

# Loop 
ii=0
last_send=datetime.now()
while True: 
    # Get Weather
    temp,rh,ws,wdir,solar,net,press,time = getWeather()
    
    # Convert to U/V format
    u=-ws*np.sin(np.radians(wdir))
    v=-ws*np.cos(np.radians(wdir))
    hourData[ii,0]=ws; hourData[ii,1]=u; hourData[ii,2]=v
    
    # Compute mean magnitude
    mu_mag=np.nanmean(hourData,axis=0) # mean speed, mean u, mean v
    
    # Compute mean direction
    mu_dir=meanDir(mu_mag[1],mu_mag[2])
    
    # Deal with indexing 
    if ii == (len(hourData)-1): ii=0
    else: ii +=1 
    
    # If we haven't posted in at least post_freq seconds, post now...
    dt=(datetime.now()-last_send).total_seconds()
    if dt >= post_freq: 
        postData(mu_mag[0],mu_dir); last_send=datetime.now()
        print "Sent data at %s [mean speed = %.2f; mean dir=%.2f. Average of %.0f obs]" % \
        (last_send, mu_mag[0],mu_dir,np.sum(~np.isnan(hourData[:,0])))
    
    # Sleep until next call
    ptime.sleep(freq)
    




