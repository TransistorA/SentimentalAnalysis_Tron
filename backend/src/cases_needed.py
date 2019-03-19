import re

class CasesNeeded:

    def __init__(self):
        # create each lines dictionary
        # each key in the dictionary is an item number
        # the value is a 3-tuple of (date, case in order, running total)
        self.pail = {}
        self.tub = {}
        self.gallon = {}
        self.retail = {}

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
                    if self.isLotCode(line[0]):
                        pass  # TODO: address lot code
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
                        # set currentItemNumber the the new item code
                        currentItemNumber = line[0]

                        # create new entry in the dictionary
                        dic[currentItemNumber] = []



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
        '''
        numBatches: The number of batches required to fulfill the orders for each item
        itemNumbers: Item number that corresponds to the date in the dueDates list
        dueDates: Date each item is due
        '''
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



    '''
    Repr function for the cases needed
    For debugging purposes only at the moment
    '''
    def __repr__(self):
        # Consider rearranging this method
        result = []
        for dicName, dic in [('Pail', self.pail),
                             ('Tub', self.tub),
                             ('Gallon', self.gallon),
                             ('Retail', self.retail)]:
            result.append('\n{}:'.format(dicName))
            result.append(printDictionary(dic))
        return '\n'.join(result)

    '''
    Regular Expression methods for determining the purpose  
    of the row in the casesneeded.csv file
    '''
    def isLotCode(self, string):
        # look for 3 or more numbers then the letter M
        pattern = r'\d{3,}M'
        return (re.search(pattern, string)) is not None

    def isDate(self, string):
        # go back and find out why this was done
        if len(string) > 15: 
            return False
        # look for MM/DD/YYYY
        pattern = r'\d{1,2}\/\d{1,2}\/\d{4}'
        return (re.search(pattern, string)) is not None

    def isItemCode(self, item):
        # Loo for 5 digit number and then possibly  an 'S'
        pattern = r'\b\d{5,6}S?\b'
        return (re.search(pattern, item)) is not None

    def getLineObj(self, lineStr):
        lineStr = lineStr.upper()
        LINES = {
            'PAIL': self.pail,
            'TUB': self.tub,
            'GALLON': self.gallon,
            'RETAIL': self.retail
        }
        return LINES[lineStr]


def printDictionary(dic):
    result = []
    for key, val in dic.items():
        result.append("{}: {}".format(key, val))
    return '\n'.join(result)
