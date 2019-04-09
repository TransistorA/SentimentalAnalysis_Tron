'''

Constants to denote the indices of information in the product item listing

This will be expanded at the product listing is expanded

'''
# for use in the items dictionary
DESCRIPTION = 0
PACK_SIZE = 1
LABEL = 2
CUSTOMER_NAME = 2
ROSS_WIP = 3
ALLERGEN = 4
NON_K = 5
COMMENTS = 6
# Skip column 7 because it could introduce weird errors
ALLERGEN_VALUE = 7  # Still need to implement
# this column gets made n
LINE = 8
CPB = 9
TIME_TO_RUN_BATCH = 10
LEAD_TIME = 11

# FOR Finished Product Listing
FPL_LINE = 5
BATCH_WEIGHT = 9

#Cases per hour by line  (CPH)
CPH_TUB = 500
CPH_GALLON = 400
CPH_PAIL = 175