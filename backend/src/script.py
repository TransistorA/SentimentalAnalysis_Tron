#!/usr/bin/env python3

# Use this script to generate a production line schedule
# given cases needed and product listing files
import os
import random
from datetime import datetime, timedelta
from math import ceil

from solver.changeover_allergen import ChangeoverAllergenModel
from cases_needed import CasesNeeded
from product_listing import ProductListing
from schedule import *
from constants import *

from pyomo.opt import TerminationCondition

MINUTES_IN_HOUR = 60
HOURS_IN_DAY = 24

DAY_BEGIN_HR = 8
DAY_END_HR = 16

DUMMY_BATCH_ITEM_NO = 'DUMMY'


def getBatchesData(cnObj, plObj, line='TUB'):
    deadlines = []      # batch deadlines
    itemNumbers = []   # batch item numbers
    batchRunTimes = []    # batch run times

    lineObj = cnObj.getLineObj(line)

    for itemNo, orders in lineObj.items():
        cpb = plObj.getCasesPerBatch(itemNumber=itemNo)
        timeToRunBatch = plObj.getBatchTime(itemNumber=itemNo)

        temp = []
        leftover = 0
        for idx, order in enumerate(orders):
            numBatches = ceil((order[1] - leftover) / float(cpb))
            temp.append(numBatches)
            leftover = (sum(temp) * cpb) - order[2]
            assert leftover <= cpb

            for _ in range(numBatches):
                deadlines.append(order[0])
                itemNumbers.append(itemNo)
                batchRunTimes.append(timeToRunBatch)

    return deadlines, itemNumbers, batchRunTimes


def deadlinesToNumeric(deadlines, startDt=None, daysToSkip=None):
    if startDt is None:
        startDt = datetime.today()
    if daysToSkip is None:
        # TODO: change this 145 days thing
        daysToSkip = 200

    result = []
    for deadline in deadlines:
        deadline = deadline.strip()
        deadlineDtObj = datetime.strptime(deadline, '%m/%d/%Y')
        deadlineHrs = (deadlineDtObj - startDt).days * HOURS_IN_DAY
        result.append(deadlineHrs + (daysToSkip * HOURS_IN_DAY))

    return result


def getFuncChangeOverTime(itemNumbers, plObj):
    numItems = len(itemNumbers)
    result = []
    for _ in range(numItems):
        result.append([0] * numItems)

    for i in range(numItems):
        for j in range(numItems):
            if (itemNumbers[i] == DUMMY_BATCH_ITEM_NO
                    or itemNumbers[j] == DUMMY_BATCH_ITEM_NO):
                result[i][j] = 0
                continue

            cot = plObj.getChangeoverTime(item1=itemNumbers[i],
                                          item2=itemNumbers[j])
            result[i][j] = cot / float(MINUTES_IN_HOUR)

    def func(i, j):
        return result[i][j]
    return func


def addExtraBatches(deadlines, batchRunTimes, itemNumbers, startTimes):
    numDays = max(deadlines) // HOURS_IN_DAY

    deadlines.append(DAY_BEGIN_HR)
    batchRunTimes.append(DAY_BEGIN_HR)
    itemNumbers.append(DUMMY_BATCH_ITEM_NO)
    startTimes.append(0)

    for day in range(1, numDays):
        new_batch = ((day - 1) * HOURS_IN_DAY + DAY_END_HR,
                     day * HOURS_IN_DAY + DAY_BEGIN_HR)
        deadlines.append(new_batch[1])

        batchRunTimes.append(new_batch[1] - new_batch[0])
        itemNumbers.append(DUMMY_BATCH_ITEM_NO)
        startTimes.append(new_batch[0])


def createInputsDict(cnObj, plObj, maxNumBatches=5):
    # 20 batches, 60 seconds, ChangeoverModel
    _deadlines, _items, _Tp = getBatchesData(cnObj, plObj)
    _D = deadlinesToNumeric(_deadlines)  # convert deadline dates to hours

    # sort based on the deadline
    indices = sorted(range(len(_D)), key=lambda k: _D[k])

    D, itemNumbers, Tp = [], [], []
    Ds = [0] * maxNumBatches
    for idx in indices[:maxNumBatches]:
        # order other lists according to deadline dates
        D.append(_D[idx])
        itemNumbers.append(_items[idx])
        Tp.append(_Tp[idx])

    addExtraBatches(D, Tp, itemNumbers, Ds)

    print('Deadlines (hr): ' + str(D))
    print('Item numbers: ', itemNumbers)
    print('Time to run (hr): ' + str(Tp))

    numBatches = len(D)
    changeroverFunc = getFuncChangeOverTime(itemNumbers, plObj)

    return {
        'num_batches': numBatches,
        'D': D,
        'Tp': Tp,
        'Ds': Ds,
        'C_time': changeroverFunc,
        'item_number': itemNumbers
    }


def convertResultsToSchedule(plObj, m, inputs):
    startTimeDic = {}
    # create a dictionary where key is the start time and value is the
    # corresponding item number
    for i in m.model.Range:
        start = round(m.model.Ts[i].value, 2)
        startTimeDic[start] = inputs['item_number'][i]

    # a list of sorted start time
    sortedStartTime = sorted(startTimeDic)

    schObj = Schedule(date=datetime.today())
    for start in sortedStartTime:
        itemNum = startTimeDic[start]

        if startTimeDic[start] == DUMMY_BATCH_ITEM_NO:
            continue

        info = plObj.getItem(itemNum)
        obj = ScheduleItem(
            itemNum=itemNum,
            label=info[LABEL],
            product=info[DESCRIPTION],
            packSize=info[PACK_SIZE],
            cases=plObj.getCasesPerBatch(itemNum),
            rossNum=info[ROSS_WIP],
            batches='1',
            allergens=[info[ALLERGEN_VALUE]],
            kosher=("Non-Kosher" if info[COMMENTS]
                    == 'Non-Kosher' else "Kosher"),
            starttime=start)

        schObj.addItemToLine(lineStr=info[LINE],
                             scheduleItem=obj)

    return schObj


def schedule(casesNeededFilename, productListingFilename, timelimit):
    cnObj = CasesNeeded()
    cnObj.readFile(casesNeededFilename)

    plObj = ProductListing()
    plObj.readNewFile(productListingFilename)

    inputs = createInputsDict(cnObj, plObj)

    m = ChangeoverAllergenModel(data=inputs)
    results = m.solve(debug=False, solver='glpk', timelimit=timelimit)
    isValid = m.isValidSchedule(results)
    if not isValid:
        if results.solver.termination_condition == TerminationCondition.maxTimeLimit:
            msg = 'Could not find a feasible schedule in the time allotted ({} secs)'.format(
                timelimit)
            raise Exception(msg)
        else:
            raise Exception('No feasible schedule available')

    scheduleObj = convertResultsToSchedule(plObj, m, inputs)
    return scheduleObj


def main():
    dir = os.path.dirname(__file__)
    casesNeededFilename = os.path.join(
        dir, 'samples', 'cases_needed.csv')
    productListingFilename = os.path.join(
        dir, 'samples', 'product_listing.csv')

    print(schedule(casesNeededFilename, productListingFilename, 60))


if __name__ == '__main__':
    main()