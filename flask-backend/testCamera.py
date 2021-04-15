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

# runs with sudo -E python testCamera.py
secret = os.environ.get('aws_secret_access_key')
access = os.environ.get('aws_access_key_id')
camera = PiCamera()

def takeVideo():
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
    camera.start_preview()
    camera.start_recording(newVideoPath)
    sleep(5)
    camera.stop_recording()
    camera.stop_preview()
    command = shlex.split("MP4Box -add {f}.h264 {f}.mp4".format(f=videoPathForMP4Convert))
    output = subprocess.check_output(command, stderr=subprocess.STDOUT)
    os.remove(videoPathForMP4Convert+".h264")

    my_config = Config(region_name = 'us-east-1')

    client = boto3.client(
        's3',
        aws_access_key_id=access,
        aws_secret_access_key=secret,
        config=my_config
    )

    reponseForUpload = client.upload_file(videoPathForMP4ConvertWithMP4, 'tedi-video-bucket', videoNameAWS)
