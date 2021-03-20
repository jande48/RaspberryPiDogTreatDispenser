
import time
import board
import busio
import adafruit_mpr121


import RPi.GPIO as GPIO
import time
from datetime import datetime, timedelta
from dispenseTreat import dispenseTreat
from pydub import AudioSegment
from pydub.playback import play
from threading import Thread
from pickleFuncs import getPickle


class ScheduleTreats: 
      
    def __init__(self): 
        self._running = True
        self.newPickle = getPickle()
    def terminate(self): 
        self._running = False
        
    

    def run(self): 

        # def dispenseTreat():
            

            
            

            
        #     GPIO.setmode(GPIO.BCM)
        #     GPIO.setup(17,GPIO.OUT)
        #     # connect to GPIO7 or pin # 11

        #     servo1 = GPIO.PWM(17,50)# 50hz frequency
        #     servo1.start(7)# starting duty cycle ( it set the servo to 0 degree )
        #     time.sleep(0.2)

        #     servo1.ChangeDutyCycle(10)
        #     time.sleep(0.1)

        #     servo1.stop()
        #     GPIO.cleanup()
                
        #     return 1

        def playGoodGirl():
            
            audio = AudioSegment.from_file('/home/pi/Desktop/DoggieObstacleCoarse/Assets/goodGirlTedi.m4a')
            play(audio)
            return 1
        
        def waitForTreats(newPickle):

            scheduleTime = newPickle['time'].split(':')
            dispenseTime = datetime(newPickle['scheduledDate'][0],newPickle['scheduledDate'][1],newPickle['scheduledDate'][2],int(scheduleTime[0]),int(scheduleTime[1]))
            dateTimeNow = datetime.now()

            if newPickle['freq'] == 'Tomorrow':
                diff = dispenseTime.timestamp() + (60*60*24) - dateTimeNow.timestamp()
            else:
                diff = dispenseTime.timestamp() - dateTimeNow.timestamp()
            if diff > 0:
                time.sleep(diff)
                time.sleep(0.5)
                dispenseTreat()
                
                playGoodGirl()
                waitForTouchFlask = WaitForTouch() 
                thr = Thread(target = waitForTouchFlask.run) 
                thr.start() 

        while self._running:
            
            for i in range(len(self.newPickle["scheduledDispenseTreats"])):
                waitForTreats(self.newPickle["scheduledDispenseTreats"][i])
                #Thread(target=waitForTreats, args = (newPickle["scheduledDispenseTreats"][i], )).start()
