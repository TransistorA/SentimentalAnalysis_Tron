To create the product listing I created a product listing class which contains a dictionary items.  The dictionary is indexed by item number so it is easy to take an item from the cases needed report and find any information about it from the item number.  I also made a file constants.py which holds constants for each item in the list of information about a product.  For example, if you wanted to knoe the pack size for item number 009203 and we called out object 'pl' you would use the getItem method as so:

pl.getItem('009203')[consants.PACK_SIZE]

The methods in the product listing are:
__init__(self): Creates a new ProductListing object and initializes an empty dictionary
readNewFile(self, fileName): reads in a .csv file and creates the product listing fromthe file
loadProductListing(self): loads a product listing that was previously saved to a .txt file
saveProductListing(self): saves the product listing to a .txt file
expandProductListing(self): adds extra columns for additional information makes use of helper methods to keep the function form being too long
addAllergenEnum(self): Unimplemented method to add the allergen enum to the product listing.  More methods like this will be added as we get more information from Tulkoff.  This is Ryan's responsibility.
getItem(self, itemNumber): Gets the information about an item as a list.  Use the constants in constants.py to index the list properly.
__repr__(self): prints out the product item listing
isDigit(self, item): helper method to identifiy the item numbers in the csv file
