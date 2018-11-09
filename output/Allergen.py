from enum import IntFlag
class Allergen(IntFlag):
    NONE = 0
    EGG = 1
    BISULFITE = 2
    MUSTARD = 4
    MILK = 8
    FISH = 16
    SOY = 32
    TREENUT = 64
    WHEAT = 128

