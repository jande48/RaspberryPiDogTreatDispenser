
import time
import board
import busio
import adafruit_mpr121
import RPi.GPIO as GPIO

from threading import Thread
from pydub import AudioSegment
from pydub.playback import play
from threading import Thread
from pickleFuncs import canDispenseTreat, decrementTodaysTreat, getPickle, setTouchPickle, getTouchPickle
from dispenseTreat import dispenseTreat
from scheduleTreats import ScheduleTreats
from datetime import datetime, timedelta

class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.
    The decorated class can define one `__init__` function that
    takes only the `self` argument. Other than that, there are
    no restrictions that apply to the decorated class.
    To get the singleton instance, use the `Instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.
    Limitations: The decorated class cannot be inherited from.
    """

    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.
        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

@Singleton
class WaitForTouch: 
      
    def __init__(self): 
        self._running = True
        
      
    def terminate(self): 
        self._running = False
        
    


    def run(self): 
        class WaitForScheduled(Thread):
            def __init__(self):
                Thread.__init__(self)
                self.newPickle = getPickle()
            
            

            def run(self):
                def determineTimeDiff(newPickle):
                    scheduleTime = newPickle['time'].split(':')
                    dispenseTime = datetime(newPickle['scheduledDate'][0],newPickle['scheduledDate'][1],newPickle['scheduledDate'][2],int(scheduleTime[0]),int(scheduleTime[1]))
                    dateTimeNow = datetime.now()

                    if newPickle['freq'] == 'Tomorrow':
                        diff = dispenseTime.timestamp() + (60*60*24) - dateTimeNow.timestamp()
                    else:
                        diff = dispenseTime.timestamp() - dateTimeNow.timestamp()
                    if diff > 0:
                        return diff
                    return -1
                timeDiffList = []
                for i in range(len(self.newPickle["scheduledDispenseTreats"])):
                    timeDiffList.append(determineTimeDiff(self.newPickle["scheduledDispenseTreats"][i])) 
                
                for i in timeDiffList:
                    if i > 0:
                        time.sleep(i)
                        dispenseTreat()
                        playGoodGirl()

        def determineIfTouched():

            
            i2c = busio.I2C(board.SCL, board.SDA)
            mpr121 = adafruit_mpr121.MPR121(i2c)
            trigger = True
            
            



            while trigger:
                
                if mpr121[2].value:
                    if canDispenseTreat():
                        #ScheduleTreats().terminate()
                        time.sleep(1)
                        dispenseTreat()
                        
                        decrementTodaysTreat()
                        playGoodGirl()
                        time.sleep(1)
                        # scheduleTreatsFlask = ScheduleTreats()
                        # thrSchedule = Thread(target= scheduleTreatsFlask.run)
                        # thrSchedule.start()
                    # else:
                    #     playWaitTilTomorrow()
                    #     time.sleep(1)
                    #     print(mpr121[1].value)
                    #     time.sleep(1)
                    #     playWaitTilTomorrow()
                    #     time.sleep(1)
                    #     if trigger:
                    #         playWaitTilTomorrow()
                    #         time.sleep(2)
                    #         trigger = False
                    trigger=False
                
            return 1

        def playGoodGirl():
            
            audio = AudioSegment.from_file('/home/pi/Desktop/DoggieObstacleCoarse/Assets/goodGirlTedi.m4a')
            play(audio)
            return 1
        
        def playWaitTilTomorrow():

            audio = AudioSegment.from_file('/home/pi/Desktop/DoggieObstacleCoarse/Assets/waitTilTomorrow.m4a')
            play(audio)
            return 1


        while self._running:
            thr = WaitForScheduled()
            thr.start()
            testTouchSingleton = getTouchPickle()
            #print(testTouchSingleton)
            #if testTouchSingleton == 0:
            setTouchPickle(1)
            determineIfTouched()
            # setTouchPickle(0)
            thr.join()
            # thr = Thread(target = determineIfTouched) 
            # thr.start() 

            
            
            # if canDispenseTreat():
            #     dispenseTreat()
            #     decrementTodaysTreat()
            #     playGoodGirl()
            # else:
            #     playWaitTilTomorrow()
