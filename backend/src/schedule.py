from allergen import Allergen


class Schedule:
    """a schedule object"""

    def __init__(self, date):
        self.date = date
        self.tub = []
        self.pail = []
        self.gallon = []
        self.retail = []

    def __repr__(self):
        colStr = '{:<10}'.format('Item #') + '{:<20}'.format('Label') \
                 + '{:<15}'.format('Product') + '{:<15}'.format('Pack Size') \
                 + '{:<7}'.format('Cases') + '{:<10}'.format('Ross #') \
                 + '{:<10}'.format('Batches') + '{:<15}'.format('Allergens') \
                 + '{:<15}'.format('Non-K')
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


class ScheduleItem:
    """an item in the schedule"""

    def __init__(self,
                 itemNum='009057',
                 label='cobbmkt originals',
                 product='apple',
                 packSize='1/1oz',
                 cases=100,
                 rossNum='10',
                 batches='1',
                 allergens=[Allergen.EGG, Allergen.BISULFITE],
                 kosher=True):
        self.itemNum = itemNum
        self.label = label
        self.product = product
        self.packSize = packSize
        self.cases = cases
        self.rossNum = rossNum
        self.batches = batches
        self.allergens = allergens
        self.kosher = kosher  # whether item is kosher or not

    def __repr__(self):
        allergensStr = []
        for item in self.allergens:
            allergensStr.append(item.name.capitalize())
        allergensStr = ', '.join(allergensStr)

        return ('{self.itemNum:<10}{self.label:<20}{self.product:<15}' +
                '{self.packSize:<15}{self.cases:<7}{self.rossNum:<10}' +
                '{self.batches:<10}{allergensNameStr:<15}{self.kosher!s:<15}' +
                '\n').format(self=self, allergensNameStr=allergensStr)


if __name__ == "__main__":
    a = Schedule("10/14/18")
    a.tub.append(ScheduleItem())
    a.pail.append(ScheduleItem())
    print(a)