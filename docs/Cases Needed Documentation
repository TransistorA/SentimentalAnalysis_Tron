Cases Needed Documentation

The cases needed class has four variables, each is a dictionary and corresponds to the line it is named after.  Each key in the dictionary is a item number, these are 6 digit codes with an 'S' on the end occacionally. The methods for this class currently include readFile(fileName) and getItem(item) as well as a constructor and repr function.

readFile will take in a path to a .csv file and parse it.  Each row in the csv can be either An item label, product already on hand, an order, or empty space.  Regular Expressions were used to detect each type of row.  Items have a 6 digit code and sometimes have an 'S' on the end.  Product on hand has a lot code as the first element, which always ends in 'M'. Orders start with a date of the form mm/dd/yyyy.  These characteristics were used to split each item.  There are also some rows that denote the beginning of a section of the file (Pail, Gallon, Tub, and Retail) and these were detected in order to tell which dictionary should be filled with the listed orders.  The item numbers are saved as strings because they sometimes have a character at the end, dates are saved as strings but can easily be parsed at a later time to use a date library, and the numbers of cases are saved as ints.  The getItem method will search all four lines for the item number and return the list of tuples for that item number.  If the item number does not exist it will return the empty list.  The repr function labels and prints out each of the product labels.  There are a few helper functions where the regular expressions are used and a helper function for the repr function.

This module does not currently account for the cases in stock but on hold and that functionality will need to be added at a later time.

Example of dictionary:
{item: [(date, number, number), (date, number, number)], item: [(date, number, number)]}

casesNeeded.csv: full cases needed report with all four production lines and extra junk that gets filtered out

casesNeededTest.csv: csv file with only the tub line for testing the integer program with only one production line
