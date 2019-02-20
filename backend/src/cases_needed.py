import re
from datetime import date
from datetime import timedelta

# TODO   Add detection and calculations on previous materials
#           Need list of items and hold times

hold_dictionary = { '449325': 6, '528136': 6, '230001': 14, '071082': 6, '072037': 6, '461390': 4, 
            '462390': 3, '619276': 1, '628276': 5, '596276': 14, '618276': 14, '070230S': 4, 
            '077356S': 4, '084001S': 4, '529136': 6, '136000': 6, '136059': 6, '136114': 6, 
            '136197': 6, '141036': 6, '236082': 6, '072082': 6, '135059': 6, '135114': 6, 
            '135143': 6, '135197': 6, '140036': 6, '168082': 6, '235082': 6, '235119': 6, 
            '629276': 14, '643276': 14, '528136':6, '034215':6, '045396':6, '110202':6, 
            '189202':6, '456390':6, '461390':6, '464390':6, '462390':6, '597276':6, '073001':6, 
            '045001':6, '125001':6, '152257':6, '045395':6, '073220':6, '535136':6, '073133':6, 
            '045395':6, '045396':6, '085001':6 }
        
class CasesNeeded:

    def __init__(self):
        # create each lines dictionary
        # each key in the dictionary is an item number
        # the value is a 3-tuple of (date, case in order, running total)
        self.pail = {}
        self.tub = {}
        self.gallon = {}
        self.retail = {}

        # stock keeps track of items in warehouse
        # indexed by item number and contains list of tuples (lotcode, number)
        self.stock = {}

    def readFile(self, fileName):
        # Tub is first
        dic = self.tub

        currentItemNumber = None
        with open(fileName) as file:
            for line in file:
                # split up by comma
                line = line.split(",")

                # check for end of section and swap dictionaries as needed
                if line[0] == "Gallon":
                    self.tub = dic
                    dic = {}
                elif line[0] == "Pail":
                    self.gallon = dic
                    dic = {}
                elif line[0] == "Retail":
                    self.pail = dic
                    dic = {}
                elif line[0] == "Purchased":
                    self.retail = dic
                    dic = {}

                # check if the line is items on hand vs order vs item number
                # one element lists are empty lines
                if len(line) > 1:
                    # if first element is a number then it is a item number
                    # check if last char of first col is 'M'
                    if self.isLotCode(line[0]):
                        stock[currentItemNumber] = stock[currentItemNumber] + [(line[0],  line[2])]
                    elif self.isDate(line[0]):
                        extra = 0
                        if len(dic[currentItemNumber]) != 0:
                            extra = int(dic[currentItemNumber][-1][-1])

                        if len(line) == 7:  # split normally
                            total = int(line[3][1:-1])
                            cases = total - extra
                        else:
                            # This is bad but I can't think of a better way to
                            # deal with weird comma shit
                            total = int("".join(line).replace("(", ")").split(")")[1])
                            cases = total - extra

                        # if date already in dictionary
                        if len(dic[currentItemNumber]) != 0 and dic[currentItemNumber][-1][0] == line[0]:
                            cases = cases + dic[currentItemNumber][-1][1]
                            dic[currentItemNumber][-1] = (line[0], cases, total)
                        else:
                            dic[currentItemNumber] = dic[currentItemNumber] + [(line[0], cases, total)]
                    elif self.isItemCode(line[0]):
                        currentItemNumber = line[0]

                        # create empty lists in dictionaries to prevent key not found errors
                        dic[currentItemNumber] = []
                        stock[currentItemNumber] = []

        # update the items that have hold times
        for itemNumber in hold_dictionary:
            # determine which line the product is run on and pass info to update
            if itemNumber in self.tub:
                self.tub[itemNumber] = self.updateItemStock(itemNumber, hold_dictionary[itemNumber], self.tub[itemNumber])
            elif itemNumber in self.gallon:
                self.gallon[itemNumber] = self.updateItemStock(itemNumber, hold_dictionary[itemNumber], self.gallon[itemNumber])
            elif itemNumber in self.pail:
                self.pail[itemNumber] = self.updateItemStock(itemNumber, hold_dictionary[itemNumber], self.pail[itemNumber])
            elif itemNumber in self.retail:
                self.retail[itemNumber] = self.updateItemStock(itemNumber, hold_dictionary[itemNumber], self.retail[itemNumber])
            

    def updateItemStock(self, itemNumber, stock, orders):
        itemStock = stock[itemNumber] # list of products
        for i in range(len(itemStock)):
         
        # calculate hold date
        readyDate = date(date.today().year, 1, 1)
        days = stock[]
        readyDate = readyDate  + timedelta(days=days) 
        # if ready date is in the past 
        #    then skip
        # if ready date is in the future, 
        #    start subtracting from the future dates
        return line

    def getItem(self, itemNumber):
        """
        Returns the list of cases needed for a particular item. If the item is not in any list
        it will print return an empty 2d array
        :param itemNumber [string]
        """
        if not itemNumber:
            return []
        itemNumber = itemNumber.strip()

        if itemNumber in self.pail:
            return self.pail[itemNumber]
        elif itemNumber in self.tub:
            return self.tub[itemNumber]
        elif itemNumber in self.gallon:
            return self.gallon[itemNumber]
        elif itemNumber in self.retail:
            return self.retail[itemNumber]
        else:
            return []

    def getItemsPail(self):
        numBatches = 0
        itemNumbers = []
        dueDates = []

        for itemNum in self.pail:
            numBatches += len(self.pail[itemNum])
            for item in self.pail[itemNum]:  # item here is a tuple of due dates, case in order and running total
                itemNumbers.append(itemNum)
                dueDates.append(item[0])

        return numBatches, itemNumbers, dueDates

    def getNumTub(self):
        numBatches = 0
        for item in self.tub:
            numBatches += len(self.tub[item])
        return numBatches

    def getNumGallon(self):
        numBatches = 0
        for item in self.gallon:
            numBatches += len(self.gallon[item])
        return numBatches

    def getNumRetail(self):
        numBatches = 0
        for item in self.retail:
            numBatches += len(self.retail[item])
        return numBatches

    def __repr__(self):
        result = []
        for dicName, dic in [('Pail', self.pail),
                             ('Tub', self.tub),
                             ('Gallon', self.gallon),
                             ('Retail', self.retail)]:
            result.append('\n{}:'.format(dicName))
            result.append(printDictionary(dic))
        return '\n'.join(result)

    def isLotCode(self, string):
        pattern = r'\d{3,}M'
        return (re.search(pattern, string)) is not None

    def isDate(self, string):
        if len(string) > 15:
            return False
        pattern = r'\d{1,2}\/\d{1,2}\/\d{4}'
        return (re.search(pattern, string)) is not None

    def isItemCode(self, item):
        pattern = r'\b\d{5,6}S?\b'
        return (re.search(pattern, item)) is not None


def printDictionary(dic):
    result = []
    for key, val in dic.items():
        result.append("{}: {}".format(key, val))
    return '\n'.join(result)
