import subprocess,sys,time
import RPi.GPIO as GPIO
import pymysql, signal, threading
from time import gmtime, strftime


class MYDB:
    db = None
    def __init__(self):
        self.db = pymysql.connect("localhost","alarm","passw0rd","alarm" )

    def gpUpdate(self,state,gp):
        cursor = self.db.cursor(pymysql.cursors.DictCursor)
        cursor.execute("update dba_switch set switch_state='"+ str(state)  +"' where switch_GPIO='"+ str(gp) +"'")
        self.db.commit()
        cursor.close()

    def getIOs(self):
        cursor = self.db.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * from dba_switch where switch_GPIO <> '0'")
        result = cursor.fetchall()
        cursor.close()
        return result

    def insertEvent(self,evName,evImage,evPlace):
        evTime = strftime("%Y%m%d-%H%M%S", gmtime())
        cursor = self.db.cursor(pymysql.cursors.DictCursor)
        cursor.execute("insert into dba_events (event_name, event_time, event_image, event_place) values ('"+ evName +"','"+ str(evTime) +"','"+ evImage +"', '"+ evPlace +"')")
        self.db.commit()
        cursor.close()
        print ("Event: " + evName + " am " + str(evTime) )



class MYIO:

    DB = None
    gp_21 = 0
    gp_24 = 0

    def __init__(self,db):
        self.DB = db


    def setGPIO(self):
        result = self.DB.getIOs()


        for row in result:
            #print(str(row['switch_GPIO']) + " : " + str(row['switch_state']))
            if (row['switch_state'] == 1):
                if (row['switch_GPIO'] == 21 and self.gp_21 == 0):
                    t = threading.Thread(target=self.seq_leuchte)
                    t.start()
                    t.join()
                    self.DB.gpUpdate('0',21)


                elif (row['switch_GPIO'] == 24 and self.gp_24 == 0):
                    t = threading.Thread(target=self.seq_sirene)
                    t.start()

                else:
                    GPIO.output(row['switch_GPIO'], GPIO.LOW)
            else:
                GPIO.output(row['switch_GPIO'], GPIO.HIGH)




    def getInGPIO(self,gpio_in):
        for gpi in gpio_in:
            if (GPIO.input(gpi) == 1):
                if (gpi == 8 and self.gp_21 == 0):
                    melder = "Alarm Leuchte"
                    self.DB.gpUpdate('1',21)
                    self.DB.insertEvent("Bewegung 1","img.png","Studio")
                elif (gpi == 10 and self.gp_24 == 0):
                    melder = "Alarm Sirene"
                    self.DB.gpUpdate('1',24)
                    self.DB.insertEvent("Bewegung 2","img.png","Recording-Room")



    def handler(self,signum,frame):
            sys.exit(0)

    def seq_sirene(self):
       GPIO.ouput(24,GPIO.LOW)


    def seq_leuchte(self):
        try:
            self.gp_21 = 1
            GPIO.output(21,GPIO.LOW)
            time.sleep(4)
            GPIO.output(21,GPIO.HIGH)
            self.gp_21 = 0


        except pymysql.Error as e:
            print(e)



    def new_event(self,gp):
        if (gp == 21):
            self.DB.insertEvent("Bewegung 1","img.png","Studio")
