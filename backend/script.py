#!/usr/bin/env python3

# Use this script to generate a production line schedule
# given cases needed and product listing files
import os
import random
from datetime import datetime, timedelta
from math import ceil

from solver.changeover_allergen import ChangeoverAllergenModel
from src.cases_needed import CasesNeeded
from src.product_listing import ProductListing
from src.schedule import *
from src.constants import *


HOURS_IN_DAY = 24
DUMMY_BATCH_ITEM_NO = 'DUMMY'


def getBatchesData(cnObj, plObj, line='Tub'):
    deadlines = []      # batch deadlines
    itemNumbers = []   # batch item numbers
    batchRunTimes = []    # batch run times

    # TODO: refactor line logic
    lineObj = cnObj.getLineObj(line.lower())

    for itemNo, orders in lineObj.items():
        cpb = plObj.getCasesPerBatch(itemNumber=itemNo)
        timeToRunBatch = plObj.getBatchTime(itemNumber=itemNo)
        timeToRunBatch = random.randint(1, 2)    # TODO: remove this line

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
        daysToSkip = 145

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
            result[i][j] = 0.5  # TODO: remove this line

    def func(i, j):
        return result[i][j]
    return func


def addExtraBatches(deadlines, timeToRun, itemNumbers, startTimes):
    num_days = max(deadlines) // HOURS_IN_DAY
    deadlines.append(8)
    timeToRun.append(8)
    itemNumbers.append(DUMMY_BATCH_ITEM_NO)
    startTimes.append(0)
    for day in range(1, num_days):
        new_batch = (day * HOURS_IN_DAY - 8, day * HOURS_IN_DAY + 8)
        deadlines.append(new_batch[1])
        timeToRun.append(new_batch[1] - new_batch[0])
        itemNumbers.append(DUMMY_BATCH_ITEM_NO)
        startTimes.append(new_batch[0])


def createInputsDict(cnObj, plObj):
    # 20 batches, 60 seconds, ChangeoverModel
    # 12 batches, 60 seconds, Shifts
    _deadlines, _items, _Tp = getBatchesData(cnObj, plObj)
    _D = deadlinesToNumeric(_deadlines)

    indices = sorted(range(len(_D)), key=lambda k: _D[k])
    indices = indices[:5]

    D, item_numbers, Tp = [], [], []
    Ds = [0] * len(indices)
    for idx in indices:
        D.append(_D[idx])
        item_numbers.append(_items[idx])
        Tp.append(_Tp[idx])

    addExtraBatches(D, Tp, item_numbers, Ds)

    print('Deadlines (hr): ' + str(D))
    print("Item numbers: ", item_numbers, "\n")
    print('Time to run (hr): ' + str(Tp))

    num_batches = len(D)
    C_time = getFuncChangeOverTime(item_numbers, plObj)

    return {
        'num_batches': num_batches,
        'D': D,
        'Tp': Tp,
        'Ds': Ds,
        'C_time': C_time,
        'item_number': item_numbers
    }


def convertResultsToSchedule(plObj, m, inputs):
    starttimedic = {}
    for i in m.model.Range:
        start = m.model.Ts[i].value
        starttimedic[inputs['item_number'][i]] = start
        # a list of item numbers sorted by start time
        sorted_starttime = sorted(starttimedic, key=lambda x: starttimedic[x])

    schObj = Schedule(date='TO FILL')
    for itemNumber in sorted_starttime:
        if itemNumber == "DUMMY":
            continue

        # information in the format as ['CAESAR DRSG', '4/123 FL OZ', 'MELTING
        # POT', 'MPT01', 'Milk,Fish,Egg,Soy', 'x blue pallet', 'Non-Kosher',
        # '', <Allergen.SOY|FISH|MILK|EGG: 57>, 'GALLON', 54, 1]
        info = plObj.getItem(itemNumber)
        obj = ScheduleItem(
            itemNum=itemNumber,
            label=info[LABEL],
            product=info[DESCRIPTION],
            packSize=info[PACK_SIZE],
            cases=100,
            rossNum=info[ROSS_WIP],
            batches='1',
            allergens=[info[8]],  # generated allergen object
            kosher=("Kosher" if info[NON_K] == '' else "Non-Kosher"))

        if info[LINE] == 'GALLON':
            schObj.gallon.append(obj)
        elif info[LINE] == 'TUB':
            schObj.tub.append(obj)
        elif info[LINE] == 'PAIL':
            schObj.pail.append(obj)
        elif info[LINE] == 'RETAIL':
            schObj.retail.append(obj)

    return schObj


def schedule(casesNeededFilename, productListingFilename):
    cnObj = CasesNeeded()
    cnObj.readFile(casesNeededFilename)

    plObj = ProductListing()
    plObj.readNewFile(productListingFilename)

    inputs = createInputsDict(cnObj, plObj)

    m = ChangeoverAllergenModel(data=inputs)
    results = m.solve(debug=False)
    isValid = m.isValidSchedule(results)
    if not isValid:
        return 'Generated schedule is infeasible'

    scheduleObj = convertResultsToSchedule(plObj, m, inputs)
    return scheduleObj


def main():
    dir = os.path.dirname(__file__)
    casesNeededFilename = os.path.join(
        dir, 'src', 'samples', 'cases_needed.csv')
    productListingFilename = os.path.join(
        dir, 'src', 'samples', 'product_listing.csv')

    print(schedule(casesNeededFilename, productListingFilename))


if __name__ == '__main__':
    main()
