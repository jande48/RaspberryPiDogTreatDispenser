import time
import board
import busio
import adafruit_mpr121
import RPi.GPIO as GPIO

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
        
    return 1

# class DispenseTreat:
#     __instance = None
#     def __new__(cls):
#         print('we got here 1')
#         if cls.__instance is None:
#             cls.__instance = object.__new__(cls)
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(17,GPIO.OUT)
#         cls.__instance.servo1 = GPIO.PWM(17,50)# 50hz frequency
#         print('we got here 2')
#         return cls.__instance

#     def __call__(cls, *args, **kwargs):
#         print('we got here 3')
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(17,GPIO.OUT)
#         servo2 = cls.__instance.servo1
#         servo2.start(7)# starting duty cycle ( it set the servo to 0 degree )
#         time.sleep(0.2)

#         servo2.ChangeDutyCycle(10)
#         time.sleep(0.1)

#         servo2.stop()
#         GPIO.cleanup()
#         print('we got here 4')
#         return 1



    # class __DispenseTreat:
    #     def __init__(self):
    #         GPIO.setmode(GPIO.BCM)
    #         GPIO.setup(17,GPIO.OUT)
    #         self.servo1 = GPIO.PWM(17,50)# 50hz frequency
        
    #     def dispenseTreat(self):

    #         #servo1 = GPIO.PWM(17,50)# 50hz frequency
    #         self.servo1.start(7)# starting duty cycle ( it set the servo to 0 degree )
    #         time.sleep(0.2)

    #         self.servo1.ChangeDutyCycle(10)
    #         time.sleep(0.1)

    #         self.servo1.stop()
    #         GPIO.cleanup()
                
    #         return 1
    # instance = None

    # def __init__(self):
    #     if not DispenseTreat.instance:
    #         DispenseTreat.instance = DispenseTreat.__DispenseTreat()
        
    
    
    # @staticmethod
    # def getInstance():
    #     if DispenseTreat.__instance == None:
    #         DispenseTreat()
    #     return DispenseTreat.__instance


    # def __init__(self): 
        
    #     if DispenseTreat.__instance != None:
    #         raise Exception("Can't do that with a singleton")
    #     else: 
    #         DispenseTreat.__instance = self

    # def dispenseTreat(self):

    #     #servo1 = GPIO.PWM(17,50)# 50hz frequency
    #     self.servo1.start(7)# starting duty cycle ( it set the servo to 0 degree )
    #     time.sleep(0.2)

    #     self.servo1.ChangeDutyCycle(10)
    #     time.sleep(0.1)

    #     self.servo1.stop()
    #     GPIO.cleanup()
            
    #     return 1
