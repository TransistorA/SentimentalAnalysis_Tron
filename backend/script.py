#!/usr/bin/env python3

# Use this script to generate a production line schedule
# given cases needed and product listing files


from solver.shifts import ShiftsModel
from src.cases_needed import CasesNeeded
from src.product_listing import ProductListing
from src.schedule import Schedule


def createInputsDict(cnObj, plObj):
    return {}


def convertResultsToSchedule(results):
    schObj = Schedule(date='TO FILL')
    return schObj


def main():
    casesNeededFilename = ''
    productListingFilename = ''

    cnObj = CasesNeeded()
    cnObj.readFile(casesNeededFilename)

    plObj = ProductListing()
    plObj.readFile(productListingFilename)

    inputs = createInputsDict(cnObj, plObj)

    m = ShiftsModel(data=inputs)
    results = m.solve()
    isValid = m.isValidSchedule(results)
    if not isValid:
        print('Generated schedule is infeasible')
        return

    scheduleObj = convertResultsToSchedule(results)
    print(scheduleObj)


if __name__ == '__main__':
    main()
