import flask
from flask import Flask
from flask import request
from flask import render_template
import json
import RPi.GPIO as GPIO
import time
import pickle
from datetime import datetime, timedelta
from waitForTouch import WaitForTouch
from threading import Thread 
from pydub import AudioSegment
from pydub.playback import play
#from scheduleTreats import ScheduleTreats
from dispenseTreat import dispenseTreat
from takeVideo import TakeVideo
from pickleFuncs import getPickle
import os
import boto3
from botocore.config import Config

app = aplication = flask.Flask(__name__)
waitForTouchFlask = WaitForTouch.Instance() 
thr = Thread(target = waitForTouchFlask.run) 
thr.start() 
#WaitForTouch().run()
#Thread(target = WaitForTouch.run).start() 
# scheduleTreatsFlask = ScheduleTreats()
# thrSchedule = Thread(target= scheduleTreatsFlask.run)
# thrSchedule.start()

# initialize singleton



# GPIO.setmode(GPIO.BCM)
# GPIO.setup(17,GPIO.OUT)
# global servo1
# servo1 = GPIO.PWM(17,50)# 50hz frequency


@app.route("/", methods=['GET','POST'])
def my_index():
    if request.method=='GET':
        return render_template('index.html', token="Hello World")
    elif request.method=='POST':
        JSON_sent = request.get_json()
        if JSON_sent['id'] == 'success':
            d = DispenseTreat()
            d.dispenseTreat()
            return json.dumps({'key': 'success'})

@app.route("/giveTreat", methods=['POST'])
def give_treat():
    JSON_sent = request.get_json()
    if JSON_sent['id'] == 'success':
        waitForTouchGiveTreat = WaitForTouch.Instance()
        waitForTouchGiveTreat.terminate()
        takeVideoFlask = TakeVideo.Instance() 
        takeVideoThr = Thread(target = takeVideoFlask.takeVideo) 
        takeVideoThr.start() 
        time.sleep(0.5)
        dispenseTreat()
        
        audio = AudioSegment.from_file('/home/pi/Desktop/DoggieObstacleCoarse/Assets/goodGirlTedi.m4a')
        play(audio)
        waitForTouchFlask = WaitForTouch.Instance() 
        thr = Thread(target = waitForTouchFlask.run) 
        thr.start() 
        # scheduleTreatsFlask = ScheduleTreats()
        # thrSchedule = Thread(target= scheduleTreatsFlask.run)
        # thrSchedule.start()

    return json.dumps({'key': 'success'})

@app.route("/getPresignedURL", methods=['GET'])
def getPresignedURL():
    pickle_off = open("treatPickle.pickle", 'rb')
    newPickle = pickle.load(pickle_off)
    pickle_off.close()

    videoPaths = newPickle['video']['videoPaths']
    presignedURL = []
    my_config = Config(region_name = 'us-east-1')
    secret = os.environ.get('aws_secret_access_key')
    access = os.environ.get('aws_access_key_id')
    client = boto3.client(
        's3',
        aws_access_key_id=access,
        aws_secret_access_key=secret,
        config=my_config
    )
    for i in videoPaths:
        responseForURL = client.generate_presigned_url('get_object',Params={'Bucket': 'tedi-video-bucket','Key':i["videoNameAWS"]},ExpiresIn=3600)
        presignedURL.insert(0,responseForURL)
    time.sleep(5)
    return json.dumps(presignedURL)

def removePastSchedules(newPickle):
    for i in range(len(newPickle["scheduledDispenseTreats"])-1,-1,-1):
        if newPickle["scheduledDispenseTreats"][i]['freq'] != 'Everyday':
            scheduleTime = newPickle["scheduledDispenseTreats"][i]['time'].split(':')
            year = newPickle["scheduledDispenseTreats"][i]['scheduledDate'][0]
            month = newPickle["scheduledDispenseTreats"][i]['scheduledDate'][1]
            day = newPickle["scheduledDispenseTreats"][i]['scheduledDate'][2]
            hour = int(scheduleTime[0])
            min = int(scheduleTime[1])
            dispenseTime = datetime(year,month,day,hour,min)
            dateTimeNow = datetime.now()

            if newPickle["scheduledDispenseTreats"][i]['freq'] == 'Tomorrow':
                diff = dispenseTime.timestamp() + (60*60*24) - dateTimeNow.timestamp()
            else:
                diff = dispenseTime.timestamp() - dateTimeNow.timestamp()
            if diff < 0:
                del newPickle["scheduledDispenseTreats"][i]

    pickling_on = open("treatPickle.pickle","wb")
    pickle.dump(newPickle, pickling_on)
    pickling_on.close()
    return newPickle

@app.route("/getPickle", methods=['GET'])
def getPickle():
    pickle_off = open("treatPickle.pickle", 'rb')
    newTreatPickle = pickle.load(pickle_off)
    pickle_off.close()
    newTreatPickle = removePastSchedules(newTreatPickle)
    return json.dumps(newTreatPickle)

@app.route("/setPickle", methods=['POST'])
def setPickle():
    waitForTouchSetPickle = WaitForTouch.Instance()
    waitForTouchSetPickle.terminate()
    # WaitForTouch().terminate() 
    # ScheduleTreats().terminate()
    # waitForTouchFlask = WaitForTouch()
    # waitForTouchFlask.terminate()
    JSON_sent = request.get_json()
    JSON_sent["lastDate"] = str(datetime.now().date())
    pickling_on = open("treatPickle.pickle","wb")
    pickle.dump(JSON_sent, pickling_on)
    pickling_on.close()
    
    #Thread(target = WaitForTouch.run).start() 
    waitForTouchFlask = WaitForTouch.Instance() 
    thr = Thread(target = waitForTouchFlask.run) 
    thr.start() 
    # scheduleTreatsFlask = ScheduleTreats()
    # thrSchedule = Thread(target= scheduleTreatsFlask.run)
    # thrSchedule.start()
    return json.dumps(JSON_sent)

@app.route("/removeVideo",methods=['POST'])
def removeVideo():
    JSON_sent = request.get_json()
    pickle_off = open("treatPickle.pickle", 'rb')
    newTreatPickle = pickle.load(pickle_off)
    pickle_off.close()
    newTreatPickle = removePastSchedules(newTreatPickle)
    print(newTreatPickle['video']['videoPaths'])
    del newTreatPickle['video']['videoPaths'][int(JSON_sent['index'])]
    print(newTreatPickle['video']['videoPaths'])
    # del newTreatPickle['video']['videoPaths'][int(JSON_sent['index'])]
    pickling_on = open("treatPickle.pickle","wb")
    pickle.dump(newTreatPickle, pickling_on)
    pickling_on.close()
    return json.dumps(newTreatPickle)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)