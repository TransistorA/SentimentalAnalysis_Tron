import csv
import os
import re

import jsonpickle

from allergen import Allergen
from constants import *


# TODO   Add detection and calculations on previous materials


class ProductListing:

    def __init__(self):
        
        # Product Listing
        self.items = {}

        # Finished Product Listing
        self.fpl = {}  

        # fpl stored in src folder
        self.loadFinishedProductList()

    def readNewFile(self, fileName):
        '''
        Open filename and create a dictionary with each item numbers product information
        saves the information to self.items
        calls expandProductlisting to generate usable information
        '''
        with open(fileName, mode='r') as infile:
            reader = csv.reader(infile)
            mydict = {}

            # iterate over each line in the file
            for row in reader:
                # filter out irrelevent lines
                if (len(row) > 1) and self.isItemCode(row[0]):
                    mydict[row[0]] = []\
                    # append all information to the coresponding key in dictionary
                    for elt in row:
                        if elt != row[0]:
                            mydict[row[0]] = mydict[row[0]] + [elt]

            # assign to self.items
            self.items = mydict

            # generate usable information
            self.expandProductListing()
            
    def loadFinishedProductList(self):
        '''
        load the finished product listing to get extra product information
        called by the constructor
        '''
        fplFilename = os.path.join(os.path.dirname(__file__),
                                   'FinishedProductList.csv')
        with open(fplFilename, mode='r') as infile:
            reader = csv.reader(infile)
            mydict = {}

            for row in reader:
                mydict[row[0].strip()] = row

            self.fpl = mydict

    def saveProductListing(self, filename):
        '''
        currently this function has no usage
        '''
        outfile = open(filename, 'a')
        outfile.write(jsonpickle.encode(self.items))
        outfile.close

    def loadProductListing(self, filename):
        '''
        currently this function has no usage
        '''
        outfile = open(filename, 'r')
        stuff = jsonpickle.decode(str(self.items))
        outfile.close
        self.items = stuff

    def getCasesPerBatch(self, itemNumber):
        # returns the number of cases produced from 1 batch
        return self.items[itemNumber][CPB]

    def getBatchTime(self, itemNumber):
        # returns the amount of time (in hours) to run one batch
        return self.items[itemNumber][TIME_TO_RUN_BATCH]

    def expandProductListing(self):
        '''
        Use the data from the file to expand the file to include items such as
        - convert the alergen to an enum
        - which line the product is run on
        - How many cases can be made from 1 batch
        - how long does it take to run 1 batch
        - how long does the product go on hold for
        '''
        # add in the extra columns
        for key in self.items.keys():
            # make each item in this equvilent to null
            # Add order: Allergen, LINE, CasesPerBatch, Batch run time, product
            # lead time
            self.items[key] = self.items[key][0:8] + \
                [Allergen.NONE, "NONE", 0, 0, 0]

        # call each individual function to update the new columns
        self.addAllergenEnum()
        self.addLine()
        self.addCasesPerBatch()
        
        self.addBatchTime()
        self.addLeadTime()

    def addAllergenEnum(self):
        # create the allergen enum and store it in the ALLERGEN_VALUE
        # all alergens are initialized to NONE and additional allergens are
        # added
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
        '''
        sets LINE to: PAIL, GALLON, RETAIL, or TUB
        '''
        for key in list(self.items.keys()):
            val = self.items[key]
            try:
                self.items[key][LINE] = self.fpl[key][FPL_LINE]
                if self.items[key][LINE] == "DRUM":
                    self.items[key][LINE] = "PAIL"
                if self.items[key][LINE] == "POUCH":
                    self.items[key][LINE] = "PAIL"

            except KeyError:
                print("addLine(): Key not found in FPL: " + key)
                
    def addBatchTime(self):
        # Each line has its own estimated line speed
        # This can be adjusted in constants.py
        # Alternatively we might need to do this by pack size because that is a better determinant
        # TIME_TO_RUN_BATCH: 1 = 1 hour, 0.05 = 3 minutes
        for key in self.items.keys():
            if self.items[key][LINE] == "PAIL":
                estimate = self.items[key][CPB] / CPH_PAIL
                self.items[key][TIME_TO_RUN_BATCH] = self.round(estimate)
            elif self.items[key][LINE] == "GALLON":
                estimate = self.items[key][CPB] / CPH_GALLON
                self.items[key][TIME_TO_RUN_BATCH] = self.round(estimate)
            elif self.items[key][LINE] == "TUB":
                estimate = self.items[key][CPB] / CPH_TUB
                self.items[key][TIME_TO_RUN_BATCH] = self.round(estimate)
            else:
                # this should only be reached by the retail line which we are
                # not implementing
                self.items[key][TIME_TO_RUN_BATCH] = 1

    def round(self, number):
        # rounds number to the nearest 20th
        # used by the addBatchTime function
        return int((number + 0.025) * 20) / 20

    def addCasesPerBatch(self):
        # Cases Per Batch = CPB
        # sets CPB = 0.9 * BATCH_WEIGHT(lbs) / CASE_WEIGHT (lbs)
        # This has room for improvement but for now this will work
        # Future work: Detect '/' and split on that to generalize the formula
        # Future work: Detect '#' and use that for pails and pouches
        # Future work: make list of units: oz, lb, gal, drum
        # Skip 12/14floz because only instance is cutomer supplies product so
        # there is
        # Use this regular Expression:
        # TODO: implement the regular expression
        # TODO: possibly add optional whitespaces to the regular expresion use "\s*" between everything
        # TODO: make the regular expresion not care about capital letters (see
        # "i flag")
        pattern = r"(\d+)(?:(?:/(\d+(?:.\d+)?)(oz|lbs?|galbags|gal|floz))|(?:#(drum|pail)))"
        # TODO: test out group selection and figure out 2/3 vs 4 so it knows
        # how to make calcuation
        i = 0
        for key in self.items.keys():
            try:
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
                elif self.items[key][PACK_SIZE].lower().replace(" ", "") == "375#drum":
                    case_weight = 375
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
                    raise Exception("Error: Pack size not found " +
                                    self.items[key][PACK_SIZE])
            except:
                print("No weight found for item " + key + " and WIP " + self.items[key][ROSS_WIP])

    def addLeadTime(self):
        '''
        adds lead time to self.items using the  holds dictionary
        '''
        holds = {
            '070230S': 4, '077356S': 4, '084001S': 4, '449325': 6, '528136': 6, '230001': 14, '071082': 6,
            '136000': 6, '136059': 6, '136114': 6, '136197': 6, '141036': 6, '236082': 6, '072037': 6,
            '072082': 6, '135059': 6, '135114': 6, '135143': 6, '135197': 6, '140036': 6, '529136': 6,
            '168082': 6, '235082': 6, '235119': 6, '461390': 4, '462390': 3, '619276': 1, '628276': 5,
            '596276': 14, '618276': 14,  '629276': 14, '643276': 14
        }
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
            raise Exception("Error: Item not found "+ itemNumber)

    def __repr__(self):
        # for dubugging purposes
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
    print("pl.getItem('009037')")
    print(pl.getItem('009037'))
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
