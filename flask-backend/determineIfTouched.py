
import board
import busio
import adafruit_mpr121
import RPi.GPIO as GPIO
import time
from pickleFuncs import canDispenseTreat, decrementTodaysTreat, getPickle
from pydub import AudioSegment
from pydub.playback import play

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
class DetermineIfTouched():

    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.mpr121 = adafruit_mpr121.MPR121(i2c)
        self._running = True
            
    def terminate(self): 
        self._running = False

    def run(self):
        def playGoodGirl():
            audio = AudioSegment.from_file('/home/pi/Desktop/DoggieObstacleCoarse/Assets/goodGirlTedi.m4a')
            play(audio)

        while self._running:
            if self.mpr121[2].value:
                if canDispenseTreat():
                    time.sleep(1)
                    dispenseTreat()
                    decrementTodaysTreat()
                    playGoodGirl()
                    time.sleep(1)
            
        return 1


