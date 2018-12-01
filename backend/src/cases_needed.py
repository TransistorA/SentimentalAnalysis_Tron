import re


# TODO   Add detection and calculations on previous materials
#           Need list of items and hold times


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
                    # if first element is a number then it is a item number
                    # check if last char of first col is 'M'
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
                        currentItemNumber = line[0]
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