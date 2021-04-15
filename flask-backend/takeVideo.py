from picamera import PiCamera 
from time import sleep
import pickle
from datetime import datetime
import subprocess
import os.path
import os
import shlex
from threading import Thread
import boto3
from botocore.config import Config

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
class TakeVideo():
    def __init__(self):
        self.camera = PiCamera()
        self.secret = os.environ.get('aws_secret_access_key')
        self.access = os.environ.get('aws_access_key_id')

    def takeVideo(self):
        pickle_off = open("treatPickle.pickle", 'rb')
        totalPickle = pickle.load(pickle_off)
        newVideoPickle = totalPickle['video']
        pickle_off.close()
        videoNumber = int(newVideoPickle["videoNumber"])
        videoNumber += 1
        newVideoPickle["videoNumber"] = videoNumber
        newVideoPath = '../videos/Tedi'+str(videoNumber)+'.h264'
        videoPathForMP4Convert = '../videos/Tedi'+str(videoNumber)
        videoPathForMP4ConvertWithMP4 = videoPathForMP4Convert + '.mp4'
        videoNameAWS = 'Tedi'+str(videoNumber)+'.mp4'
        now = datetime.now()
        nowTimestamp = int(datetime.timestamp(now))
        newVideoPickle["videoPaths"].append({"path":(videoPathForMP4Convert+".mp4"),"date":nowTimestamp,"videoNumber":videoNumber,"videoNameAWS":videoNameAWS})

        pickling_on = open("treatPickle.pickle","wb")
        totalPickle['video']=newVideoPickle
        pickle.dump(totalPickle, pickling_on)
        pickling_on.close()
        self.camera.start_preview()
        self.camera.start_recording(newVideoPath)
        sleep(5)
        self.camera.stop_recording()
        self.camera.stop_preview()
        command = shlex.split("MP4Box -add {f}.h264 {f}.mp4".format(f=videoPathForMP4Convert))
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        os.remove(videoPathForMP4Convert+".h264")

        my_config = Config(region_name = 'us-east-1')

        client = boto3.client(
            's3',
            aws_access_key_id=self.access,
            aws_secret_access_key=self.secret,
            config=my_config
        )

        reponseForUpload = client.upload_file(videoPathForMP4ConvertWithMP4, 'tedi-video-bucket', videoNameAWS)

    # def takeVideo(self):
    #     pickle_off = open("treatPickle.pickle", 'rb')
    #     totalPickle = pickle.load(pickle_off)
    #     newVideoPickle = totalPickle['video']
    #     pickle_off.close()
    #     videoNumber = int(newVideoPickle["videoNumber"])
    #     videoNumber += 1
    #     newVideoPickle["videoNumber"] = videoNumber
    #     newVideoPath = './videos/Tedi'+str(videoNumber)+'.h264'
    #     videoPathForMP4Convert = './videos/Tedi'+str(videoNumber)
    #     now = datetime.now()
    #     nowTimestamp = int(datetime.timestamp(now))
    #     newVideoPickle["videoPaths"].append({"path":(videoPathForMP4Convert+".mp4"),"date":nowTimestamp,"videoNumber":videoNumber})

    #     pickling_on = open("treatPickle.pickle","wb")
    #     totalPickle['video']=newVideoPickle
    #     pickle.dump(totalPickle, pickling_on)
    #     pickling_on.close()

    #     self.camera.start_preview()
    #     self.camera.start_recording(newVideoPath)
    #     sleep(15)
    #     self.camera.stop_recording()
    #     self.camera.stop_preview()
    #     os.remove(videoPathForMP4Convert+".mp4")
    #     command = shlex.split("MP4Box -add {f}.h264 {f}.mp4".format(f=videoPathForMP4Convert))
    #     output = subprocess.check_output(command, stderr=subprocess.STDOUT)
    #     os.remove(videoPathForMP4Convert+".h264")

# class TakeVideo():
#     def __init__(self): 
#         self._running = True
        
        
#     def terminate(self): 
#         self._running = False

#     def run(self): 
#         def takeVideo():
#             camera = PiCamera()
#             pickle_off = open("treatPickle.pickle", 'rb')
#             totalPickle = pickle.load(pickle_off)
#             newVideoPickle = totalPickle['video']
#             pickle_off.close()
#             videoNumber = int(newVideoPickle["videoNumber"])
#             videoNumber += 1
#             newVideoPickle["videoNumber"] = videoNumber
#             newVideoPath = '../react-frontend/src/videos/Tedi'+str(videoNumber)+'.h264'
#             videoPathForMP4Convert = '../react-frontend/src/videos/Tedi'+str(videoNumber)
#             videoPathForReact = './videos/Tedi'+str(videoNumber)+'.mp4'
#             now = datetime.now()
#             nowTimestamp = int(datetime.timestamp(now))
#             newVideoPickle["videoPaths"].append({"pathFlask":(videoPathForMP4Convert+".mp4"),"pathReact":videoPathForReact,"date":nowTimestamp})

#             pickling_on = open("treatPickle.pickle","wb")
#             totalPickle['video']=newVideoPickle
#             pickle.dump(totalPickle, pickling_on)
#             pickling_on.close()

#             camera.start_preview()
#             camera.start_recording(newVideoPath)
#             sleep(15)
#             camera.stop_recording()
#             camera.stop_preview()

#             command = shlex.split("MP4Box -add {f}.h264 {f}.mp4".format(f=videoPathForMP4Convert))
#             output = subprocess.check_output(command, stderr=subprocess.STDOUT)
#             os.remove(videoPathForMP4Convert+".h264")

#         if self._running == True:
            
#             takeVideo()



# def takeVideo():
#     camera = PiCamera()
#     pickle_off = open("treatPickle.pickle", 'rb')
#     totalPickle = pickle.load(pickle_off)
#     newVideoPickle = totalPickle['video']
#     pickle_off.close()
#     videoNumber = int(newVideoPickle["videoNumber"])
#     videoNumber += 1
#     newVideoPickle["videoNumber"] = videoNumber
#     newVideoPath = '../react-frontend/src/videos/Tedi'+str(videoNumber)+'.h264'
#     videoPathForMP4Convert = '../react-frontend/src/videos/Tedi'+str(videoNumber)
#     videoPathForReact = './videos/Tedi'+str(videoNumber)+'.mp4'
#     now = datetime.now()
#     nowTimestamp = int(datetime.timestamp(now))
#     newVideoPickle["videoPaths"].append({"pathFlask":(videoPathForMP4Convert+".mp4"),"pathReact":videoPathForReact,"date":nowTimestamp})

#     pickling_on = open("treatPickle.pickle","wb")
#     totalPickle['video']=newVideoPickle
#     pickle.dump(totalPickle, pickling_on)
#     pickling_on.close()

#     camera.start_preview()
#     camera.start_recording(newVideoPath)
#     sleep(15)
#     camera.stop_recording()
#     camera.stop_preview()

#     command = shlex.split("MP4Box -add {f}.h264 {f}.mp4".format(f=videoPathForMP4Convert))
#     output = subprocess.check_output(command, stderr=subprocess.STDOUT)
#     os.remove(videoPathForMP4Convert+".h264")