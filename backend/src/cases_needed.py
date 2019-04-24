import re
from datetime import date
from datetime import datetime
from datetime import timedelta
from time import strptime
from time import mktime


# we might want to double the numbers to try and ge these things schecduled so they vcan be remade
# this will be a later thing
hold_dictionary = {
    '070230S': 4, '077356S': 4, '084001S': 4, '449325': 6, '528136': 6, '230001': 14, '071082': 6,
    '136000': 6, '136059': 6, '136114': 6, '136197': 6, '141036': 6, '236082': 6, '072037': 6,
    '072082': 6, '135059': 6, '135114': 6, '135143': 6, '135197': 6, '140036': 6, '529136': 6,
    '168082': 6, '235082': 6, '235119': 6, '461390': 4, '462390': 3, '619276': 1, '628276': 5,
    '596276': 14, '618276': 14,  '629276': 14, '643276': 14
}


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
        self.todaysDate = date.today()

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
                        # save lot code, number tuples
                        if currentItemNumber in hold_dictionary:  # only save the items that need to go on hold
                            # get rest of line because of the seperating by commas thing
                            # merge the line with join
                            # strip any excess quotiation marks
                            # convert to int
                            numInStock = int("".join(line[2:-1]).strip('"'))
                            self.stock[currentItemNumber] = self.stock[
                                currentItemNumber] + [(line[0], line[1], numInStock)]

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
                            total = int("".join(line).replace(
                                "(", ")").split(")")[1])
                            cases = total - extra

                        # if date already in dictionary
                        if len(dic[currentItemNumber]) != 0 and dic[currentItemNumber][-1][0] == line[0]:
                            cases = cases + dic[currentItemNumber][-1][1]
                            dic[currentItemNumber][-1] = (line[0],
                                                          cases, total)
                        else:
                            dic[currentItemNumber] = dic[
                                currentItemNumber] + [(line[0], cases, total)]
                    elif self.isItemCode(line[0]):
                        # set currentItemNumber the the new item code
                        currentItemNumber = line[0]
                        # create empty lists in dictionaries to prevent key not
                        # found errors
                        dic[currentItemNumber] = []
                        if currentItemNumber in hold_dictionary:
                            self.stock[currentItemNumber] = []
                    elif (line[0][:8] == "Printed:"):
                        line = line[0].split(" ")
                        self.todaysDate = strptime(line[1], '%m/%d/%Y')
                        self.todaysDate = datetime.fromtimestamp(
                            mktime(self.todaysDate)).date()

        # update the items that have hold times
        for itemNumber in hold_dictionary:
            # determine which line the product is run on and pass info to
            # update
            if itemNumber in self.tub:
                self.tub[itemNumber] = self.updateItemStock(
                    itemNumber, hold_dictionary[itemNumber], self.tub[itemNumber])
            elif itemNumber in self.gallon:
                self.gallon[itemNumber] = self.updateItemStock(
                    itemNumber, hold_dictionary[itemNumber], self.gallon[itemNumber])
            elif itemNumber in self.pail:
                self.pail[itemNumber] = self.updateItemStock(
                    itemNumber, hold_dictionary[itemNumber], self.pail[itemNumber])
            elif itemNumber in self.retail:
                self.retail[itemNumber] = self.updateItemStock(
                    itemNumber, hold_dictionary[itemNumber], self.retail[itemNumber])

    def updateItemStock(self, itemNumber, holdDays, orders):
        # itemNumber = itemNumber
        # hold_days is the number of days item goes on hold before ready
        # orders are the orders for the item (this is what needs to be updated
        # and returned)
        if (itemNumber == 596276):
            print("specialcase")

        # push forward ship date by hold time to ensure products are produced
        # in advanced
        orders = self.adjustOrderDates(itemNumber, orders)

        # get list of products in stock
        itemStock = self.stock[itemNumber]

        # return with no alteration if nothing in stock
        if itemStock == []:
            return orders

        # iterate through all items in stock
        for i in range(len(itemStock)):
            # calculate readyDate
            readyDate = self.getReadyDate(
                itemStock[i][0], itemNumber, itemStock[i][1])

            # get the current date which is saved globally
            compareDate = self.todaysDate

            if (compareDate > readyDate):
                # if the stock item is already ready then we dont need to
                # acount for it in code
                continue
            else:
                # subtract from the orders the item in stock waiting to be released
                # iterate until we have accounted for all items in stock
                # or there are no more orders
                while (len(orders) != 0 and itemStock[i][2] != 0):
                    # loop until all orders have been fulfilled or
                    # we have alloted all of itemStock[i]
                    if orders[0][2] > itemStock[i][2]:
                        # not enough to cover order, subtract and exit  while
                        # loop
                        updatedAmount = orders[0][2] - itemStock[i][2]
                        orders = self.updateOrder(orders, updatedAmount)
                        itemStock[i] = (0, 0, 0)
                    else:
                        # enough in stock to cover order
                        # reduce item stock and the running total for orders by
                        # the amount in the first order
                        itemStock[i] = (itemStock[i][0], itemStock[i][
                                        1], itemStock[i][2] - orders[0][2])
                        amountToReduce = orders[0][2]
                        orders = orders[1:]
                        orders = self.updateOrder(orders, amountToReduce)

            return orders

    def updateOrder(self, orders, amountToReduce):
        '''
        takes in the list of orders and the quinitiy to be reduced by
        outputs the same orders but adjusts the running totals for the orders
        '''
        for i in range(len(orders)):
            newRunningTotal = orders[i][2] - amountToReduce
            orders[i] = (orders[i][0], orders[i][1], newRunningTotal)
        return orders

    def getReadyDate(self, lotCode, itemNumber, percentage):
        '''
        takes in a lot code and the number of days the product is on hold
        returns a date object with the date that the product can be shipped
        '''

        # calculate the production date based on the lot code
        if len(lotCode) == 9:
            readyDate = date(int(lotCode[4:8]), int(
                lotCode[0:2]), int(lotCode[2:4]))
        elif len(lotCode) == 7:
            readyDate = date(
                2000 + int(lotCode[4:6]), int(lotCode[0:2]), int(lotCode[2:4]))
        elif len(lotCode) == 5:
            # get year from first digit
            # this will stop working in 2027 but it wont be in use by then
            if int(lotCode[0]) > 7:
                year = 2010 + int(lotCode[0])
            else:
                year = 2020 + int(lotCode[0])
            readyDate = date(year, 1, 1)
            readyDate = readyDate + timedelta(days=int(lotCode[1:-1]) - 1)
        elif len(lotCode) == 10:
            # MMMDDYYXXX
            # this lotcode is 365 days in advanced so subtract 1 year
            readyDate = strptime(lotCode[:-3], '%b%d%y')
            readyDate = datetime.fromtimestamp(mktime(readyDate)).date()
            readyDate = readyDate - timedelta(days=365)
        else:
            # catch all other lot codes and hopefully find errors sooner
            raise Exception("Lotcode not recognized")

        # adjust dates for lotcodes that are futute / expiration dates
        today = self.todaysDate
        if readyDate > today + timedelta(days=180):
            print("subtract 180")
            readyDate = readyDate - timedelta(days=360)
        elif readyDate > today + timedelta(days=90):
            print("subtract 90")
            readyDate = readyDate - timedelta(days=180)
        elif readyDate > today + timedelta(days=30):
            print("subtract 90")
            readyDate = readyDate - timedelta(days=90)

        # add hold times to the dates and return
        return readyDate + timedelta(days=hold_dictionary[itemNumber])

    def adjustOrderDates(self, itemNumber, orders):
        ''' 
        adjusts order dates by product hold times
        takes in the item number and the list of orders
        outputs the same list of orders but the dates are pushed forward by the nimber of hold days
        This ensures that the products are produced in advanced
        '''
        days = hold_dictionary[itemNumber]
        for i in range(len(orders)):
            date = strptime(orders[i][0], ' %m/%d/%Y')
            date = datetime.fromtimestamp(mktime(date)).date()
            date = date - timedelta(days=days)
            date = date.strftime('%m/%d/%Y')
            orders[i] = (date, orders[i][1], orders[i][2])
        return orders

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
            # item here is a tuple of due dates, case in order and running
            # total
            for item in self.pail[itemNum]:
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
        pattern = r'(\d{4,8}M)|(\w{3}\d{4})'
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
