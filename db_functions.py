import subprocess,sys

def handler(signum,frame):
        sys.exit(0)

def seq_sirene():
   GPIO.ouput(24,GPIO.LOW)


def seq_leuchte():
    GPIO.output(21,GPIO.LOW)


def new_event(gp):
    print("event: " + str(gp))
