import sys

sys.path.append('../../')
from casesNeeded.casesNeeded import *


def readinputPail():
    fileName = "../../casesNeeded/casesNeeded.csv"
    cn = CasesNeeded()
    cn.readFile(fileName)
    # return the total number of batches, item number and due date of each item
    numBatches, itemNumbers, Duedates = cn.getItemsPail()

    return numBatches, itemNumbers, Duedates


def stringToTime(strList, today):
    # Change a list of string of dates into a list of date object
    # the strList is the list of string of duedates, today is the present day in date data structure
    timeList = []  # the time left until due date for each item
    for str in strList:
        month = int(str[1:3])
        day = int(str[4:6])
        year = int(str[7:])
        d = date(year, month, day)
        time = abs(d - today).days * 24 * 60  # Transfer number of days to minutes
        timeList.append(time)
    return timeList


def outputdata():
    num_batches, itemNumbers, Duedates = readinputPail()  # number of batches
    today = date(2018, 9, 25)  # for test only, in real implementation will change it to the present day. It is basically the D_s.
    D = stringToTime(Duedates, today)  # deadline of batch i
    return num_batches, itemNumbers, D


print(outputdata()[2])
