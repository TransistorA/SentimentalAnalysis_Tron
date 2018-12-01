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
# and might be used in future

# Additional columns made by productListing.py
ALLERGEN_VALUE = 8  
LINE = 9
CPB = 10
TIME_TO_RUN_BATCH = 11

# FOR Finished Product Listing
FPL_LINE = 5
BATCH_WEIGHT = 9
