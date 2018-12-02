#!/usr/bin/env python3

# Use this script to generate a production line schedule
# given cases needed and product listing files
import os
from datetime import datetime, timedelta
from math import ceil

from solver.deadline_overlapping import DeadlineOverlappingModel
from solver.shifts import ShiftsModel
from src.cases_needed import CasesNeeded
from src.product_listing import ProductListing
from src.schedule import Schedule

HOURS_IN_DAY = 24


def getBatchesInfo(cnObj, plObj, line=None):
    deadlines = []  # batch's deadline
    itemNumbers = []  # batch's item number
    timeToRun = []  # time to run batch
    for itemNo, orders in cnObj.tub.items():
        tempResult = []
        cpb = plObj.getCasesPerBatch(itemNumber=itemNo)
        timeToRunBatch = plObj.getBatchTime(itemNumber=itemNo)
        leftover = 0
        for idx, order in enumerate(orders):
            numBatches = ceil((order[1] - leftover) / float(cpb))
            tempResult.append(numBatches)
            leftover = (sum(tempResult) * cpb) - order[2]
            assert leftover <= cpb

            for _ in range(numBatches):
                deadlines.append(order[0])
                itemNumbers.append(itemNo)
                timeToRun.append(timeToRunBatch)

    return deadlines, itemNumbers, timeToRun


def convertDeadlinesToNum(deadlines, startDate=None):
    if startDate is None:
        startDate = datetime.today() - timedelta(days=70)

    result = []
    for deadline in deadlines:
        deadline = deadline.strip()
        dateObj = datetime.strptime(deadline, '%m/%d/%Y')
        deadlineInHour = (dateObj - startDate).days * HOURS_IN_DAY
        result.append(deadlineInHour)

    return result


def getFuncChangeOvertime(itemNumbers, plObj):
    result = []
    for _ in range(len(itemNumbers)):
        result.append([0] * len(itemNumbers))

    for i in range(len(itemNumbers)):
        for j in range(len(itemNumbers)):
            cot = plObj.getChangeoverTime(item1=itemNumbers[i],
                                          item2=itemNumbers[j])
            result[i][j] = cot

    def func(i, j):
        return 1  # TODO: change this to result[i][j]

    return func


def createInputsDict(cnObj, plObj):
    deadlines, itemNumbers, Tp = getBatchesInfo(cnObj, plObj)

    deadlines = deadlines[:8]
    itemNumbers = itemNumbers[:8]
    Tp = Tp[:8]

    num_batches = len(deadlines)
    D = convertDeadlinesToNum(deadlines)

    print(D)
    print(Tp)
    # raise Exception

    C_time = getFuncChangeOvertime(itemNumbers, plObj)

    return {
        'num_batches': num_batches,
        'D': D,
        'Tp': Tp,
        'Ds': 0,
        'C_time': C_time
    }


def convertResultsToSchedule(results):
    schObj = Schedule(date='TO FILL')
    return schObj


def main():
    dir = os.path.dirname(__file__)
    casesNeededFilename = os.path.join(dir, 'src', 'samples', 'cases_needed.csv')
    productListingFilename = os.path.join(dir, 'src', 'samples', 'product_listing.csv')

    cnObj = CasesNeeded()
    cnObj.readFile(casesNeededFilename)

    plObj = ProductListing()
    plObj.readNewFile(productListingFilename)

    inputs = createInputsDict(cnObj, plObj)

    m = ShiftsModel(data=inputs)
    results = m.solve(debug=True)
    isValid = m.isValidSchedule(results)
    if not isValid:
        print('Generated schedule is infeasible')
        return

    scheduleObj = convertResultsToSchedule(results)
    print(scheduleObj)


if __name__ == '__main__':
    main()
