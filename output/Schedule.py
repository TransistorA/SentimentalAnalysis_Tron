class Schedule:
    ''' a schedule object'''
    def __init__(self):
        self.date = None
        self.tub = []
        self.pail = []
        self.gallon = []
        self.retail = []

    def __repr__(self):
        colStr = '{:<10}'.format('Item #') + '{:<20}'.format('Label')\
        + '{:<15}'.format('Product') + '{:<15}'.format('Pack Size')\
        + '{:<7}'.format('Cases') + '{:<10}'.format('Ross #')\
        + '{:<10}'.format('Batches') + '{:<15}'.format('Allergens')\
        + '{:<15}'.format('Non-K')
        schedule = '{:^114}'.format("Production Schedule") + '\n'\
        + "Date: {self.date} \n".format(self=self)
        schedule += '\n' + '{:^114}'.format("Tub Line") + '\n' + colStr + '\n'
        for item in self.tub:
            schedule += str(item) 
        schedule += '\n' + '{:^114}'.format("Pail/Drum/Pouch Line") + '\n' + colStr + '\n'
        for item in self.pail:
            schedule += str(item)
        schedule += '\n' + '{:^114}'.format("Gallon Line") + '\n' + colStr + '\n'
        for item in self.gallon:
            schedule += str(item)
        schedule += '\n' + '{:^114}'.format("Retail Line") + '\n' + colStr + '\n'
        for item in self.retail:
            schedule += str(item)
        return schedule

class ScheduleItem:
    ''' an item in the schedule '''
    def __init__(self,infoList=None):
        self.duration = 0 # time for the item to run
        self.allergens = 'na' # whether it is allergen
        self.kosher = 'null' # whether it is kosher or not. Default as kosher
        self.changeoverTime = 0 # default as 0
        self.itemNum = '009057' 
        self.label = 'cobbmkt originals'
        self.product = 'apple'
        self.packSize = '1/1oz'
        self.cases = '100'
        self.rossNum = '10'
        self.batches = '1'

    def __repr__(self):
        return ('{self.itemNum:<10}{self.label:<20}{self.product:<15}'+
                '{self.packSize:<15}{self.cases:<7}{self.rossNum:<10}'+
                '{self.batches:<10}{self.allergens:<15}{self.kosher:<15}'
                + '\n').format(self=self)

def test():
    a = Schedule()
    a.date = "10/14/18"
    a.tub.append(ScheduleItem())
    a.pail.append(ScheduleItem())
    print(a)
