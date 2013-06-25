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
led2 = 0

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
brew_array.addSubscriber("button_2","boolean")

brew_array.addPublisher("led_1", "boolean")
brew_array.addPublisher("led_2", "boolean")


# =========================
# SPACEBREW EVENT HANDLERS
# =========================

def led_1(value):
  print "LED1 : "
  print value

def led_2(value):
  print "LED2 : "
  print value

def button_1(value):
  if value == 1:
    GPIO.output(24, GPIO.HIGH)
    time.sleep(.5)
    GPIO.output(24, GPIO.LOW)
 
def button_2(value):
  if value == 1:
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
brew_array.subscribe("button_1", button_1);
brew_array.subscribe("button_2", button_2);

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

  if GPIO.input(18) != led_1:

    led_1 = GPIO.input(18)
    brew_array.publish("led_1",1)


  if GPIO.input(23) != led_2:

    led_2 = GPIO.input(23)
    brew_array.publish("led_2",1)
