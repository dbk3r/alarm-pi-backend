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


class MYDB:
    db = None
    def __init__(self):
        self.db = pymysql.connect("localhost","alarm","passw0rd","alarm" )

    def gpUpdate(self,state,gp):
        cursor = self.db.cursor(pymysql.cursors.DictCursor)
        cursor.execute("update dba_switch set switch_state='"+ state  +"' where switch_GPIO='"+ gp +"'")
        cursor.close()

    def setGPIO(self):
        cursor = self.db.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * from dba_switch where switch_GPIO <> '0'")
        result = cursor.fetchall()

        for row in result:
            #print(str(row['switch_GPIO']) + " : " + str(row['switch_state']))
            if (row['switch_state'] == 1):
                if (row['switch_GPIO'] == 21):
                    t = threading.Thread(target=seq_leuchte)
                    t.start()
                elif (row['switch_GPIO' == 24]):
                    t = threading.Thread(target=seq_sirene)
                    t.start()
                else:
                    GPIO.output(row['switch_GPIO'], GPIO.LOW)
            else:
                GPIO.output(row['switch_GPIO'], GPIO.HIGH)

        cursor.close()


    def getInGPIO(self):
        for gpi in gpio_in:
            if (GPIO.input(gpi) == 1):
                if (gpi == 8):
                    melder = "Alarm Leuchte"
                    gpo = 21
                elif (gpi == 10):
                    melder = "Alarm Sirene"
                    gpo= 24
                self.gpUpdate('1',gpo)
                new_event(gpo)
        
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)

db = MYDB()
start_time = time.time()
try:
    while True:
        db.setGPIO()
        db.getInGPIO()
finally:
    time.sleep(1)
    print ("exit")
