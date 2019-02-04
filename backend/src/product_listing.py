import csv
import os
import re

import jsonpickle

from allergen import Allergen
from constants import *


# TODO   Add detection and calculations on previous materials
#           Need list of items and hold times


class ProductListing:

    def __init__(self):
        # create each lines dictionary
        # each key in the dictionary is an item number
        # the value is a 3-tuple of (date, case in order, running total)
        self.items = {}
        self.fpl = {}  # Finished Product Listing
        self.loadFinishedProductList()

    def readNewFile(self, fileName):
        with open(fileName, mode='r') as infile:
            reader = csv.reader(infile)
            mydict = {}

            for row in reader:
                if (len(row) > 1) and self.isItemCode(row[0]):
                    mydict[row[0]] = []
                    for elt in row:
                        if elt != row[0]:
                            mydict[row[0]] = mydict[row[0]] + [elt]

            self.items = mydict
            self.expandProductListing()
            # print(printDictionary("ITEMS", self.items))

    def loadFinishedProductList(self):
        fplFilename = os.path.join(os.path.dirname(__file__),
                                   'FinishedProductList.csv')
        with open(fplFilename, mode='r') as infile:
            reader = csv.reader(infile)
            mydict = {}

            for row in reader:
                mydict[row[0]] = row

            self.fpl = mydict

    def saveProductListing(self, filename):
        outfile = open(filename, 'a')
        outfile.write(jsonpickle.encode(self.items))
        outfile.close

    def loadProductListing(self, filename):
        outfile = open(filename, 'r')
        stuff = jsonpickle.decode(str(self.items))
        outfile.close
        self.items = stuff

    def getCasesPerBatch(self, itemNumber):
        return self.items[itemNumber][CPB]

    def getBatchTime(self, itemNumber):
        return self.items[itemNumber][TIME_TO_RUN_BATCH]

    # def loadProductListing(self):
    #    '''
    #    Read in an old product listing
    #    '''
    #    # hacking that one line function
    #    self.items = eval(open("currentListing.txt", 'r').read())

    # def saveProductListing(self):
    #    fileName = 'currentListing.txt'
    #    with open(fileName, 'w+') as wfile:
    #        wfile.write(str(self.items))

    def expandProductListing(self):
        '''
        Use the data from the file to expand the file to include items such as
        -nozzle used
        -bottle descrambler or other
        -enum based on allergens
        '''
        # add in the extra columns
        for key in self.items.keys():
            # make each item in this the null equvilent
            # Add order: Allergen, LINE, CasesPerBatch

            self.items[key] = self.items[key][0:8] + \
                [Allergen.NONE, "NONE", 0, 0, 0]
        self.addAllergenEnum()
        self.addLine()
        self.addCasesPerBatch()
        self.addBatchTime()
        self.addLeadTime()

    def addAllergenEnum(self):
        # untested function
        for key in self.items.keys():
            val = self.items[key]

            if "egg" in val[ALLERGEN].lower():
                val[ALLERGEN_VALUE] = Allergen(
                    val[ALLERGEN_VALUE] + Allergen.EGG)
            if "bisulfite" in val[ALLERGEN].lower():
                val[ALLERGEN_VALUE] = Allergen(
                    val[ALLERGEN_VALUE] + Allergen.BISULFITE)
            if "mustard" in val[ALLERGEN].lower():
                val[ALLERGEN_VALUE] = Allergen(
                    val[ALLERGEN_VALUE] + Allergen.MUSTARD)
            if "milk" in val[ALLERGEN].lower():
                val[ALLERGEN_VALUE] = Allergen(
                    val[ALLERGEN_VALUE] + Allergen.MILK)
            if "fish" in val[ALLERGEN].lower():
                val[ALLERGEN_VALUE] = Allergen(
                    val[ALLERGEN_VALUE] + Allergen.FISH)
            if "anchovy" in val[ALLERGEN].lower():
                val[ALLERGEN_VALUE] = Allergen(
                    val[ALLERGEN_VALUE] + Allergen.FISH)
            if "soy" in val[ALLERGEN].lower():
                val[ALLERGEN_VALUE] = Allergen(
                    int(val[ALLERGEN_VALUE]) + int(Allergen.SOY))
            if "treenut" in val[ALLERGEN].lower():
                val[ALLERGEN_VALUE] = Allergen(
                    val[ALLERGEN_VALUE] + Allergen.TREENUT)
            if "tree nut" in val[ALLERGEN].lower():
                val[ALLERGEN_VALUE] = Allergen(
                    val[ALLERGEN_VALUE] + Allergen.TREENUT)
            if "wheat" in val[ALLERGEN].lower():
                val[ALLERGEN_VALUE] = Allergen(
                    val[ALLERGEN_VALUE] + Allergen.WHEAT)

    def addLine(self):
        # untested function
        # sets LINE to: PAIL, GALLON, RETAIL, or TUB
        for key in self.items.keys():
            val = self.items[key]
            self.items[key][LINE] = self.fpl[key][FPL_LINE]
            if self.items[key][LINE] == "DRUM":
                self.items[key][LINE] = "PAIL"
            if self.items[key][LINE] == "POUCH":
                self.items[key][LINE] = "PAIL"

    def addBatchTime(self):
        # Each line hasits  own estimated line speed 
        # This can be adjusted in constants.py
        # Alternatively we might need to do this by pack size because that is a better determinant
        # round to nearest 1/20th : int(((value)+.025)*20)/20
        # a vlaue of 1 is equal to 1 hour
        for key in self.items.keys():
            if self.items[key][LINE] == "PAIL":
                estimate = self.items[key][CPB] / CPH_PAIL 
                self.items[key][TIME_TO_RUN_BATCH] = int(((estimate) + 0.025) * 20) / 20
            elif self.items[key][LINE] == "GALLON":
                estimate = self.items[key][CPB] / CPH_GALLON 
                self.items[key][TIME_TO_RUN_BATCH] = int(((estimate) + 0.025) * 20) / 20
            elif self.items[key][LINE] == "TUB":
                estimate = self.items[key][CPB] / CPH_TUB 
                self.items[key][TIME_TO_RUN_BATCH] = int(((estimate) + 0.025) * 20) / 20
            else: 
                # this should only be reached by the retail line which we are not implementing
                self.items[key][TIME_TO_RUN_BATCH] = 1
                
    def addCasesPerBatch(self):
        # untested function
        # Cases Per Batch = CPB
        # sets CPB = 0.9 * BATCH_WEIGHT(lbs) / CASE_WEIGHT (lbs)
        # This has room for improvement but for now this will work
        # Future work: Detect '/' and split on that to generalize the formula
        # Future work: Detect '#' and use that for pails and pouches
        # Future work: make list of units: oz, lb, gal, drum
        # Skip 12/14floz because only instance is cutomer supplies product so
        # there is
        i = 0
        for key in self.items.keys():
            i = i + 1
            val = self.items[key]
            if self.fpl[key][BATCH_WEIGHT] == "":
                pass
                # skip customer supplies items for now need more information
                # fom tulkoff
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "12/5oz":
                case_weight = (12 * 5) / 16
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "4/8lb":
                case_weight = (4 * 8)
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "2/32oz":
                case_weight = (2 * 32) / 16
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "6/32oz":
                case_weight = (6 * 32) / 16
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "2/1gal":
                # got this number from the internet may not be completely
                # accurate
                case_weight = (2 * 10.4)
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "4/1gal":
                # got this number from the internet may not be completely
                # accurate
                case_weight = (4 * 10.4)
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "4/1galbags":
                # got this number from the internet may not be completely
                # accurate
                case_weight = (4 * 10.4)
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "12/8oz":
                case_weight = (12 * 8) / 16
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "12/9oz":
                case_weight = (12 * 9) / 16
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "12/6oz":
                case_weight = (12 * 6) / 16
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "6/15.5oz":
                case_weight = (6 * 15.5) / 16
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "24/8oz":
                case_weight = (24 * 8) / 16
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "200#drum":
                case_weight = 200
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "400#drum":
                case_weight = 400
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "385#drum":
                case_weight = 385
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "30#pail":
                case_weight = 30
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "35#pail":
                case_weight = 200
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "6/32floz":
                case_weight = (6 * 32) / 16
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "4/123floz":
                case_weight = (4 * 123) / 16
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "12/8floz":
                case_weight = (12 * 8) / 16
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "12/8.25floz":
                case_weight = (12 * 8.25) / 16
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "8/18floz":
                case_weight = (8 * 18) / 16
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "8/20.5oz":
                case_weight = (8 * 20.5) / 16
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "2/30floz":
                case_weight = (2 * 30) / 16
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "12/32floz":
                case_weight = (12 * 32) / 16
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "6/10floz":
                case_weight = (6 * 10) / 16
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "6/16floz":
                case_weight = (6 * 16) / 16
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "6/9floz":
                case_weight = (6 * 9) / 16
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "6/12floz":
                case_weight = (6 * 12) / 16
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "6/30floz":
                case_weight = (6 * 30) / 16
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "6/6.5lbs":
                case_weight = 6 * 6.5
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "4/4.9lbs":
                case_weight = 4 * 4.9
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "4/4.75lbs":
                case_weight = 4 * 4.75
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "4/8.75lbs":
                case_weight = 4 * 8.75
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "4/9.06lbs":
                case_weight = 4 * 9.06
                self.items[key][CPB] = int(
                    0.9 * int(self.fpl[key][BATCH_WEIGHT]) / case_weight)
            else:
                raise Exception("Error: Pack size not found " + self.items[key][PACK_SIZE])

    def addLeadTime():
        # lead time is based on the pdf provided by kingsley
        holds = { '449325': 6, '528136': 6, '230001': 14, '071082': 6, '072037': 6, '461390': 4, 
            '462390': 3, '619276': 1, '628276': 5, '596276': 14, '618276': 14, '070230S': 4, 
            '077356S': 4, '084001S': 4, '529136': 6, '136000': 6, '136059': 6, '136114': 6, 
            '136197': 6, '141036': 6, '236082': 6, '072082': 6, '135059': 6, '135114': 6, 
            '135143': 6, '135197': 6, '140036': 6, '168082': 6, '235082': 6, '235119': 6, 
            '629276': 14, '643276': 14, '528136':6, '034215':6, '045396':6, '110202':6, 
            '189202':6, '456390':6, '461390':6, '464390':6, '462390':6, '597276':6, '073001':6, 
            '045001':6, '125001':6, '152257':6, '045395':6, '073220':6, '535136':6, '073133':6, 
            '045395':6, '045396':6, '085001':6 }
        holdKeys = holds.keys()
        for key in self.items.keys():
            if key in holdKeys:
                self.items[key][LEAD_TIME] = holds[key]


    def getItem(self, itemNumber):
        '''
        Returns the list of cases needed for a particular item.  If the item is not in any list
        it will print return an empty 2d array
        '''
        if itemNumber in self.items.keys():
            return self.items[itemNumber]
        else:
            return None

    def __repr__(self):
        return printDictionary("PL: ", self.items)

    def isItemCode(self, item):
        pattern = r'\b\d{5,6}S?\b'
        return (re.search(pattern, item)) is not None

    def getChangeoverTime(self, item1, item2):
        # check to make sure both items are on th same line
        # check the bottle size is the same
        # check allergen constraints
        # check for same WIP
        # Ask Terrence or Ryan about the process of changing from HRF to HRV
        #   Need to ask about process of changing over to a value product from normal product
        # Possibly add Kosher status to this
        ####################################
        # can be used but is not fully implemented
        ####################################
        if item1 == item2:
            # same product, no changing needed
            return 0
        if self.items[item1][LINE] != self.items[item2][LINE]:
            # not on the same line
            # you cant do this
            return 2 ** 50
        if ((self.items[item1][ROSS_WIP] == self.items[item2][ROSS_WIP]) and (
                self.items[item1][PACK_SIZE] == self.items[item2][PACK_SIZE])):
            return 5
        if self.items[item1][PACK_SIZE] != self.items[item2][PACK_SIZE]:
            # change pack size takes 1 hour
            return 60
        if self.items[item2][ALLERGEN_VALUE] in self.items[item1][ALLERGEN_VALUE]:
            # allergen cleaning is not necessary
            return 30
        else:
            # add 3 for allergen clensing
            return 45


def printDictionary(dicName, dic):
    keys = dic.keys()
    string = '\n' + dicName + '\n'
    for key in dic.keys():
        val = str(dic[key])
        string = string + key + val + '\n'
    return string


if __name__ == "__main__":
    fileName = "productListing.csv"
    savedListing = 'currentListing.txt'

    pl = ProductListing()
    pl.readNewFile(fileName)
    print("TEST")
    print(pl.getItem('064001'))

    pl.saveProductListing(savedListing)

    pl2 = ProductListing()
    pl2.loadProductListing(savedListing)
    # print(pl)
    # print(pl)
    '''
    # use getItem to get all inofmation about an item
    print(pl.getItem('009203'))
    
    # use he constants deifined in constants.py to access specific items in the product listing
    itemdes = pl.getItem('009203')
    print("HI", itemdes)

    print(itemdes[ALLERGEN_VALUE])

    # writing to file
    pl.saveProductListing()

    pl2 = ProductListing()
    pl2.loadProductListing()
    #print(pl2)
    print("Test")
    print(pl.getItem('009203'))
    print(pl2.getItem('009203'))
    assert (1 == 1)
    assert pl.items == pl2.items
    '''
