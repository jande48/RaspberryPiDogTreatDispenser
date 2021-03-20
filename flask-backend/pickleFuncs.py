import pickle
from datetime import datetime, timedelta
# mylist = ['a', 'b', 'c', 'd']
# with open('pickleFile.txt', 'wb') as fh:
#    pickle.dump(mylist, fh)
def initPickle():
    treatPickle = {"maxNumOfTreatsPerDay":3,"treatsGivenToday":0,'lastDate': '2021-03-17',"scheduledDispenseTreats":[{'time':'10:00','freq':'Everyday','scheduledDate':[2021,3,17]}]}
    pickling_on = open("treatPickle.pickle","wb")
    pickle.dump(treatPickle, pickling_on)
    pickling_on.close()

def decrementTodaysTreat():
    pickle_off = open("treatPickle.pickle", 'rb')
    newTreatPickle = pickle.load(pickle_off)
    newTreatPickle['treatsGivenToday'] += 1
    pickle_off.close()

    pickling_on = open("treatPickle.pickle","wb")
    pickle.dump(newTreatPickle, pickling_on)
    pickling_on.close()

def canDispenseTreat():
    pickle_off = open("treatPickle.pickle", 'rb')
    newTreatPickle = pickle.load(pickle_off)
    pickle_off.close()
    dateLast = datetime.strptime(newTreatPickle['lastDate'], '%Y-%m-%d')
    dateToday =datetime.strptime(str(datetime.now().date()),'%Y-%m-%d')

    if dateToday.timestamp() > dateLast.timestamp():
        newTreatPickle['lastDate'] = str(datetime.now().date())
        newTreatPickle["treatsGivenToday"] = 0
        pickling_on = open("treatPickle.pickle","wb")
        pickle.dump(newTreatPickle, pickling_on)
        pickling_on.close()

    if newTreatPickle["treatsGivenToday"] <= newTreatPickle['maxNumOfTreatsPerDay']:
        return True
    else:
        return False

def seePickle():
    pickle_off = open("treatPickle.pickle", 'rb')
    newTreatPickle = pickle.load(pickle_off)
    print(newTreatPickle)
    pickle_off.close()

def getPickle():
    pickle_off = open("treatPickle.pickle", 'rb')
    newTreatPickle = pickle.load(pickle_off)
    pickle_off.close()
    return newTreatPickle

def waitForTreats(newPickle):
    for i in range(len(newPickle["scheduledDispenseTreats"])):
        scheduleTime = newPickle["scheduledDispenseTreats"][i]['time'].split(':')
        dispenseTime = datetime(newPickle["scheduledDispenseTreats"][i]['scheduledDate'][0],newPickle["scheduledDispenseTreats"][i]['scheduledDate'][1],newPickle["scheduledDispenseTreats"][i]['scheduledDate'][2],int(scheduleTime[0]),int(scheduleTime[1]))
        dateTimeNow = datetime.now()

        if newPickle["scheduledDispenseTreats"][i]['freq'] == 'Tomorrow':
            dispenseTime =+ timedelta(days=1)

        diff = dispenseTime.timestamp() - dateTimeNow.timestamp()
        if diff > 0:
            time.sleep(diff)
            dispenseTreat()
