from __future__ import print_function
import os
import sys
# TO Yash: These file paths may need to be changed while moving the file
sys.path.append('../../')
import productListing.productListing as prodList
import productListing.constants as constants
from backend.src.allergen import Allergen

import productListing
import os



# run with $ py.test -s -v productListingTest.py

def resourceSetup():
	print('resources_setup()')
	with open(fileName, 'w+') as file:
		file.write(testList)
	with open(fpl_fileName, 'w+') as file:
		file.write(finished_product_list)

  
def resourceTeardown():
	print('resources_teardown()')
	os.remove(fileName)
	os.remove(fpl_fileName)
	#os.remove(tmpFile)
	#os.remove(savedListing)

def setupModule():
	print('\nsetupModule()')
	resourceSetup()

def teardownModule():
	print('\nteardownModule()')
	resourceTeardown()
 
def test():
	setupModule()
	print('test1()')
	pl = prodList.ProductListing()
	pl.readNewFile(fileName)
	
	assert str(pl.getItem('086001')) == testItem

	#pl.saveProductListing(savedListing)	
	#pl2 = prodList.ProductListing()
	#pl2.loadProductListing(savedListing)
	#assert len(pl.items) == len(pl2.items)
	#assert pl.getItem('043113') == pl2.getItem('043113')

	teardownModule()

def test_constants():
	print("test_constants()")
	assert constants.ALLERGEN_VALUE == 8

fileName = "test.csv"
fpl_fileName = "FinishedProductList.csv"
tmpFile = 'currentListing.txt'
savedListing = 'tempFile'
testItem = "['GARLIC IN OIL', '400# Drum', 'Tulkoff', 'GOR01', 'na', '', '', '', <Allergen.NONE: 0>, 'PAIL', 7, 30]"
	
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
015001S,CKTL SCE X BOLD,4/8 LB,Tulkoff,CSB02S,na,,,
016037,TIGER SAUCE,4/1 GAL,Sysco Classic,TIS01S,Egg & Mustard,blue pallet,,
017356S,CKTL SCE BOLD,12/9 OZ,Fresh Market,CSB03S,na,,,
025229S,CKTL SAUCE,24/8 OZ,Publix,CSR01S,na,blue pallet,,
027001,HR WHITE,200# Drum,Tulkoff,HRF09,na,,,
028061,HR WHITE,12/8 OZ,Shoprite-P,HRF05,Bisulfite,,Passover,
028087,HR WHITE,12/8 OZ,T-Passover,HRF05,Bisulfite,,Passover,
028098,HR WHITE,12/8 OZ,Shoprite,HRF03,Bisulfite,,,
028156,HR WHITE,12/8 OZ,Gordon Choice,HRF01,na,blue pallet,,
043195,HR WHITE,30# Pail,Cain's,HRC02,na,,no artificial flavor,
045001,G/W,30# Pail,Tulkoff,GWR01,na,MICRO TESTED,,
045172,G/W & CA,30# Pail,Tulkoff,GWR02,na,,w/ 2% citric acid,
045395,GARLIC/WATER,30# Pail,Heinz,GWR01,na,MICRO TESTED,Micro tested - APC & Coliforms only,
061356S,DILL TARTAR SCE,12/8 FL OZ,Fresh Market,TAD01S,Egg,,,
064230S,COCKTAIL SAUCE- X BOLD,12/9 OZ,PHILLIPS,CSB02S,na,,,
067001,HR WHITE,30# Pail,Tulkoff,HRF01,na,,,
070230S,DILL TARTAR ,12/8.25 FL OZ,PHILLIPS,TAD01S,Egg,,,
071082,GARLIC/O -V,30# Pail,Seaside,GOV01,na,,,
072082,GARLIC/W -V,30# Pail,Seaside,GWV01,na,,,
072037,GARLIC/W-V,30#Pail,Sysco Classic,GWV01,na,blue pallet,,
073001,GARLIC/PUREE,30# Pail,Tulkoff,GPR01,na,MICRO TESTED,,
073133,GARLIC/PUREE,30# Pail,Kens,GPR01,na,MICRO TESTED,,
073220,GARLIC/PUREE,30# Pail,Ventura Fds,GPR01,na,MICRO TESTED,,
077356S,SWT TARTAR SCE,12/8 FL OZ,Fresh Market,TAS01S,Egg,,,
079001,HR NAT HOT,200#DRUM,Tulkoff,HRF12,na,,,
082001,HR WHITE,400# Drum,Tulkoff,HRF07,na,,,
083001S,Chipotle Aioli,8/18floz,Tulkoff,CCA01S,Egg & Mustard,,,
084001S,SWT TARTAR SCE,4/1 GAL,Tulkoff,TAS01S,Egg,,,
085001,CHOPPED GARLIC,400# Drum,Tulkoff,GWR01,na,MICRO TESTED,,
086001,GARLIC IN OIL,400# Drum,Tulkoff,GOR01,na,,,
089001,HR WHITE,35# Pail,Tulkoff,HRF12,na,,,
089244,HR WHITE,35# Pail,TW Garner,HRF12,na,,,
090001S,EX BOLD COCKTAIL,8/20.5oz ,Tulkoff,CSB02S,na,blue pallet,,
135114,G/W - V,6/32 OZ,Mama Lucia,GWV01,na,,,
135143,G/W - V,6/32 OZ,Mt Stirling,GWV01,na,,,
135147,G/W - V,6/32 OZ,Monarch,GWV01,na,,,
135197,G/W - V,6/32 OZ,Roma,GWV01,na,,,
195001,GINGER PUREE,6/32 OZ,Tulkoff,GIP01,na,,,
195036,GINGER PUREE,6/32 OZ,Arrezzio,GIP01,na,blue pallet,,
198001,PESTO,6/30 FL OZ,Tulkoff,PES01,Milk,x,,
198036,PESTO,6/32 OZ,Arrezzio,PES01,Milk,x-blue pallet,,
199001,GINGER PUREE,2/32 OZ,Tulkoff,GIP01,na,,,
200037,GAR&OLIVE OIL,6/32OZ,Sysco Classic,GOO02,na,blue pallet,,
215179S,CRABCAKE BSE,4/1 GAL,Calvert House,CCS01S,Egg & Mustard,,,
217179S,CRABCAKE BSE,385# Drum,Grahams & Rollins,CCS01S,Egg & Mustard,,,
229328,HR WHT w/MOEB,12/8oz,Damn Good CS,HRF11,na,,,
231001,HR WHITE,400# Drum,Tulkoff,HRF09,na,,,
234019,HR WHITE - V,6/32 OZ ,Unipro,HRV01,na,,"Fine grind, West - HRF01 / 0105",
234082,HR WHITE - V,6/32 OZ ,Seaside,HRV01,na,,"Fine grind, West - HRF01 / 0105",
235082,G/W - V,6/32 OZ ,Seaside,GWV01,na,blue pallet,,
235119,G/W - V,6/32 OZ ,Cortona,GWV01,na,,,
236082,G/O - V,6/32 OZ ,Seaside,GOV01,na,blue pallet,,
257213,G/W - SV,6/32 OZ,C Express,GWV02,na,,,
Kosher,
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
037001,GARLIC SPREAD,2/2 LB,TULKOFF,REPACK,Milk & Soy,x,Oasis,,
158001,SCAMPI ZERO T,2/2.5 LB,TULKOFF,CP-30510,Milk & Soy,x,Darifair.  S/L = 4 R,,
335125,GARLIC SPREAD,6/2 LB,ROSELI,REPACK,Milk & Soy,,,,
,,,,,,,
,,
,,
'''

finished_product_list = '''Product Code,Item Description (WIP Name),Pack Size,Label or Customer Name,Ross WIP #,Line,BLENDING ROOM,GRINDING ROOM,Notes,  WIP BATCH SIZE POUNDS,Minimum Wt.,MinimumWt. using MAV,MAV,Target Wt.,Maximum Wt.
027001,HR WHT FINE,200# Drum,T,HRF09,DRUM,,X,,1114,1114,1092,22,1147,1182
027200,HR WHT CRSE,200# Drum,COARSE,HRC01,DRUM,,X,,1114,1114,1092,22,1147,1182
027215,HR WHT CRSE,400# Drum,KRAFT,HRC01,DRUM,,X,,1114,1114,1092,22,1147,1182
030001,HR WHT FINE,200# Drum,T,HRF07,DRUM,,X,,2210,2210,2166,44,2276,2345
031001,HR WHT FINE,200# Drum,T,HRF01,DRUM,,X,,2210,2210,2166,44,2276,2345
056001,HR WHT FINE,400# Drum,T,HRF01,DRUM,,X,,2210,2210,2202,8,2276,2345
079001,HR WHT FINE,200# DRUM,T,HRF12,DRUM,,X,,1200,1200,1176,24,1236,1273
082001,HR WHT FINE,400# Drum,T,HRF07,DRUM,,X,,2210,2210,2166,44,2276,2345
085001,GAR/W,400# Drum,T,GWR01,DRUM,X,,,3562,3562,3491,71,3669,3779
086001,GAR/O,400# Drum,T,GOR01,DRUM,X,,GWR07+OIL AT THE LINE=GOR01,3511,,,,,
168082,GARLIC/W VALUE,400# DRUM,SEASIDE (PANOLA PEPPER),GWV01,DRUM,X,,,3547,,,,,
217179S,CRAB CAKE MIX,385# Drum,CALVERT HOUSE,CCS01S,DRUM,X,,,1758,1758,1723,35,1811,1865
231001,HR WHT FINE,400# Drum,T,HRF09,DRUM,,X,,1114,n/a,n/a,n/a,n/a,n/a
635276,CLASSIC RANCH,400# Drum,SIR KENSINGTON'S,SRK14,DRUM,X,,,1698,,,,,
636276,PIZZA RANCH,400# Drum,SIR KENSINGTON'S,SRK16,DRUM,X,,,1552,,,,,
637276,AVOCADO RANCH,400# Drum,SIR KENSINGTON'S,SRK15,DRUM,X,,,1546,,,,,
638276,BUFFALO RANCH,400# Drum,SIR KENSINGTON'S,SRK17,DRUM,X,,,1712,,,,,
469001,HR WHT CRSE,400# DRUM,T,HRC01,DRUM,,X,,1114,,,,,
003128,HR WHT FINE,4/8 LBS,OUTBACK STEAKHOUSE,HRF01,GALLON,,X,,2210,2210,2124,86,2276,2345
007001,HR WHT FINE,4/8 LBS,T,HRF01,GALLON,,X,,2210,2210,2124,86,2276,2345
007037,HR WHT FINE,4/8 LBS,SYSCO CLASSIC ,HRF01,GALLON,,X,,2210,2210,,,2276,2345
007057,HR WHT FINE,4/8 LBS,COBBLESTREET MARKET ORIGINALS,HRF01,GALLON,,X,,2210,2210,,,2276,2345
007147,HR WHT FINE,4/8 LBS,MONARCH,HRF01,GALLON,,X,,2210,2210,2124,86,2276,2345
011001S,TGR SCE DRSNG,4/1 GAL,T,TID01S,GALLON,X,,,2196,2196,2110,86,2262,2330
014001S,CKTAIL SCE,4/8 LBS,T,CSR01S,GALLON,X,,,2258,2258,2245,13,2326,2396
014037S,CKTAIL SCE,4/8 LBS,SYSCO CLASSIC ,CSR01S,GALLON,X,,,2258,,,,,
015001S,EXTRA BOLD CKTAIL SCE,4/8 LBS,T,CSB02S,GALLON,X,,,2397,2258,2172,86,2326,2396
016037,TGR SCE,4/1 GAL,SYSCO CLASSIC ,TIS01S,GALLON,X,,,1851,2258,,,2326,2396
032001,HR RED FINE,4/8 LBS,T,HRR01,GALLON,,X,,1177,2397,2311,86,2469,2543
057196,CAESAR DRESSING,4/1 GAL,MELTING POT,MPT01,GALLON,X,,,1875,1851,1774,77,1907,1964
084001S,TAR SCE SWT - SUGAR,4/1 GAL,T,TAS01S,GALLON,X,,,1389,1177,1091,86,1212,1249
133019S,CKTAIL SCE-V,4/8 LBS,UNIPRO,CSV01S,GALLON,X,,,1900,1875,1789,86,1931,1989
133082S,CKTAIL SCE-V,4/8 LBS,SEASIDE,CSV01S,GALLON,X,,,1900,1389,,,1431,1474
133156,CKTAIL SCE-V,4/8 LBS,GFS,CSV01S,GALLON,X,,,1900,1900,1814,86,1957,2016
182019,HR WHT FINE ,4/8 LBS,UNIPRO,HRV01,GALLON,,X,HRF01+WATER AT THE LINE=HRV01,2210,1900,1814,86,1957,2016
182059,HR WHT FINE ,4/8 LBS,COBBLESTREET MARKET FOUNDATIONS,HRV01,GALLON,,X,HRF01+WATER AT THE LINE=HRV01,2210,1900,1814,86,1957,2016
182082,HR WHT FINE ,4/8 LBS,SEASIDE,HRV01,GALLON,,X,HRF01+WATER AT THE LINE=HRV01,2210,2210,2124,86,2276,2345
182110,HR WHT FINE ,4/8 LBS,GATOR,HRV01,GALLON,,X,HRF01+WATER AT THE LINE=HRV01,2210,2210,,,2276,2345
182192,HR WHT FINE ,4/8 LBS,HARVEST VALUE,HRV01,GALLON,,X,HRF01+WATER AT THE LINE=HRV01,2210,2210,2124,86,2276,2345
182198,HR WHT FINE ,4/8 LBS,WEST CREEK,HRV01,GALLON,,X,HRF01+WATER AT THE LINE=HRV01,2210,2210,2124,86,2276,2345
193031,BOLD CKTAIL SCE #0350,4/1 GAL,SYSCO IMPERIAL,CSB04,GALLON,X,,,2424,2210,2124,86,2276,2345
196031,COCKTAIL SAUCE #0351 ,4/1 GAL,SYSCO IMPERIAL,CSR03,GALLON,X,,,2424,2210,,,2276,2345
215179S,CRAB CAKE MIX,4/1 GAL,CALVERT HOUSE,CCS01S,GALLON,X,,,1758,2424.0,,,2496.7,2572
241238,Horseradish w/MOEB ,4/8 LBS,Damn Good Cocktails,HRF11,GALLON,,X,,1400,2424.0,,,2497,2572
325233S,GARLIC AIOLI w/ SUGAR,4/1 GAL,LEDO'S,LED01S,GALLON,X,,,1846,1758,1681,77,1811,1865
590276,CLASSIC MAYO,4/1 GAL,SIR KENSINGTON'S,SRK01,GALLON,X,,,1875,3630,3544,86,3739,3851
596276,DIJONNAISE,4/1 GAL,SIR KENSINGTON'S,SRK08,GALLON,X,,,1897,,,,,
631276,CLASSIC RANCH,4/1 GAL,SIR KENSINGTON'S,SRK14,GALLON,X,,,1698,,,,,
632276,PIZZA RANCH,4/1 GAL,SIR KENSINGTON'S,SRK16,GALLON,X,,,1552,,,,,
633276,AVOCADO RANCH,4/1 GAL,SIR KENSINGTON'S,SRK15,GALLON,X,,,1546,,,,,
634276,BUFFALO RANCH,4/1 GAL,SIR KENSINGTON'S,SRK17,GALLON,X,,,1712,,,,,
435238,VINEGAR POMPEIAN RED WINE ,4/1 GALLON,POMPEIAN,"CS0096
4N51",GALLON/RETAIL,,,CUSTOMER SUPPLIED - TANKER. Can run on either line.,,,,,,
187001,GAR/O,30# Pail,T,GOR01,PAIL,X,,GWR07+OIL AT THE LINE=GOR01,3511,,,,,
034215,HR WHT CRSE,30# Pail,KRAFT,HRC02,PAIL,,X,,1113,0,-86,86,0,0
040219,HR WHT FINE,30# Pail,T (RICHELIEU),HRF09,PAIL,,X,,1114,3511,3510.6,0.4,3616.3,3725
041357,HR WHT FINE,30# Pail,MAK,HRF07,PAIL,,X,,2210,,,,,
043001,HR WHT CRSE,30# Pail,T,HRC01,PAIL,,X,,1114,1114,1113.63,0.37,1147.42,1182
043113,HR WHT CRSE,30# Pail,OC.SPRAY,HRC02,PAIL,,X,,1113,2210,2209.63,0.37,2276.30,2345
043195,HR WHT CRSE,30# Pail,CAIN'S,HRC02,PAIL,,X,,1113,1114,1113.63,0.37,1147.42,1182
045001,GAR/W,30# Pail,T,GWR01,PAIL,,,,3562,1113,1112.63,0.37,1146.39,1181
045172,GAR/W CITRIC ACID,30# Pail,T,GWR02,PAIL,X,,,3385,1113,1112.63,0.37,1146.39,1181
045395,GAR/W,30# Pail,HEINZ,GWR01,PAIL,X,,,3562,3562,3561.63,0.37,3668.86,3779
045396,GAR/W,30# Pail,KELLOGG,GWR01,PAIL,X,,,3562,3385,3384.63,0.37,3486.55,3591
048001,GAR/W CITRIC ACID,30# Pail,T,GWR04,PAIL,X,,,3571,3562,3561.63,0.37,3668.86,3779
049001,HR WHT CRSE,35# Pail,T,HRC03,PAIL,,X,,1113,3562,3561.63,0.37,3668.86,3779
050001,HR WHT FINE,35# Pail,T,HRF09,PAIL,,X,,1114,3571,3571,0.4,3678,3788
051001,HR WHT CRSE,35# Pail,T,HRC01,PAIL,,X,,1114,1113,1113,0.4,1146,1181
067001,HR WHT FINE,30# Pail,T,HRF01,PAIL,,X,,2210,1114,1114,0.4,1147,1182
071082,GAR/O VALUE,30# Pail,SEASIDE,GOV01,PAIL,X,,GWV01+OIL AT THE LINE=GOV01,3547,1114,1114,0.4,1147,1182
072037,GARLIC/W VALUE,30# Pail,SYSCO CLASSIC ,GWV01,PAIL,X,,,3547,2210,2210,0,2276,2345
072082,GARLIC/W VALUE,30# Pail,SEASIDE,GWV01,PAIL,X,,,3547,3547,3547,0,3653,3763
073001,GAR/PUREE,30# Pail,T,GPR01,PAIL,X,,,3315,3547,,,,
073133,GAR/PUREE,30# Pail,KENS,GPR01,PAIL,X,,,3315,3547,3547,0,3653,3763
073220,GARLIC PUREE,30# Pail,VENTURA FOODS,GPR01,PAIL,X,,,3315,3315,3315,0,3414,3517
089001,HR WHT FINE,35# Pail,T,HRF12,PAIL,,X,,1200,3315,3315,0,3414,3517
089244,HR WHT FINE,35# Pail,TW GARNER,HRF12,PAIL,,X,,1200,3315,3315,0,3414,3517
092001,HR WHT CRSE,30# Pail,T,HRC07,PAIL,,X,,2000,1200,,,1236,1273
125001,CHOPPED RSTED GARLIC,30# Pail,T (DAWN FOODS),GRC04,PAIL,X,,,3562,1200,0,0,1236,1273
163001,PUREE/GING,35# Pail,T,GIP01,PAIL,,X,,2718,,,,,
164001,PUREE/GING ALL NAT,30# Pail,T,GIP04,PAIL,,X,,1000,,,,,
164357,PUREE/GING ALL NAT,30# Pail,MID ATLANTIC KITCHEN,GIP04,PAIL,,X,,1000,2718,2717.6,0.4,2799.5,2884
183001,HR WHT FINE ,30# Pail,SEASIDE,HRV01,PAIL,,X,HRF01+WATER AT THE LINE=HRV01,2210,1000,999.6,0.4,1030.0,1061
319001,PIZZA SAUCE - UMD,4/1 lb Pouches,UNIVERSITY OF MARYLAND,PIZ01,POUCH,X,,,2300,1000,999.6,0.4,1030.0,1061
389275,SHACK SAUCE,6/5.5 lb Pouches,Shake Shack,SHK02,POUCH,X,,,1800,2210,2124,86,2276,2345
399275,Buttermilk Herb Sauce ,6/5.5 lb Pouches,Shake Shack,SHK01,POUCH,X,,,1636,2300,,,2369,2440
591276,SUGAR FREE CLASSIC MAYO,4/1 GAL,SIR KENSINGTON'S,SRK03,POUCH,X,,,1841,,,,,
001001,HR WHT FINE,12/5 OZ,T,HRF03,RETAIL,,X,,1107,,,,,
013001S,CKTAIL SCE w/ SUGAR,12/8 OZ,T,CSR01S,RETAIL,X,,,2258,,,,,
013356S,CKTAIL SCE w/ SUGAR,12/9 OZ,THE FRESH MARKET,CSR01S,RETAIL,X,,,2258,142,133,9,146,151
017356S,FM BOLD CKTAIL SCE w/ SUGAR,12/9 OZ,THE FRESH MARKET,CSB03S,RETAIL,X,,,2424,,,,,
028001,HR WHT FINE,12/8 OZ,T,HRF03,RETAIL,,X,,1107,1107,1094,13,1140,1174
028054,HR WHT FINE,12/8 OZ,ROSOL,HRF03,RETAIL,,X,,1107,1107,1094,13,1140,1174
028061,HR WHITE,12/8 OZ,SHOP-PASSOVER,HRF05,RETAIL,,X,RUN ONCE A YEAR,1150,1150,1137,13,1185,1220
028087,HR WHT FINE PASSOVER,12/8 OZ,PASSOVER,HRF05,RETAIL,,X,RUN ONCE A YEAR,1150,1150,1137,13,1185,1220
028098,HR WHT FINE,12/8 OZ,SHOPRITE,HRF03,RETAIL,,X,,1107,1107,1094,13,1140,1174
028156,HR WHT FINE,12/8 OZ,GFS,HRF01,RETAIL,,X,,2210,,,,,
033001,HR RED FINE,12/8 OZ,T,HRR01,RETAIL,,X,,1177,1177,1164,13,1212,1249
033054,HR RED FINE,12/8 OZ,ROSOL,HRR01,RETAIL,,X,,1177,1177,1164,13,1212,1249
033061,HR RED FINE PASSOVER,12/8 OZ,SHOP-PASSOVER,HRR02,RETAIL,,X,RUN ONCE A YEAR,1257,1257,1244,13,1295,1334
033087,HR RED FINE PASSOVER,12/8 OZ,PASSOVER,HRR02,RETAIL,,X,RUN ONCE A YEAR,1257,1257,1244,13,1295,1334
033098,HR RED FINE,12/8 OZ,SHOPRITE,HRR01,RETAIL,,X,,1177,1177,1164,13,1212,1249
061356S,TAR SCE DILL w/ SUGAR,12/8 FL OZ,THE FRESH MARKET,TAD01S,RETAIL,X,,,1389,,,,,
064230S,EXTRA BOLD CKTAIL SCE w/ SUGAR,12/9 OZ,PHILLIPS,CSB02S,RETAIL,X,,,2397,,,,,
070230S,TAR SCE DILL,12/8.25 OZ,PHILLIPS,TAD01S,RETAIL,X,,,1389,,,,,
077356S,TAR SCE SWT - SUGAR,12/8 FL OZ,THE FRESH MARKET,TAS01S,RETAIL,X,,,1389,,,,,
083001S,CHPTL CHILI AIOLI,8/18 FL OZ,T,CCA01S,RETAIL,X,,,1800,490,468,22,504,519
088001S ,TGR SCE,8/18 FL OZ,T,TIS01S,RETAIL,X,,,1851,484,464,20,499,513
090001S,EXTRA BOLD CKTAIL SCE w/ SUGAR,8/20.5 OZ,T,CSB02S,RETAIL,X,,,2397,,,,,
093001S,HR SCE DELI,8/18 FL OZ,T,DHR01S,RETAIL,X,,,648,510,488,22,525,541
098001,KIMCHI AILOI,8/18 FL OZ,T,KIM01,RETAIL,X,,,1692,1692,,,1743,1795
099001,GARLIC AIOLI  ,8/18 FL OZ,T,LED01S,RETAIL,X,,,1846,1846,,,1901,1958
102001,KICKIN' DIPPIN' SAUCE,8/18 FL OZ,T,HMA01,RETAIL,X,,,2111,,,,,
103001,JALAPENO AIOLI,8/18 FL OZ,T,JPA01,RETAIL,X,,,1600,,,,,
229328,HR WHT w/ MOEB,12/8 OZ,DAMN GOOD COCKTAILS,HRF11,RETAIL,,X,,1400,,,,,
361267,OIL COCONUT ORGANIC,12/14 FL OZ,VITA COCO,CS0129,RETAIL,,,CUSTOMER SUPPLIED - TOTES,,,,,,
362267,OIL COCONUT ORGANIC,6/14 FL OZ,VITA COCO,CS0129,RETAIL,,,CUSTOMER SUPPLIED - TOTES,,,,,,
362285,OIL COCONUT ORGANIC,6/14 FL OZ,VITA COCO CANADA,CS0129,RETAIL,,,CUSTOMER SUPPLIED - TOTES,,,,,,
421238,SHERRY COOKING WINE,6/12.7 FL OZ (375 mL),POMPEIAN,"CS0102
4P61",RETAIL,,,CUSTOMER SUPPLIED - TANKER,,0,-30,30,0,0
421265,SHERRY COOKING WINE,6/12.7 FL OZ (375 mL),SHOPRITE,"CS0102
4P61",RETAIL,,,CUSTOMER SUPPLIED - TANKER,,0,-38,38,0,0
422238,MARSALA COOKING WINE,6/12.7 FL OZ (375 mL),POMPEIAN,"CS0104
4P63",RETAIL,,,CUSTOMER SUPPLIED - TANKER,,0,-31,31,0,0
422265,MARSALA COOKING WINE,6/12.7 FL OZ (375 mL),SHOPRITE,"CS0104
4P63",RETAIL,,,CUSTOMER SUPPLIED - TANKER,,0,-39,39,0,0
423238,SAUTERNE COOKING WINE (WHITE),6/12.7 FL OZ (375 mL),POMPEIAN,"CS0103
4P62",RETAIL,,,CUSTOMER SUPPLIED - TANKER,,0,-32,32,0,0
423265,SAUTERNE COOKING WINE (WHITE),6/12.7 FL OZ (375 mL),SHOPRITE,"CS0103
4P62",RETAIL,,,CUSTOMER SUPPLIED - TANKER,,0,-40,40,0,0
424238,BURGUNDY COOKING WINE,6/12.7 FL OZ (375 mL),POMPEIAN,"CS0105
4P64",RETAIL,,,CUSTOMER SUPPLIED - TANKER,,0,-33,33,0,0
424265,BURGUNDY COOKING WINE,6/12.7 FL OZ (375 mL),SHOPRITE,"CS0105
4P64",RETAIL,,,CUSTOMER SUPPLIED - TANKER,,0,-41,41,0,0
425238,SHERRY COOKING WINE,6/16 fl. oz.,POMPEIAN,CS0102,RETAIL,,,CUSTOMER SUPPLIED - TANKER,,0,,,0,0
426238,MARSALA COOKING WINE,6/16 fl. oz.,POMPEIAN,CS0104 ,RETAIL,,,CUSTOMER SUPPLIED - TANKER,,,,,,
427238,WHITE COOKING WINE,6/16 fl. oz.,POMPEIAN,CS0029,RETAIL,,,CUSTOMER SUPPLIED - TANKER,,,,,,
428238,BURGUNDY COOKING WINE,6/16 fl. oz.,POMPEIAN,CS0105 ,RETAIL,,,CUSTOMER SUPPLIED - TANKER,,,,,,
446325,SESAME GARLIC SCE,4/4.9 LBS,ASIAN MENU,ASM01,RETAIL,X,,,4000,4000,3937,63,4120,4244
447325,BROWN SAUCE (STIR FRY),4/4.9 LBS,ASIAN MENU,ASM03,RETAIL,X,,,4000,4000,3937,63,4120,4244
448325,GENERAL TSO,4/4.9 LBS,ASIAN MENU,ASM04,RETAIL,X,,,4000,4000,3937,63,4120,4244
449325,ORANGE GINGER ,4/4.86 LBS,ASIAN MENU,ASM05,RETAIL,X,,,4000,4000,3937,63,4120,4244
450325,HOISIN TERIYAKI SCE,2/10.34 LB,ASIAN MENU,ASM02,RETAIL,X,,,4000,4000,3901,99,4120,4244
451325,SESAME GARLIC SAUCE,2/10.34 LB,ASIAN MENU,ASM01,RETAIL,X,,,4000,4000,3901,99,4120,4244
453325,HOISIN TERIYAKI SCE,6/15.5 OZ,ASIAN MENU,ASM02,RETAIL,X,,,4000,4000,3980,20,4120,4244
454325,SESAME GARLIC SAUCE,6/15.5 OZ,ASIAN MENU,ASM01,RETAIL,X,,,4000,4000,3980,20,4120,4244
455325,BROWN SAUCE (STIR FRY),6/15.5 OZ,ASIAN MENU,ASM03,RETAIL,X,,,4000,4000,3980,20,4120,4244
456390,LWRYS GARLIC SPREAD,12/6 OZ,McCORMICK,LWR01,RETAIL,X,,,1717,1717,1706,11,1769,1822
480156,LIQUID SMOKE FLAVOR,12/32 FL OZ,GFS,LSF01,RETAIL,X,,,3000,3000,2968,32,3090,3183
592276,CLASSIC MAYO,6/10 FL OZ,SIR KENSINGTON'S,SRK01,RETAIL,X,,,1875,,,,,
593276,CLASSIC MAYO,6/16 FL OZ,SIR KENSINGTON'S,SRK01,RETAIL,X,,,1875,,,,,
594276,CLASSIC MAYO,6/32 FL OZ,SIR KENSINGTON'S,SRK01,RETAIL,X,,,1875,,,,,
615276,CLASSIC MAYO,6/12 FL OZ,SIR KENSINGTON'S,SRK01,RETAIL,X,,,1875,,,,,
616276,ORGANIC MAYO ,6/12 FL OZ,SIR KENSINGTON'S,SRK09,RETAIL,X,,,1871,,,,,
617276,AVOCADO OIL MAYO,6/12 FL OZ,SIR KENSINGTON'S,SRK02,RETAIL,X,,,1871,,,,,
618276,CHIPOTLE MAYO,6/12 FL OZ,SIR KENSINGTON'S,SRK10,RETAIL,X,,,1800,,,,,
619276,SPECIAL SAUCE,6/12 FL OZ,SIR KENSINGTON'S,SRK05,RETAIL,X,,,1718,,,,,
620276,AVOCADO OIL MAYO,6/16 FL OZ,SIR KENSINGTON'S,SRK02,RETAIL,X,,,1871,,,,,
621276,ORGANIC MAYO ,6/32 FL OZ,SIR KENSINGTON'S,SRK09,RETAIL,X,,,1871,,,,,
622276,AVOCADO RANCH,6/9 FL OZ,SIR KENSINGTON'S,SRK15,RETAIL,X,,,1546,,,,,
624276,BUFFALO RANCH,6/9 FL OZ,SIR KENSINGTON'S,SRK17,RETAIL,X,,,1712,,,,,
626276,CLASSIC RANCH,6/9 FL OZ,SIR KENSINGTON'S,SRK14,RETAIL,X,,,1698,,,,,
627276,PIZZA RANCH,6/9 FL OZ,SIR KENSINGTON'S,SRK16,RETAIL,X,,,1552,,,,,
628276,SRIRACHA MAYO,6/10 FL OZ,SIR KENSINGTON'S,SRK06,RETAIL,X,,,1845,,,,,
629276,DIJONNAISE,6/10 FL OZ,SIR KENSINGTON'S,SRK08,RETAIL,X,,,1897,,,,,
642276,ORGANIC MAYO ,6/16 FL OZ,SIR KENSINGTON'S,SRK09,RETAIL,X,,,1871,,,,,
643276,CHIPOTLE MAYO,6/10 FL OZ,SIR KENSINGTON'S,SRK10,RETAIL,X,,,1800,,,,,
714131,GINGER PLUM SAUCE,4/9.06 LBS,MELTING POT,71413,RETAIL,X,,,3000,3000,2914,86,3090,3183
714141,TERIYAKI GLAZE,4/8.75 LBS,MELTING POT,71414,RETAIL,X,,,3000,3000,2914,86,3090,3183
004001,HR WHT FINE,2/32 OZ,T,HRF01,TUB,,X,,2210,2210,2178,32,2276,2345
009001,HR WHT FINE,6/32 OZ,T,HRF01,TUB,,X,,2210,2210,2178,32,2276,2345
009037,HR WHT FINE,6/32 OZ,SYSCO CLASSIC ,HRF01,TUB,,X,,2210,2210,,,2276,2345
009057,HR WHT FINE,6/32 OZ,COBBLESTREET MARKET ORIGINALS,HRF01,TUB,,X,,2210,2210,,,2276,2345
009108,HR WHT FINE,6/32 OZ,WHITE MUSTANG,HRF01,TUB,,X,,2210,2210,2178,32,2276,2345
009147,HR WHT FINE,6/32 OZ,MONARCH,HRF01,TUB,,X,,2210,2210,2178,32,2276,2345
025229S,CKTAIL SCE,24/8 OZ (TUB),T (PUBLIX),CSR01S,TUB,X,,,2258,227,214,13,234,241
047001,GAR/W CITRIC ACID,6/32 OZ,T,GWR04,TUB,X,,,3571,3571,3539,32,3678,3788
047036,GAR/W CITRIC ACID,6/32 OZ,ARREZZIO,GWR04,TUB,X,,,3571,3571,3539,32,3678,3788
047057,GAR/W CITRIC ACID,6/32 OZ,COBBLESTREET MARKET ORIGINALS,GWR04,TUB,X,,,3571,3571,,,3678,3788
047105,GAR/W CITRIC ACID,6/32 OZ,NATURAL PACK,GWR04,TUB,X,,,3571,3571,3539,32,3678,3788
047125,GAR/W CITRIC ACID,6/32 OZ,ROSELI,GWR04,TUB,X,,,3571,3571,3539,32,3678,3788
047300,GAR/W CITRIC ACID,6/32 OZ,T (APPLEBEE'S/EGN),GWR04,TUB,X,,,3571,3571,3539,32,3678,3788
052001S,TGR SCE,6/32 FL OZ,T,TIS01S,TUB,X,,,1851,1851,1819,32,1907,1964
052037,TGR SCE,6/32 FL OZ,SYSCO CLASSIC ,TIS01S,TUB,X,,,1851,1851,1819,32,1907,1964
054001S,CKTAIL SCE,6/32 OZ,T,CSR01S,TUB,X,,,2258,,,,,
054037S,CKTAIL SCE,6/32 OZ,SYSCO CLASSIC ,CSR01S,TUB,X,,,2258,2258,,,2326,2396
096001,GAR/RSTD/CHPD,6/32 OZ,T,GRC01,TUB,X,,,3547,3547,3515,32,3653,3763
096036,GAR/RSTD/CHPD,6/32 OZ,ARREZZIO,GRC01,TUB,X,,,3547,3547,3515,32,3653,3763
096196,GAR/RSTD/CHPD,6/32 OZ,MELTING POT,GRC01,TUB,X,,,3547,3547,3515,32,3653,3763
110202,GING/GAR MIX,6/32 OZ,PANDA,GIGA01,TUB,X,,,6849,6849,6817,32,7054,7266
110302,GING/GAR MIX,6/32 OZ,PANDA CANADA,GIGA01,TUB,X,,,6849,6849,6817,32,7054,7266
110303,GING/GAR MIX,6/32 OZ,PANDA UAE,GIGA01,TUB,X,,,6849,907,875,32,934,962
134059,HR WHT FINE ,6/32 OZ,COBBLESTREET MARKET FOUNDATIONS,HRV01,TUB,X,,HRF01+WATER AT THE LINE=HRV01,2210,,,,,
134143,HR WHT FINE,6/32 OZ,MT STIRLING,HRV01,TUB,X,,HRF01+WATER AT THE LINE=HRV01,2210,2210,2178,32,2276,2345
134198,HR WHT FINE ,6/32 OZ,WEST CREEK,HRV01,TUB,X,,HRF01+WATER AT THE LINE=HRV01,2210,,,,,
135059,GARLIC/W VALUE,6/32 OZ,COBBLESTREET MARKET FOUNDATIONS,GWV01,TUB,X,,,3547,,,,,
135114,GARLIC/W VALUE,6/32 OZ,MAMA LUCIA,GWV01,TUB,X,,,3547,3547,3515,32,3653,3763
135143,GARLIC/W VALUE,6/32 OZ,MT STIRLING,GWV01,TUB,X,,,3547,3547,3515,32,3653,3763
135147,GARLIC/W VALUE,6/32 OZ,MONARCH,GWV01,TUB,X,,,3547,3547,3515,32,3653,3763
135197,GARLIC/W VALUE ,6/32 OZ,ROMA,GWV01,TUB,X,,,3547,,,,,
136059,GAR/O VALUE,6/32 OZ,COBBLESTREET MARKET FOUNDATIONS,GOV01,TUB,X,,GWV01+OIL AT THE LINE=GOV01,3547,,,,,
136114,GAR/O VALUE,6/32 OZ,MAMA LUCIA,GOV01,TUB,X,,GWV01+OIL AT THE LINE=GOV01,3547,3547,3515,32,3653,3763
136147,GAR/O VALUE,6/32 OZ,MONARCH,GOV01,TUB,X,,GWV01+OIL AT THE LINE=GOV01,3547,3547,3515,32,3653,3763
136197,GAR/O VALUE ,6/32 OZ,ROMA,GOV01,TUB,X,,GWV01+OIL AT THE LINE=GOV01,3547,,,,,
140036,GARLIC/W VALUE,6/32 OZ,ARREZZIO,GWV01,TUB,X,,,3547,3547,3515,32,3653,3763
141036,GAR/O VALUE,6/32 OZ,ARREZZIO,GOV01,TUB,X,,GWV01+OIL AT THE LINE=GOV01,3547,3547,3515,32,3653,3763
162001,PESTO BASIL,2/30 FL OZ,T,PES01,TUB,X,,,6519,6519,6487,32,6715,6916
162125,PESTO BASIL,2/30 FL OZ,ROSELI,PES01,TUB,X,,,6519,6519,6487,32,6715,6916
174001,GAR/O,6/32 OZ,T,GOR01,TUB,X,,GWR07+OIL AT THE LINE=GOR01,3511,3511,3479,32,3616,3725
174036,GAR/O,6/32 OZ,ARREZZIO,GOR01,TUB,X,,GWR07+OIL AT THE LINE=GOR01,3511,3511,3479,32,3616,3725
174057,GAR/O,6/32 OZ,COBBLESTREET MARKET ORIGINALS,GOR01,TUB,X,,GWR07+OIL AT THE LINE=GOR01,3511,3511,,,3616,3725
189202,GAR/O XTRA Garlic flavor,6/32 OZ,Panda,GOR03,TUB,X,,GWR07+OIL AT THE LINE=GOR03,3527,3527,,,3632.8,3742
195001,PUREE/GING,6/32 OZ,T,GIP01,TUB,,X,,2718,2718,2686,32,2800,2884
195036,PUREE/GING,6/32 OZ,ARREZZIO,GIP01,TUB,,X,,2718,2718,2686,32,2800,2884
198001,PESTO BASIL,6/30 FL OZ,T,PES01,TUB,X,,,6519,6519,6487,32,6715,6916
198036,PESTO BASIL,6/30 FL OZ,ARREZZIO,PES01,TUB,X,,,6519,6519,6487,32,6715,6916
199001,PUREE/GING,2/32 OZ,T,GIP01,TUB,,X,,2718,2718,2686,32,2800,2884
200037,CHP GARLIC & OLIVEOIL,6/32 OZ,SYSCO CLASSIC ,GOO02,TUB,X,,GWR07+OIL AT THE LINE=GOO02,3511,907,,,,
234019,HR WHT FINE ,6/32 OZ,UNIPRO,HRV01,TUB,,X,HRF01+WATER AT THE LINE=HRV01,2210,,,,,
234082,HR WHT FINE ,6/32 OZ,SEASIDE,HRV01,TUB,,X,HRF01+WATER AT THE LINE=HRV01,2210,,,,,
235082,GARLIC/W VALUE ,6/32 OZ,SEASIDE,GWV01,TUB,X,,,3547,,,,,
235119,GARLIC/W VALUE ,6/32 OZ,CORTONA,GWV01,TUB,X,,,3547,,,,,
236082,GAR/O VALUE,6/32 OZ,SEASIDE,GOV01,TUB,X,,GWV01+OIL AT THE LINE=GOV01,3547,,,,,
257213,GAR/W SV,6/32 OZ,CULINAIRE EXPRESS,GWV02,TUB,X,,,3547,3547,3515,32,3653,3763
351147,GAR FRY SCE,6/32 OZ,MONARCH ,GFS01,TUB,X,,,4017,,,,,
351209,GAR FRY SCE,6/32 OZ,T,GFS01,TUB,X,,,4017,,0,,0,0
368213S,CHPTL CHILI AIOLI,2/30 FL OZ,T,CCA01S,TUB,X,,,1800,1800,1771,29,1854,1910
370213S,CHPTL CHILI AIOLI,6/30 FL OZ,T,CCA01S,TUB,X,,,1800,1800,1771,29,1854,1910
,,,,,,,,,,, ,,  ,
PURCHASED CO-PACKED ITEMS,,,,,,,,,,,,,,
021001,GARLIC SPREAD,6/4 LB,T,FEGY,Milk & Soy,9,R,Oasis,,,0,,0,0
023162,HR SCE,12/32 OZ,INFERNO,HRS01,Nat.-Occ Sulfites,6,R,TFPW-West Coast,,,,,,
035001,GARLIC SPREAD,6/2 LB,T,FEGY,Milk & Soy,9,R,Oasis,,,0,,0,0
037001,GARLIC SPRD,2/2 LB,T,CP-FEGZ,Milk & Soy,9,R,Oasis,,,0,,0,0
158001,SCAMPI ZERO T,2/2.5 LB,T,CP-30510,Milk & Soy,12,F,Darifair.  S/L = 4 R,,,0,,0,0
169037,HR SCE,4/8 LB,SYSCO CLASSIC,HRS01,Nat.-Occ Sulfites,6,R,TFPW-West Coast,,,,,,
321036,GARLIC SPREAD,6/4 LB,ARREZZIO,,,,R,Oasis,,,,,,
335125,GARLIC SPREAD,6/2 LB,ROSELI,,,,R,Oasis,,,,,,
,,,,,,,,,,,,,,
,,,,,,,,,,,,,,
,,,,,,,,,,,,,,
,,,,,,,,,,,,,,
,,,,,,,,,,,,,,
,,,,,,,,,,,,,,
,,,,,,,,,,,,,,
,,,,,,,,,,,,,,
,,,,,,,,,,,,,,
,,,,,,,,,,,,,,
,,,,
,,,,
,,,,
,,,,
,,,,
,,,,
,,,,
,,,,
,,,,
,,,,
,,,,
,,,,
,,,,
,,,,
,,,,
,,,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
,,
'''
