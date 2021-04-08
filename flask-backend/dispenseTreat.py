import time
import board
import busio
import adafruit_mpr121
import RPi.GPIO as GPIO
from takeVideo import TakeVideo



def dispenseTreat():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17,GPIO.OUT)
    servo1 = GPIO.PWM(17,50)# 50hz frequency
    servo1.start(7)# starting duty cycle ( it set the servo to 0 degree )
    time.sleep(0.2)

    servo1.ChangeDutyCycle(10)
    time.sleep(0.1)

    servo1.stop()
    GPIO.cleanup()
    #takeVideo = TakeVideo.Instance()
    #takeVideo.takeVideo()

    return 1
