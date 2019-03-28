import csv
import io
import datetime as dt

from allergen import Allergen


class Schedule:
    """a schedule object"""

    def __init__(self, date):
        if isinstance(date, dt.datetime):
            self.date = date.strftime("%A, %b %d, %Y")
        elif isinstance(date, str):
            self.date = date
        else:
            raise Exception('Invalid schedule date {}'.format(date))

        self.pail = []
        self.tub = []
        self.gallon = []
        self.retail = []

    def addItemToLine(self, lineStr, scheduleItem):
        lineStr = lineStr.upper()
        LINES = {
            'PAIL': self.pail,
            'TUB': self.tub,
            'GALLON': self.gallon,
            'RETAIL': self.retail
        }
        LINES[lineStr].append(scheduleItem)

    def __repr__(self):
        colStr = '{:<10}'.format('Item #') + '{:<20}'.format('Label') \
                 + '{:<15}'.format('Product') + '{:<15}'.format('Pack Size') \
                 + '{:<7}'.format('Cases') + '{:<10}'.format('Ross #') \
                 + '{:<10}'.format('Batches') + '{:<15}'.format('Allergens') \
                 + '{:<15}'.format('Non-K') + '{:<15}'.format('StartTime')
        schedule = '{:^114}'.format("Production Schedule") + '\n' \
                   + "Date: {self.date} \n".format(self=self)
        schedule += '\n' + '{:^114}'.format("Tub Line") + '\n' + colStr + '\n'
        for item in self.tub:
            schedule += str(item)
        schedule += '\n' + '{:^114}'.format("Pail/Drum/Pouch Line") + '\n' \
                    + colStr + '\n'
        for item in self.pail:
            schedule += str(item)
        schedule += '\n' + '{:^114}'.format("Gallon Line") + '\n' \
                    + colStr + '\n'
        for item in self.gallon:
            schedule += str(item)
        schedule += '\n' + '{:^114}'.format("Retail Line") + '\n' \
                    + colStr + '\n'
        for item in self.retail:
            schedule += str(item)
        return schedule

    def toCSV(self):
        csv = ['Production Schedule']
        csv.append('Date: {}'.format(self.date))

        cols = ['Item #', 'Label', 'Product', 'Pack Size', 'Cases',
                'Ross #', 'Batches', 'Allergens', 'Kosher Status',
                'Start Time (Hrs)']
        csv.append(','.join(cols))

        LINES = {
            'Tub': self.tub,
            'Pail/Drum/Pouch': self.pail,
            'Gallon': self.gallon,
            'Retail': self.retail
        }
        for lineStr, line in LINES.items():
            csv.append('')
            csv.append('{} Line'.format(lineStr))
            for item in line:
                csv.append(item.toCSV())

        return '\n'.join(csv)


class ScheduleItem:
    """an item in the schedule"""

    def __init__(self,
                 itemNum,
                 label,
                 product,
                 packSize,
                 cases,
                 rossNum,
                 batches,
                 allergens,
                 kosher,
                 starttime):
        self.itemNum = itemNum
        self.label = label
        self.product = product
        self.packSize = packSize
        self.cases = cases
        self.rossNum = rossNum
        self.batches = batches
        self.allergens = allergens
        self.kosher = kosher  # whether item is kosher or not
        self.starttime = starttime

    def _getAllergenStr(self):
        allergensStr = []
        for item in self.allergens:
            allergensStr.append(item.name.capitalize())
        return ', '.join(allergensStr)

    def toCSV(self):
        allergenStr = self._getAllergenStr()
        kosherStr = "Kosher" if self.kosher else "Non-Kosher"

        vals = [self.itemNum, self.label, self.product, self.packSize,
                self.cases, self.rossNum, self.batches, allergenStr,
                kosherStr, self.starttime]

        # https://stackoverflow.com/a/35319592/4103546
        output = io.StringIO()
        writer = csv.writer(output, lineterminator='')
        writer.writerow(vals)

        return output.getvalue()

    def __repr__(self):
        allergenStr = self._getAllergenStr()
        kosherStr = "Kosher" if self.kosher else "Non-Kosher"

        return ('{self.itemNum:<10}{self.label:<20}{self.product:<15}'
                + '{self.packSize:<15}{self.cases:<7}{self.rossNum:<10}'
                + '{self.batches:<10}{allergenStr:<15}{kosherStr:<15}'
                + '{self.starttime:<15}\n').format(self=self,
                                                   allergenStr=allergenStr,
                                                   kosherStr=kosherStr)


if __name__ == "__main__":
    a = Schedule("10/14/18")
    a.tub.append(ScheduleItem(itemNum='009057',
                              label='cobbmkt originals',
                              product='apple',
                              packSize='1/1oz',
                              cases=100,
                              rossNum='10',
                              batches='1',
                              allergens=[Allergen.EGG, Allergen.BISULFITE],
                              kosher=True))

    print(a)
