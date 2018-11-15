#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import os, os.path, csv

aprs_wx_active_station = "https://aprs.link/app/aprs/listings/activewx"

response = requests.get(aprs_wx_active_station)
soup = BeautifulSoup(response.text, "html.parser")
print("<?xml version=\"1.0\" encoding=\"UTF-8\"?><kml xmlns=\"http://earth.google.com/kml/2.1\"><Document id=\"aprs\">")

for rows in soup.find_all("tr"):
    cols = rows.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    if cols[0] not in ['Callsign'] and cols[2] not in ['n/a']:
        wx_station = cols[0]
        latitude,longitude = cols[2].split(' ')
        latd,latm,lats = latitude.split('.')
        lond,lonm,lons = longitude.split('.')
        ilons=lons[0:2]
        ilats=lats  [0:2]
        latitudedd = (float(latd))+(float(latm)/60)+(float(ilats)/3600)
        longitudedd = (float(lond))+(float(lonm)/60)+(float(ilons)/3600)
        if lons[2:3] in "W":
            longitudedd=longitudedd*-1
        if lats[2:3] in "S":
            latitudedd=latitudedd*-1
        print("<Placemark><name>"+wx_station+"</name><styleUrl>http://aprs.fi/s1/f24/p5fp5f.png</styleUrl><description> [[http://www.findu.com/cgi-bin/wxpage.cgi?call="+wx_station+"]] [[https://aprs.fi/weather/a/"+wx_station+"]]</description><MultiGeometry><Point><coordinates>"+str(longitudedd)+","+str(latitudedd)+",0</coordinates></Point></MultiGeometry></Placemark>")
print("</Document></kml>")
