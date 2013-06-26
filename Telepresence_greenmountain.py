#!/usr/bin/python

import os,sys
import RPi.GPIO as GPIO
import time

import ConfigParser
import getopt
import os
import sys
import twitter

adafruit_path = '/home/pi/keurig_rpi/Adafruit_PWM_Servo_Driver'
sys.path.append(adafruit_path)
print adafruit_path

spacebrew_path = '/home/pi/keurig_rpi/pySpacebrew'
sys.path.append(spacebrew_path)
print spacebrew_path

from spacebrew import Spacebrew

led1 = 0
led0 = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)


#Twitter Stuff
consumer_key = "Dnminp2VUN91nrRbUMy4Q"
consumer_secret = "u1UnbxgHYyOYXYJ5CJoiUs80H3fSTVKGkNzeKUn2CA"

access_key = "1510848594-pyP3fxZptsQAWLQhq0FgMI8xP4U9rv9aV231rAo"
access_secret = "CBaiyVdhoUTdDVUVVWmKPstYFXBo0vQIjEg2TnyFdiw"


# ===========================
# CREATE SPACEBREW AND SUBSCRIBE
# =========================
brew_array = Spacebrew("keurig", server="spacebrew.madsci1.havasworldwide.com")

#CREATE SUBSCRIBERS
brew_array.addSubscriber("button_1","boolean")
brew_array.addSubscriber("button_0","boolean")

brew_array.addPublisher("led_1", "boolean")
brew_array.addPublisher("led_0", "boolean")


# =========================
# SPACEBREW EVENT HANDLERS
# =========================

def led_0(value):
  print "LED0 : "
  print value

def led_1(value):
  print "LED1 : "
  print value

def button_0(value):
  print "button 0"
  print value
  if value == "true":
    print "HIGH"
    GPIO.output(24, GPIO.HIGH)
    time.sleep(1)
    print "LOW"
    GPIO.output(24, GPIO.LOW)
 
def button_1(value):
  print "button 1"
  print value 
  if value == true:
    GPIO.output(25, GPIO.HIGH)
    time.sleep(.5)
    GPIO.output(25, GPIO.LOW)


# TWITTER
def tweet_coffee(message):


  api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                    access_token_key=access_key, access_token_secret=access_secret,
                    input_encoding=None)

  try:
    status = api.PostUpdate(message)

  except UnicodeDecodeError:
    print "Your message could not be encoded.  Perhaps it contains non-ASCII characters? "
    print "Try explicitly specifying the encoding with the --encoding flag"
    sys.exit(2)
  print "%s just posted: %s" % (status.user.name, status.text)


# ==========
# Subscribe
# ==========
brew_array.subscribe("button_0", button_0);
brew_array.subscribe("button_1", button_1);

brew_array.start()


# =======================
#INIT STATE VALUES
# =======================

#Initialise the PWM device using the default address

#Init switches
#for i in range(0,3):
#  GPIO.output(arrSwitchPins[i], GPIO.HIGH)

CUR8OZ = 0
COUNT8OZ = 0

CUR16OZ = 0
COUNT16OZ = 0

while (True):

  if GPIO.input(18) != led0:

    led0 = GPIO.input(18)
    #print bool(led0)
    brew_array.publish("led_0", ("false" if bool(led0) else "true"))


  if GPIO.input(23) != led1:

    led1 = GPIO.input(23)
    #print bool(led1)
    brew_array.publish("led_1", ("false" if bool(led1) else "true"))
