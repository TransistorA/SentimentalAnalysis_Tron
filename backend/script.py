#!/usr/bin/env python3

# Use this script to generate a production line schedule
# given cases needed and product listing files
import os
import random
from datetime import datetime, timedelta
from math import ceil

from solver.shifts import ShiftsModel
from solver.changeover_allergen import ChangeoverAllergenModel
from src.cases_needed import CasesNeeded
from src.product_listing import ProductListing
from src.schedule import *
from src.constants import *


HOURS_IN_DAY = 24


def getBatchesInfo(cnObj, plObj, line=None):
    deadlines = []  # batch's deadline
    itemNumbers = []  # batch's item number
    timeToRun = []  # time to run batch
    for itemNo, orders in cnObj.tub.items():
        tempResult = []
        cpb = plObj.getCasesPerBatch(itemNumber=itemNo)
        timeToRunBatch = plObj.getBatchTime(itemNumber=itemNo)
        timeToRunBatch = random.randint(1, 2)  # TODO: remove this
        leftover = 0
        for idx, order in enumerate(orders):
            num_batches = ceil((order[1] - leftover) / float(cpb))
            tempResult.append(num_batches)
            leftover = (sum(tempResult) * cpb) - order[2]
            assert leftover <= cpb

            for _ in range(num_batches):
                deadlines.append(order[0])
                itemNumbers.append(itemNo)
                timeToRun.append(timeToRunBatch)

    return deadlines, itemNumbers, timeToRun


def convertDeadlinesToNum(deadlines, startDate=None):
    if startDate is None:
        startDate = datetime.today()

    result = []
    for deadline in deadlines:
        deadline = deadline.strip()
        dateObj = datetime.strptime(deadline, '%m/%d/%Y')
        deadlineInHour = (dateObj - startDate).days * HOURS_IN_DAY
        # TODO: change this 125 days thing
        result.append(deadlineInHour + 127 * 24)

    return result


def getFuncChangeOvertime(itemNumbers, plObj):
    result = []
    for _ in range(len(itemNumbers)):
        result.append([0] * len(itemNumbers))

    for i in range(len(itemNumbers)):
        for j in range(len(itemNumbers)):
            if itemNumbers[i] == 'DUMMY' or itemNumbers[j] == 'DUMMY':
                result[i][j] = 0
                continue
            cot = plObj.getChangeoverTime(item1=itemNumbers[i],
                                          item2=itemNumbers[j])
            result[i][j] = 0.5  # TODO: change this to cot

    def func(i, j):
        return result[i][j]

    return func


def addExtraBatches(deadlines, time_to_run, item_numbers, start_times):
    num_days = max(deadlines) // HOURS_IN_DAY
    deadlines.append(8)
    time_to_run.append(8)
    item_numbers.append('DUMMY')
    start_times.append(0)
    for day in range(1, num_days):
        new_batch = (day * HOURS_IN_DAY - 8, day * HOURS_IN_DAY + 8)
        deadlines.append(new_batch[1])
        time_to_run.append(new_batch[1] - new_batch[0])
        item_numbers.append('DUMMY')
        start_times.append(new_batch[0])


def createInputsDict(cnObj, plObj):
    # 20 batches, 60 seconds, ChangeoverModel
    # 12 batches, 60 seconds, Shifts
    _deadlines, _items, _Tp = getBatchesInfo(cnObj, plObj)
    _D = convertDeadlinesToNum(_deadlines)

    indices = sorted(range(len(_D)), key=lambda k: _D[k])
    indices = indices[:10]

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
    C_time = getFuncChangeOvertime(item_numbers, plObj)

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
        sorted_starttime = sorted(starttimedic, key=lambda x: starttimedic[x])  # a list of item numbers sorted by start time

    schObj = Schedule(date='TO FILL')
    for itemNumber in sorted_starttime:
        if itemNumber == "DUMMY":
            continue
        
        #information in the format as ['CAESAR DRSG', '4/123 FL OZ', 'MELTING POT', 'MPT01', 'Milk,Fish,Egg,Soy', 'x blue pallet', 'Non-Kosher', '', <Allergen.SOY|FISH|MILK|EGG: 57>, 'GALLON', 54, 1]
        info = plObj.getItem(itemNumber)
        obj = ScheduleItem(
         itemNum=itemNumber,
         label=info[LABEL],
         product=info[DESCRIPTION],
         packSize=info[PACK_SIZE],
         cases=100,
         rossNum=info[ROSS_WIP],
         batches='1',
         allergens=[info[8]], # generated allergen object
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


def main():
    dir = os.path.dirname(__file__)
    casesNeededFilename = os.path.join(
        dir, 'src', 'samples', 'cases_needed.csv')
    productListingFilename = os.path.join(
        dir, 'src', 'samples', 'product_listing.csv')

    cnObj = CasesNeeded()
    cnObj.readFile(casesNeededFilename)

    plObj = ProductListing()
    plObj.readNewFile(productListingFilename)

    inputs = createInputsDict(cnObj, plObj)

    m = ChangeoverAllergenModel(data=inputs)
    results = m.solve(debug=True)
    isValid = m.isValidSchedule(results)
    if not isValid:
        print('Generated schedule is infeasible')
        return

    scheduleObj = convertResultsToSchedule(plObj, m, inputs)
    print(scheduleObj)


if __name__ == '__main__':
    main()
