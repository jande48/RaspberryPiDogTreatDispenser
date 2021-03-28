from picamera import PiCamera 
from time import sleep
import pickle
from datetime import datetime
import subprocess
import os.path
import os
import shlex
camera = PiCamera()


pickle_off = open("treatPickle.pickle", 'rb')
totalPickle = pickle.load(pickle_off)
newVideoPickle = totalPickle['video']
pickle_off.close()
videoNumber = int(newVideoPickle["videoNumber"])
videoNumber += 1
newVideoPickle["videoNumber"] = videoNumber
newVideoPath = '../react-frontend/src/videos/Tedi'+str(videoNumber)+'.h264'
videoPathForMP4Convert = '../react-frontend/src/videos/Tedi'+str(videoNumber)
videoPathForReact = './videos/Tedi'+str(videoNumber)+'.mp4'
now = datetime.now()
nowTimestamp = int(datetime.timestamp(now))
newVideoPickle["videoPaths"].append({"pathFlask":(videoPathForMP4Convert+".mp4"),"pathReact":videoPathForReact,"date":nowTimestamp})

pickling_on = open("treatPickle.pickle","wb")
totalPickle['video']=newVideoPickle
pickle.dump(totalPickle, pickling_on)
pickling_on.close()

camera.start_preview()
camera.start_recording(newVideoPath)
sleep(5)
camera.stop_recording()
camera.stop_preview()

command = shlex.split("MP4Box -add {f}.h264 {f}.mp4".format(f=videoPathForMP4Convert))
output = subprocess.check_output(command, stderr=subprocess.STDOUT)
os.remove(videoPathForMP4Convert+".h264")