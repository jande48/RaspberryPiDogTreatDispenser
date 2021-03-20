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
from pickleFuncs import getPickle


app = aaplication = flask.Flask(__name__)
waitForTouchFlask = WaitForTouch() 
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
        WaitForTouch().terminate() 
        # ScheduleTreats().terminate()
        time.sleep(0.5)
        dispenseTreat()
        
        audio = AudioSegment.from_file('/home/pi/Desktop/DoggieObstacleCoarse/Assets/goodGirlTedi.m4a')
        play(audio)
        waitForTouchFlask = WaitForTouch() 
        thr = Thread(target = waitForTouchFlask.run) 
        thr.start() 
        # scheduleTreatsFlask = ScheduleTreats()
        # thrSchedule = Thread(target= scheduleTreatsFlask.run)
        # thrSchedule.start()
    return json.dumps({'key': 'success'})

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
    WaitForTouch().terminate() 
    # ScheduleTreats().terminate()
    # waitForTouchFlask = WaitForTouch()
    # waitForTouchFlask.terminate()
    JSON_sent = request.get_json()
    JSON_sent["lastDate"] = str(datetime.now().date())
    pickling_on = open("treatPickle.pickle","wb")
    pickle.dump(JSON_sent, pickling_on)
    pickling_on.close()
    
    #Thread(target = WaitForTouch.run).start() 
    waitForTouchFlask = WaitForTouch() 
    thr = Thread(target = waitForTouchFlask.run) 
    thr.start() 
    # scheduleTreatsFlask = ScheduleTreats()
    # thrSchedule = Thread(target= scheduleTreatsFlask.run)
    # thrSchedule.start()
    return json.dumps(JSON_sent)




if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)