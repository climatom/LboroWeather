# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from pylab import*
import urllib.request as urllib2
import numpy as np
import re
import pandas as pd
import os
import requests

#======================================================================#
# Params
#======================================================================]
url="http://158.125.175.200/?command=TableDisplay&table=Met1&records=24"
logfile="/home/lunet/gytm3/LboroWeather/campus_log.txt"
cols=["T","RH","WS","SOL","RAIN","PRESS"]
#======================================================================#

response = urllib2.urlopen(url)
html = response.readlines(); n=len(html)-3
heads=[re.search("p>(.*)</t",ii).group(1) for ii in html[7:25]]

# Now extract (if possible)
try:
    time=[re.search("p>(.*)</t",ii).group(1) for ii in html[27:n:20]]
    temp=[re.search("p>(.*)</t",ii).group(1) for ii in html[29:n:20]]
    rh=[re.search("p>(.*)</t",ii).group(1) for ii in html[30:n:20]]
    ws=[re.search("p>(.*)</t",ii).group(1) for ii in html[36:n:20]]
    sun=[re.search("p>(.*)</t",ii).group(1) for ii in html[39:n:20]]
    rain=[re.search("p>(.*)</t",ii).group(1) for ii in html[43:n:20]]
    press=[re.search("p>(.*)</t",ii).group(1) for ii in html[44:n:20]]

    # Error check!
    assert len(time)==len(temp),"Mismatch in time/temp lengths!"
    
except: 
    with open("latest_error.txt","w") as f: 
        f.write("Failed!"); exit()

# Put in data frame - and ensure that it's "time-aware"
data=pd.DataFrame(data=np.array([temp,rh,ws,sun,rain,press]).T,\
                  columns=cols,dtype=np.float32)
data["datetime"]=pd.to_datetime(time)
data.set_index("datetime",inplace=True)

# try to read in "campus_log.txt"
if os.path.isfile(logfile):
    old=pd.read_csv(logfile,sep="\t")
    old.set_index("datetime",inplace=True)  
    out=old.append(data[data.index>old.index[-1]])
    out.to_csv(logfile,sep="\t",\
               float_format="%.3f")

else: 
    data.to_csv(logfile,sep="\t",\
               float_format="%.3f")


