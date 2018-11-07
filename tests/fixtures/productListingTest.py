from __future__ import print_function
import productListing
import os
import constants

# run with $ py.test -s -v productListingTest.py

def resourceSetup():
	print('resources_setup()')
	with open(fileName, 'w+') as file:
		file.write(testList)

  
def resourceTeardown():
	print('resources_teardown()')
	os.remove(fileName)
	os.remove(tmpFile)


def setupModule():
	print('\nsetupModule()')
	resourceSetup()

def teardownModule():
	print('\nteardownModule()')
	resourceTeardown()
 
def test():
	setupModule()
	print('test1()')
	pl = productListing.ProductListing()
	pl.readNewFile(fileName)
	pl.saveProductListing()
	
	pl2 = productListing.ProductListing()
	pl2.loadProductListing()

	assert pl.items == pl2.items
	assert pl.getItem('064001') == testItem
	
	teardownModule()

def test_constants():
	print("test_constants()")
	assert constants.ALLERGEN_VALUE == 8

fileName = "test.csv"
tmpFile = 'currentListing.txt'
testItem = ['CKTL SCE XBOLD', '12/9 OZ', 'Tulkoff', 'CSB02', 'na', '', '', '', 'Allergen enum', 'nozzle type', 'WIP source']
	
testList = '''Finished Product Item Listing,,,,,,,,
"Cross reference between Product Code, Ross #, and Formula #",,,,,,,,
Item,Item Description,Pack Size,Label or Customer Name,Ross WIP #,Allergen / Sensitizer,Non K,Comments,
HRP0100,HR Peroxidase,250 gal Tote,Tulkoff,HRP01,na,,,
001001,HR WHITE,12/5 OZ,Tulkoff,HRF03,Bisulfite,,,
003128,HR WHITE,4/8 LB,Outback,HRF01,na,,,
004001,HR WHITE,2/32 OZ,Tulkoff,HRF01,na,,,
007001,HR WHITE,4/8 LB,Tulkoff,HRF01,na,,,
007037,HR WHITE,4/8 LB,Sysco Classic,HRF01,na,blue pallet,,
013001S,CKTL SAUCE,12/8 OZ,Tulkoff,CSR01S,na,,,
013356S,CKTL SAUCE,12/9 OZ,Fresh Market,CSR01S,na,,,
014001S,CKTL SAUCE,4/8 LB,Tulkoff,CSR01S,na,,,
014037S,CKTL SAUCE,4/8 LB,Sysco Classic,CSR01S,na,blue pallet,,
014147S,CKTL SAUCE,4/1 GAL,Monarch,CSR01S,na,,,
015001S,CKTL SCE X BOLD,4/8 LB,Tulkoff,CSB02S,na,,,
016037,TIGER SAUCE,4/1 GAL,Sysco Classic,TIS01S,Egg & Mustard,blue pallet,,
017356S,CKTL SCE BOLD,12/9 OZ,Fresh Market,CSB03S,na,,,
025000,HR ROOTS - wash,na,T,na,na,,Roots,
025001S,CKTL SAUCE,24/8 OZ,Tulkoff,CSR01S,na,,,
025229S,CKTL SAUCE,24/8 OZ,Publix,CSR01S,na,blue pallet,,
026000,HR ROOTS - dirty,na,T,na,na,,Roots,
026133,HR WHITE,375# Drum,Kens,HRF01,na,Micro Test,"Special micro tests, yeast apc mold",
027001,HR WHITE,200# Drum,Tulkoff,HRF09,na,,,
027045,HR WHITE,200# Drum,Buedel,HRF01,na,,,
028061,HR WHITE,12/8 OZ,Shoprite-P,HRF05,Bisulfite,,Passover,
028079,HR WHITE,12/8 OZ,GFS,HRF01,na,blue pallet,,
028087,HR WHITE,12/8 OZ,T-Passover,HRF05,Bisulfite,,Passover,
028098,HR WHITE,12/8 OZ,Shoprite,HRF03,Bisulfite,,,
028156,HR WHITE,12/8 OZ,Gordon Choice,HRF01,na,blue pallet,,
043195,HR WHITE,30# Pail,Cain's,HRC02,na,,no artificial flavor,
043215,HR WHITE,30# Pail,Kraft,HRC01,na,MICRO TEST (5),Special micro tests,
043218,HR WHITE,30# Pail,Chelton House,HRC01,na,,,
045001,G/W,30# Pail,Tulkoff,GWR01,na,MICRO TESTED,,
045172,G/W & CA,30# Pail,Tulkoff,GWR02,na,,w/ 2% citric acid,
045219,G/W,30# Pail,Lakeview,GWRM1,na,MICRO TESTED,MICRO TESTED,
045220,G/W,30# Pail,Ventura Fds,GWRM1,na,MICRO TESTED,MICRO TESTED,
045350,G/W,30# Pail,Lonestar,GWR01,na,MICRO TESTED,,
045395,GARLIC/WATER,30# Pail,Heinz,GWR01,na,MICRO TESTED,Micro tested - APC & Coliforms only,
058082,CKTL SAUCE,30# Pail,Seaside,CSV01,na,,,
061356S,DILL TARTAR SCE,12/8 FL OZ,Fresh Market,TAD01S,Egg,,,
064001,CKTL SCE XBOLD,12/9 OZ,Tulkoff,CSB02,na,,,
064082,CKTL SCE XBOLD,12/9 OZ,Seaside,CSB02,na,,,
064230S,COCKTAIL SAUCE- X BOLD,12/9 OZ,PHILLIPS,CSB02S,na,,,
065220,GW w/CA,30# Pail,Ventura Fds,GWR04,na,MICRO TESTED,w/ citric acid,
066133,HR - EXTRA HOT,35# Pail,Kens,HRC06,na,,Extra Hot,
067001,HR WHITE,30# Pail,Tulkoff,HRF01,na,,,
067133,HR WHITE,30# Pail,Kens,HRF01,na,MICRO TESTED,MICRO TESTED,
067220,HR WHITE,30# Pail,Ventura Fds,HRF01,na,MICRO TESTED,,
068001,HR WHITE,30# Pail,Tulkoff,HRF08,na,,w/ capsicum (no mustard oil),
069328,HR NAT W/ MOEB,30# Pail,Damn Good,HRF11,Mustard,,w/ mustard oil essence blend,
070230S,DILL TARTAR ,12/8.25 FL OZ,PHILLIPS,TAD01S,Egg,,,
071082,GARLIC/O -V,30# Pail,Seaside,GOV01,na,,,
072082,GARLIC/W -V,30# Pail,Seaside,GWV01,na,,,
072037,GARLIC/W-V,30#Pail,Sysco Classic,GWV01,na,blue pallet,,
072220,GARLIC/W -V,30# Pail,Ventura Fds,GWV01,na,,,
073001,GARLIC/PUREE,30# Pail,Tulkoff,GPR01,na,MICRO TESTED,,
073133,GARLIC/PUREE,30# Pail,Kens,GPR01,na,MICRO TESTED,,
073220,GARLIC/PUREE,30# Pail,Ventura Fds,GPR01,na,MICRO TESTED,,
077356S,SWT TARTAR SCE,12/8 FL OZ,Fresh Market,TAS01S,Egg,,,
078001,GAR/PUREE - V,30# Pail,Tulkoff,GPV01,na,,,
079001,HR NAT HOT,200#DRUM,Tulkoff,HRF12,na,,,
080082,DILL TARTAR SCE,4/1 GAL,Seaside,TAD01,Egg,,,
082001,HR WHITE,400# Drum,Tulkoff,HRF07,na,,,
083001S,Chipotle Aioli,8/18floz,Tulkoff,CCA01S,Egg & Mustard,,,
084001S,SWT TARTAR SCE,4/1 GAL,Tulkoff,TAS01S,Egg,,,
085001,CHOPPED GARLIC,400# Drum,Tulkoff,GWR01,na,MICRO TESTED,,
088001S,Creamy HR Sce,8/18floz,Tulkoff,TIS01S,Egg & Mustard,,,
086001,GARLIC IN OIL,400# Drum,Tulkoff,GOR01,na,,,
089001,HR WHITE,35# Pail,Tulkoff,HRF12,na,,,
089244,HR WHITE,35# Pail,TW Garner,HRF12,na,,,
090001S,EX BOLD COCKTAIL,8/20.5oz ,Tulkoff,CSB02S,na,blue pallet,,
091001,Garlic Puree,400#Drum,Tulkoff,GPR01,na,MICRO TESTED,,
135114,G/W - V,6/32 OZ,Mama Lucia,GWV01,na,,,
135143,G/W - V,6/32 OZ,Mt Stirling,GWV01,na,,,
135147,G/W - V,6/32 OZ,Monarch,GWV01,na,,,
135197,G/W - V,6/32 OZ,Roma,GWV01,na,,,
136046,G/O - V,6/32 OZ,Villa Frizzoni,GOV01,na,,,

195001,GINGER PUREE,6/32 OZ,Tulkoff,GIP01,na,,,
195036,GINGER PUREE,6/32 OZ,Arrezzio,GIP01,na,blue pallet,,
198001,PESTO,6/30 FL OZ,Tulkoff,PES01,Milk,x,,
198036,PESTO,6/32 OZ,Arrezzio,PES01,Milk,x-blue pallet,,
199001,GINGER PUREE,2/32 OZ,Tulkoff,GIP01,na,,,
200037,GAR&OLIVE OIL,6/32OZ,Sysco Classic,GOO02,na,blue pallet,,
213260,CRABCAKE BSE,4/1 GAL,Tulkoff,CCB01,Egg & Mustard,,,
215179S,CRABCAKE BSE,4/1 GAL,Calvert House,CCS01S,Egg & Mustard,,,
217179S,CRABCAKE BSE,385# Drum,Grahams & Rollins,CCS01S,Egg & Mustard,,,
229328,HR WHT w/MOEB,12/8oz,Damn Good CS,HRF11,na,,,
230001,Chipotle Shelf Stable,8/18floz,Tulkoff,CCA01SS,Egg/Mustard,,,
231001,HR WHITE,400# Drum,Tulkoff,HRF09,na,,,
234019,HR WHITE - V,6/32 OZ ,Unipro,HRV01,na,,"Fine grind, West - HRF01 / 0105",
234082,HR WHITE - V,6/32 OZ ,Seaside,HRV01,na,,"Fine grind, West - HRF01 / 0105",
235082,G/W - V,6/32 OZ ,Seaside,GWV01,na,blue pallet,,
235119,G/W - V,6/32 OZ ,Cortona,GWV01,na,,,
236082,G/O - V,6/32 OZ ,Seaside,GOV01,na,blue pallet,,
241328,HR WHT w/MOEB,4/8 lb,Damn Good CS,HRF11,na,,,
254213,G/O - SV,6/32 OZ,C Express,GOV03,na,,,
257213,G/W - SV,6/32 OZ,C Express,GWV02,na,,,
Kosher,
424253,BurgundyCookinGWine,6/12.7fl oz,Sun of Italy,CS0105,na,x,Non-Kosher,
421265,SherryCookingWine,6/12.7fl oz,Shop Rite,CS0102,na,x,Non-Kosher,
422265,MarsalaCookingWine,6/12.7fl oz,Shop Rite,CS0104,na,x,Non-Kosher,
423265,WhiteCookingWine,6/12.7fl oz,Shop Rite,CS0103,na,x,Non-Kosher,
424265,BurgundyCookinGWine,6/12.7fl oz,Shop Rite,CS0105,na,x,Non-Kosher,
425238,SherryCookingWine,6/16 fl oz,Pompeian,CS0102,na,x-red peco,Non-Kosher,
426238,MarsalaCookingWine,6/16 fl oz,Pompeian,CS0104,na,x-red peco,Non-Kosher,
427238,WhiteCookingWine,6/16 fl oz,Pompeian,CS0103,na,x-red peco,Non-Kosher,
428238,BurgundyCookinGWine,6/16 fl oz,Pompeian,CS0105,na,x-red peco,Non-Kosher,
435238,Red Wine Vinegar,4/1 Gal,Pompeian,CS0096,na,x-red peco,Non-Kosher,
446325,SESAME GARLIC,4/4.9 LBS,Asian Menu,ASM01,"Soy, Wheat",,23-JJJ01Y of manufacturing,
447325,CLASSIC STIR FRY,4/4.9 LBS,Asian Menu,ASM03,"Soy, Wheat",,23-JJJ01Y of manufacturing,
448325,GENERAL TSO'S,4/4.9 LBS,Asian Menu,ASM04,"Soy, Wheat",,23-JJJ01Y of manufacturing,
449325,ORANGE GINGER,4/4.75 LBS,Asian Menu,ASM05,"Soy, Wheat",,23-JJJ01Y of manufacturing,
450325,HOISIN TERIYAKI ,2/1 GAL,Asian Menu,ASM02,"Soy, Wheat",,23-JJJ01Y of manufacturing,
451325,SESAME GARLIC,2/1 GAL,Asian Menu,ASM01,"Soy, Wheat",,23-JJJ01Y of manufacturing,
615276,Classic Mayo,6/12 floz,Sir Kensington's,SRK01,Egg/Mustard,blue pallet,,
616276,Organic Mayo,6/12 floz,Sir Kensington's,SRK09,Egg/Mustard,blue pallet,,
617276,Avocado Mayo,6/12 floz,Sir Kensington's,SRK02,Egg/Mustard,blue pallet,,
618276,Chipotle Mayo,6/12 floz,Sir Kensington's,SRK10,Egg,blue pallet,,
619276,Special Sauce,6/12 floz,Sir Kensington's,SRK05,Egg/Mustard,blue pallet,,
620276,Avocado Mayo,6/16 floz,Sir Kensington's,SRK02,Egg/Mustard,blue pallet,,
621276,Organic Mayo,6/32 floz,Sir Kensington's,SRK09,Egg/Mustard,blue pallet,,
622276,Avocado Ranch,6/9 floz,Sir Kensington's,SRK15,Egg/Micro,blue pallet,,
624276,Buffalo Ranch,6/9 floz,Sir Kensington's,SRK17,Egg/Micro,blue pallet,,
626276,Classic Ranch,6/9 floz,Sir Kensington's,SRK14,Egg/Micro,blue pallet,,
627276,Pizza Ranch,6/9 floz,Sir Kensington's,SRK16,Egg/Micro,blue pallet,,
628276,Sriracha Mayo,6/10floz,Sir Kensington's,SRK06,Egg/Micro,blue pallet,,
629276,Dijonnaise,6/10floz,Sir Kensington's,SRK08,Egg/Mustard,blue pallet,,
035036,GARLIC SPREAD,6/2 LB,ARREZZIO,CP-FEGT,Milk & Soy,x,Oasis TO REPLACE 039036 - effective?,,
035105,GARLIC SPREAD,6/2 LB,NATURAL PACK,REPACK,Milk & Soy,x,Oasis,,
035125,GARLIC SPREAD,6/2 LB,ROSELI,CP-FEGT,Milk & Soy,x,Oasis,,
037001,GARLIC SPREAD,2/2 LB,TULKOFF,REPACK,Milk & Soy,x,Oasis,,
038001,ZERO T GARLIC SPRD,6/2 LB,TULKOFF,CP-FEGZ,Milk & Soy,x,Oasis,,
039036,GARLIC SPREAD,6/2 LB,ARREZZIO,CP-10209,Milk & Soy,x,Kagome,,
158001,SCAMPI ZERO T,2/2.5 LB,TULKOFF,CP-30510,Milk & Soy,x,Darifair.  S/L = 4 R,,
259197,GARLIC SPREAD,2/4 LB,ROMA,REPACK,Milk & Soy,,,,
335125,GARLIC SPREAD,6/2 LB,ROSELI,REPACK,Milk & Soy,,,,
,,,,,,,
,,
,,
'''
