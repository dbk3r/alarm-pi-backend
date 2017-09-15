#!/usr/bin/python
from __future__ import print_function
import time,sys,threading
import RPi.GPIO as GPIO
import pymysql, signal
from db_functions import *

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


gpio_out = [3,5,7,29,31,24,26,19,21,23]
gpio_in = [8,10,12]
for gpo in gpio_out:
    GPIO.setup(gpo, GPIO.OUT)

for gpi in gpio_in:
    GPIO.setup(gpi, GPIO.IN)

DB = MYDB()
IO = MYIO(DB)

signal.signal(signal.SIGTERM, IO.handler)
signal.signal(signal.SIGINT, IO.handler)



start_time = time.time()
try:
    time.sleep(1)
    while True:
        IO.getInGPIO(gpio_in)
        IO.setGPIO()
        time.sleep(0.1)

finally:

    print ("exit")
