#!/usr/bin/python3
# -*- coding: utf-8 -*-

# GPS CODE SOURCE = https://www.developpez.net/forums/d1868942/autres-langages/python/contribuez/distance-entre-2-lieux-connus-leurs-coordonnees-gps/#post11657860


"""
Source pour le calcul:
https://geodesie.ign.fr/contenu/fichiers/Distance_longitude_latitude.pdf

sudo apt-get install python-matplotlib
https://stackoverflow.com/questions/18625085/how-to-plot-a-wav-file
sudo pip3 install utils xsmtplib

"""


import ConfigParser
from math import sin, cos, acos, pi
import urllib2
import json
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import smtplib

config = ConfigParser.ConfigParser()
config.readfp(open(r'config.ini'))

gmail_ifsend = config.get('EMAIL', 'EMAIL_SEND')
gmail_server = config.get('EMAIL', 'EMAIL_SERVER')
gmail_port = config.get('EMAIL', 'EMAIL_PORT')
gmail_user = config.get('EMAIL', 'EMAIL_USER')
gmail_password = config.get('EMAIL', 'EMAIL_PASSWORD')
gmail_send_email_to = config.get('EMAIL', 'EMAIL_1')
gmail_send_email_to_2 = config.get('EMAIL', 'EMAIL_2')
gmail_title = config.get('EMAIL', 'EMAIL_TITLE')


radius = config.get('GPS', 'RADIUS')
LAT_HOME = config.get('GPS', 'LATITUDE')
LONG_HOME = config.get('GPS', 'LONGITUDE')

interval = config.get('OTHER', 'UPDATE_INTERVAL')

triggered = 0
emailsend = 0


sent_from = gmail_user
to = [gmail_send_email_to, gmail_send_email_to_2]
subject = gmail_title
body = ' '

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)


#############################################################################
def dms2dd(d, m, s):
    """Convertit un angle "degrÃ©s minutes secondes" en "degrÃ©s dÃ©cimaux"
    """
    return d + m/60 + s/3600

#############################################################################
def dd2dms(dd):
    """Convertit un angle "degrÃ©s dÃ©cimaux" en "degrÃ©s minutes secondes"
    """
    d = int(dd)
    x = (dd-d)*60
    m = int(x)
    s = (x-m)*60
    return d, m, s

#############################################################################
def deg2rad(dd):
    """Convertit un angle "degrÃ©s dÃ©cimaux" en "radians"
    """
    return dd/180*pi

#############################################################################
def rad2deg(rd):
    """Convertit un angle "radians" en "degrÃ©s dÃ©cimaux"
    """
    return rd/pi*180

#############################################################################
def distanceGPS(latA, longA, latB, longB):
    """Retourne la distance en mÃ¨tres entre les 2 points A et B connus grÃ¢ce Ã 
       leurs coordonnÃ©es GPS (en radians).
    """
    # Rayon de la terre en mÃ¨tres (sphÃ¨re IAG-GRS80)
    RT = 6378137
    # angle en radians entre les 2 points
    S = acos(sin(latA)*sin(latB) + cos(latA)*cos(latB)*cos(abs(longB-longA)))
    # distance entre les 2 points, comptÃ©e sur un arc de grand cercle
    return S*RT

#############################################################################
if __name__ == "__main__":
    while True:
        latA = deg2rad(float(LAT_HOME)) # Nord
        longA = deg2rad(float(LONG_HOME)) # Est


	req = urllib2.Request("http://api.open-notify.org/iss-now.json")
	response = urllib2.urlopen(req)

	obj = json.loads(response.read())

        latB = deg2rad(float(obj['iss_position']['latitude'])) # Nord
        longB = deg2rad(float(obj['iss_position']['longitude'])) # Est


        dist = distanceGPS(latA, longA, latB, longB)
	print("---")


	if int(dist/1000) < float(radius):
	    print("YES")
	    triggered = 1
	    if emailsend == 0:
		if float(gmail_ifsend) == 1:
		    print("SEND EMAIL")
	            try:
    		        server = smtplib.SMTP_SSL(gmail_password, gmail_port)
    		        server.ehlo()
    		        server.login(gmail_user, gmail_password)
    		        server.sendmail(sent_from, to, email_text)
    		        server.close()

    	 	        print 'Email sent!'
	            except:
    		        print 'Something went wrong...'
		    emailsend = 1
	else:
	    print("NO")
	    triggered = 0
	    emailsend = 0
        dist = dist/1000
        print dist+'km'
        time.sleep(float(interval))
