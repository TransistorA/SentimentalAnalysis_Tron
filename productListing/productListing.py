from datetime import date
import re
import csv
import constants
from enum import Enum
import os
import sys
sys.path.append('../')
from output.Allergen import Allergen

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
            with open(fileName.split('.')[0] + "out.csv", mode='w') as outfile:
                writer = csv.writer(outfile)
                mydict = {}

                for row in reader:
                    if (self.isItemCode(row[0])):
                        mydict[row[0]] = []
                        for elt in row:
                            if elt != row[0]:
                                mydict[row[0]] = mydict[row[0]] + [elt]

            self.items = mydict
            self.expandProductListing()
            self.saveProductListing()
            print(printDictionary("ITEMS", self.items))

    def loadFinishedProductList(self):
        with open("FinishedProductList.csv", mode='r') as infile:
            reader = csv.reader(infile)
            mydict = {}

            for row in reader:
                mydict[row[0]] = row

            self.fpl = mydict

    def loadProductListing(self):
        '''
        Read in an old product listing
        '''

        # hacking that one line function
        self.items = eval(open("currentListing.txt", 'r').read())

    def saveProductListing(self):
        fileName = 'currentListing.txt'
        with open(fileName, 'w+') as wfile:
            wfile.write(str(self.items))

    def expandProductListing(self):
        '''
        Use the dat fromt he file to expand the file to include items such as
        -nozzle used
        -bottle descrambler or other
        -enum based on alergens
        '''
        # add in the extra columns
        for key in self.items.keys():
            # make each item in this the null equvilent
            # Add order: Allergen, LINE, CasesPerBatch

            self.items[key] = self.items[key][0:8] + \
                [Allergen.NONE, "NONE", 0]
        self.addAllergenEnum()
        self.addLine()
        self.addCasesPerBatch()

    def addAllergenEnum(self):
        # untested function
        for key in self.items.keys():
            val = self.items[key]

            if "egg" in val[constants.ALLERGEN].lower():
                val[constants.ALLERGEN_VALUE] = Allergen(val[
                    constants.ALLERGEN_VALUE] + Allergen.EGG)
            if "bisulfite" in val[constants.ALLERGEN].lower():
                val[constants.ALLERGEN_VALUE] = Allergen(val[
                    constants.ALLERGEN_VALUE] + Allergen.BISULFITE)
            if "mustard" in val[constants.ALLERGEN].lower():
                val[constants.ALLERGEN_VALUE] = Allergen(val[
                    constants.ALLERGEN_VALUE] + Allergen.MUSTARD)
            if "milk" in val[constants.ALLERGEN].lower():
                val[constants.ALLERGEN_VALUE] = Allergen(val[
                    constants.ALLERGEN_VALUE] + Allergen.MILK)
            if "fish" in val[constants.ALLERGEN].lower():
                val[constants.ALLERGEN_VALUE] = Allergen(val[
                    constants.ALLERGEN_VALUE] + Allergen.FISH)
            if "anchovy" in val[constants.ALLERGEN].lower():
                val[constants.ALLERGEN_VALUE] = Allergen(val[
                    constants.ALLERGEN_VALUE] + Allergen.FISH)
            if "soy" in val[constants.ALLERGEN].lower():
                val[constants.ALLERGEN_VALUE] = Allergen(int(val[
                    constants.ALLERGEN_VALUE]) + int(Allergen.SOY))
            if "treenut" in val[constants.ALLERGEN].lower():
                val[constants.ALLERGEN_VALUE] = Allergen(val[
                    constants.ALLERGEN_VALUE] + Allergen.TREENUT)
            if "tree nut" in val[constants.ALLERGEN].lower():
                val[constants.ALLERGEN_VALUE] = Allergen(val[
                    constants.ALLERGEN_VALUE] + Allergen.TREENUT)
            if "wheat" in val[constants.ALLERGEN].lower():
                val[constants.ALLERGEN_VALUE] = Allergen(val[
                    constants.ALLERGEN_VALUE] + Allergen.WHEAT)

    def addLine(self):
        # untested function
        # sets LINE to: PAIL, GALLON, RETAIL, or TUB
        for key in self.items.keys():
            val = self.items[key]
            self.items[key][constants.LINE] = self.fpl[key][constants.FPL_LINE]
            if self.items[key][constants.LINE] == "DRUM":
                self.items[key][constants.LINE] = "PAIL"
            if self.items[key][constants.LINE] == "POUCH":
                self.items[key][constants.LINE] = "PAIL"

    def addBatchTime(self):
        # for now we are just assigning 30 minutes to a batch but we will change this later
        for key in self.items.keys():
            # for now all batches take 30 minutes to complete
            self.items[key][constants.TIME_TO_RUN_BATCH] = 6

    def addCasesPerBatch(self):
        # untested function
        # Cases Per Batch = CPB 
        # sets CPB = 0.9 * BATCH_WEIGHT(lbs) / CASE_WEIGHT (lbs)
        # This has room for improvement but for now this will work
        # Future work: Detect '/' and split on that to generalize the formula
        # Future work: Detect '#' and use that for pails and pouches
        # Future work: make list of units: oz, lb, gal, drum
        # Skip 12/14floz because only instance is cutomer supplies product so there is
        i = 0
        for key in self.items.keys():
            i = i + 1
            val = self.items[key]
            if self.fpl[key][constants.BATCH_WEIGHT] == "":
                pass
                # skip customer supplies items for now need more information fom tulkoff
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "12/5oz":
                case_weight = (12 * 5) / 16
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "4/8lb":
                case_weight = (4 * 8)
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "2/32oz":
                case_weight = (2 * 32) / 16
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "6/32oz":
                case_weight = (6 * 32) / 16
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "2/1gal":
                case_weight = (2 * 10.4) # got this number from the internet may not be completely accurate
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "4/1gal":
                case_weight = (4 * 10.4) # got this number from the internet may not be completely accurate
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "4/1galbags":
                case_weight = (4 * 10.4) # got this number from the internet may not be completely accurate
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "12/8oz":
                case_weight = (12 * 8) / 16
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "12/9oz":
                case_weight = (12 * 9) / 16
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "12/6oz":
                case_weight = (12 * 6) / 16
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "6/15.5oz":
                case_weight = (6 * 15.5) / 16
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "24/8oz":
                case_weight = (24 * 8) / 16
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "200#drum":
                case_weight = 200
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "400#drum":
                case_weight = 400
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "385#drum":
                case_weight = 385
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "30#pail":
                case_weight = 30
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "35#pail":
                case_weight = 200
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "6/32floz":
                case_weight = (6 * 32) / 16
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "4/123floz":
                case_weight = (4 * 123) / 16
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "12/8floz":
                case_weight = (12 * 8) / 16
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "12/8.25floz":
                case_weight = (12 * 8.25) / 16
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "8/18floz":
                case_weight = (8 * 18) / 16
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "8/20.5oz":
                case_weight = (8 * 20.5) / 16
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "2/30floz":
                case_weight = (2 * 30) / 16
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "12/32floz":
                case_weight = (12 * 32) / 16
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "6/10floz":
                case_weight = (6 * 10) / 16
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "6/16floz":
                case_weight = (6 * 16) / 16
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "6/9floz":
                case_weight = (6 * 9) / 16
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "6/12floz":
                case_weight = (6 * 12) / 16
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "6/30floz":
                case_weight = (6 * 30) / 16
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "6/6.5lbs":
                case_weight = 6 * 6.5
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "4/4.9lbs":
                case_weight = 4 * 4.9
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "4/4.75lbs":
                case_weight = 4 * 4.75
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "4/8.75lbs":
                case_weight = 4 * 8.75
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            elif self.items[key][constants.PACK_SIZE].lower().replace(" ", "") == "4/9.06lbs":
                case_weight = 4 * 9.06
                self.items[key][constants.CPB] = int(0.9 * int(self.fpl[key][constants.BATCH_WEIGHT]) / case_weight)
            else:
                print(self.items[key])
                print(self.items[key][constants.PACK_SIZE].lower(), i)
                raise Exception("Error")

    def getItem(self, itemNumber):
        '''
        Retruns the list of cases needed for a particular item.  If the item is not in any list 
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
        return (re.search(pattern, item)) != None

    def getChangeoverTime(item1, item2):
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
        if self.items[item1][constants.LINE] != self.items[item2][constants.LINE]:
            # not on the same line
            # you cant do this
            return 2 ** 50
        if ((self.items[item1][constants.ROSS_WIP] == self.items[item2][constants.ROSS_WIP]) and (self.items[item1][constants.PACK_SIZE] == self.items[item2][constants.PACK_SIZE])):
            return 1
        if (self.items[item1][constants.PACK_SIZE] != self.items[item2][constants.PACK_SIZE]):
            # change pack size takes 1 hour
            return 12
        if (self.items[item2][constants.ALLERGEN_VALUE] in self.items[item1][constants.ALLERGEN_VALUE]):
            # allergen cleaning is not necessary
            return 6
        else:
            # add 3 for allergen clensing
            return 9
        

def printDictionary(dicName, dic):
    keys = dic.keys()
    string = '\n' + dicName + '\n'
    for key in dic.keys():
        val = str(dic[key])
        print(type(key))
        string = string + key + val + '\n'
    return string

if __name__ == "__main__":

    fileName = "productListing.csv"
    pl = ProductListing()
    pl.readNewFile(fileName)
    print("TEST")

    # print(pl)
    '''
    # use getItem to get all inofmation about an item
    print(pl.getItem('009203'))
    
    # use he constants deifined in constants.py to access specific items in the product listing
    itemdes = pl.getItem('009203')
    print("HI", itemdes)

    print(itemdes[constants.ALLERGEN_VALUE])

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
