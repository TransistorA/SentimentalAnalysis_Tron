from datetime import date
import re
import csv
import constants
from enum import Enum
import AllergenEnum
import os


# TODO   Add detection and calculations on previous materials
#           Need list of items and hold times


class ProductListing:

    def __init__(self):
        # create each lines dictionary
        # each key in the dictionary is an item number
        # the value is a 3-tuple of (date, case in order, running total)
        self.items = {}

    def readNewFile(self, fileName):
        with open(fileName, mode='r') as infile:
            reader = csv.reader(infile)
            with open(fileName.split('.')[0] + "out.csv", mode='w') as outfile:
                writer = csv.writer(outfile)
                mydict = {}

                for row in reader:
                    if (self.isDigit(row[0])):
                        mydict[row[0]] = []
                        for elt in row:
                            if elt != row[0]:
                                mydict[row[0]] = mydict[row[0]] + [elt]

            self.items = mydict
            self.expandProductListing()
            self.saveProductListing()


    def loadProductListing(self):
        '''
        Read in an old product listing
        '''

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
            self.items[key] = self.items[key] + \
                ["Allergen enum", "nozzle type", "WIP source"]
        self.addAllergenEnum()

        # To be implemented when I have the information
        # self.addNozzles()
        # self.addWIPSource()

        # Add in other columns for now with junk values then add the actual
        # values later

    def addAllergenEnum(self):
        # TODO: ADD allergens once I get he allergen enum that Junjie was
        # working on
        pass

        '''
        for allergen in list(AllergenEnum.AllergenEnum):
            # check for each type of allergen in the allergen category using re
            allergenValue = allergen.value
            allergenName = allergen.name
            if (len(self.items[key])<constants.ALLERGEN_VALUE):
                self.items[key][constants]
            self.items[key][constants.ALLERGEN_VALUE] = 0
            if allergenName in self.items[key][constants.ALLERGEN].upper():
                print(allergenName)
                self.items[key][constants.ALLERGEN_VALUE] = AllergenEnum.allergenName.addALLERGEN(
                    self.items[key][constants.ALLERGEN_VALUE])
            # add to array
        '''

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

    def isDigit(self, item):
        pattern = r'\b\d{5,6}S?\b'
        return (re.search(pattern, item)) != None


def printDictionary(dicName, dic):
    keys = dic.keys()
    string = '\n' + dicName + '\n'
    for key in keys:
        print(type(key))
        string = string + key + str(dic[key]) + '\n'
    return string

if __name__ == "__main__":
    fileName = "productListing.csv"
    pl = ProductListing()
    pl.readNewFile(fileName)
    print("TEST")
    #print(pl)
    
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

