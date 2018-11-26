from __future__ import print_function
import casesNeeded
import os
import pytest


# run with $ py.test -s -v casesNeededTest.py

def resourceSetup():
	print('resources_setup()')
	with open(fileName, 'w+') as file:
		file.write(testcsv)

  
def resourceTeardown():
	print('resources_teardown()')
	os.remove(fileName)


def setupModule():
	print('\nsetupModule()')
	resourceSetup()

def teardownModule():
	print('\nteardownModule()')
	resourceTeardown()
 
def test():
	setupModule()
	print('test1()')
	cn = casesNeeded.CasesNeeded()
	cn.readFile(fileName)
	assert testItem == cn.getItem('009037')
	assert [] == cn.getItem('123456')
	
	teardownModule()

fileName = "test.csv"

testItem = [(' 09/28/2018', 29, 29), (' 10/01/2018', 488, 517), (' 10/04/2018', 128, 645), (' 10/08/2018', 100, 745)]	
testcsv = '''Tub,,,,,,
004001,HR Wht 2/Tub Tulk,30 ,,,,
8264M,98.33% ,30 ,,,,
 10/01/2018,157569,200 ,(170),HRF01,,
009037,HR Wht 6/Tub SysCl,491 ,,,,
8264M,98.33% ,491 ,,,,
 09/28/2018,157509,65 ,(29),HRF01,,**CHEP**
 10/01/2018,157436,150 ,(179),HRF01,,**CHEP**
 10/01/2018,157437,78 ,(257),HRF01,,**CHEP**
 10/01/2018,157447,260 ,(517),HRF01,,
 10/04/2018,157508,24 ,(541),HRF01,,**CHEP**
 10/04/2018,157539,78 ,(619),HRF01,,**CHEP**
 10/04/2018,157548,26 ,(645),HRF01,,**CHEP**
 10/08/2018,157560,100 ,(745),HRF01,,**CHEP**
009147,HR Wht 6/Tub Monarch,506 ,,,,
8261M,98.33% ,345 ,,,,
8263M,97.78% ,161 ,,,,
 10/01/2018,157452,39 ,(11),HRF01,,
 10/01/2018,157453,39 ,(50),HRF01,,
 10/01/2018,157454,26 ,(76),HRF01,,
 10/01/2018,157456,10 ,(86),HRF01,,
 10/01/2018,157569,260 ,(346),HRF01,,
 10/03/2018,157531,234 ,(580),HRF01,,
 10/04/2018,157444,52 ,(632),HRF01,,
025229S,Cktail Sce 24/8oz Publix,0 ,,,,
09132019M,96.67% ,6 ,,,,
 09/27/2018,157547,390 ,(390),CSR01S,,**CHEP**
047001,Gar/W 6/Tub Tulk,148 ,,,,
8261M,96.67% ,148 ,,,,
 10/02/2018,157435,39 ,(21),GWR04,,**CHEP**
 10/02/2018,157510,104 ,(125),GWR04,,**CHEP**
 10/02/2018,157511,120 ,(245),GWR04,,**CHEP**
 10/02/2018,157512,234 ,(479),GWR04,,**CHEP**
 10/02/2018,157517,13 ,(492),GWR04,,
 10/03/2018,157451,234 ,(726),GWR04,,**CHEP**
 10/03/2018,157530,273 ,(999),GWR04,,**CHEP**
047036,Gar/W 6/Tub Arrez,457 ,,,,
8260M,96.11% ,457 ,,,,
 10/04/2018,157539,78 ,(61),GWR04,,**CHEP**
 10/08/2018,157560,100 ,(161),GWR04,,**CHEP**
047125,Gar/W 6/Tub Roseli,195 ,,,,
8261M,96.67% ,195 ,,,,
 10/01/2018,157452,117 ,(107),GWR04,,
 10/01/2018,157453,52 ,(159),GWR04,,
 10/01/2018,157454,39 ,(198),GWR04,,
 10/01/2018,157455,78 ,(276),GWR04,,
 10/01/2018,157456,39 ,(315),GWR04,,
 10/01/2018,157457,78 ,(393),GWR04,,
 10/01/2018,157569,130 ,(523),GWR04,,
 10/03/2018,157531,156 ,(679),GWR04,,
 10/04/2018,157443,12 ,(691),GWR04,,
 10/04/2018,157444,31 ,(722),GWR04,,
 10/08/2018,157543,39 ,(761),GWR04,,
047300,Gar/W 6/Tub EGN,182 ,,,,
8261M,96.67% ,182 ,,,,
 10/01/2018,157569,260 ,(221),GWR04,,
 10/05/2018,157411,130 ,(351),GWR04,,
 10/11/2018,157537,130 ,(481),GWR04,,
 10/18/2018,157566,91 ,(572),GWR04,,
052001S,Tgr Sce 6/Tub Tulk,174 ,,,,
8264M,98.33% ,174 ,,,,
 10/03/2018,157530,78 ,(57),TIS01S,,**CHEP**
 10/10/2018,157561,78 ,(135),TIS01S,,**CHEP**
054001S,Cktail Sce 6/Tub Tulk,38 ,,,,
8261M,96.67% ,38 ,,,,
 09/26/2018,157333,26 ,(22),CSR01S,,
 10/02/2018,157511,39 ,(61),CSR01S,,**CHEP**
 10/02/2018,157581,2 ,(63),CSR01S,,
 10/02/2018,157584,5 ,(68),CSR01S,,
 10/02/2018,157585,2 ,(70),CSR01S,,
 10/02/2018,157596,2 ,(72),CSR01S,,
 10/02/2018,157597,2 ,(74),CSR01S,,
 10/02/2018,157600,2 ,(76),CSR01S,,
 10/02/2018,157604,2 ,(78),CSR01S,,
 10/02/2018,157605,3 ,(81),CSR01S,,
 10/02/2018,157606,4 ,(85),CSR01S,,
 10/02/2018,157610,2 ,(87),CSR01S,,
 10/02/2018,157611,7 ,(94),CSR01S,,
 10/03/2018,157530,117 ,(211),CSR01S,,**CHEP**
 10/10/2018,157561,39 ,(250),CSR01S,,**CHEP**
110202,Gin Gar Mix 6/Tub Panda,"1,618 ",,,,
031819M,97.22% ,"1,618 ",,,,
 09/28/2018,157426,600 ,(482),GIGA01,,**CHEP**
 10/01/2018,157320,800 ,"(1,282)",GIGA01,,**CHEP**
 10/01/2018,157569,130 ,"(1,412)",GIGA01,,
 10/04/2018,157412,"1,040 ","(2,452)",GIGA01,,
 10/11/2018,157564,600 ,"(3,052)",GIGA01,,
 10/15/2018,157565,800 ,"(3,852)",GIGA01,,**CHEP**
135147,Gar/W 6/Tub Monarch,439 ,,,,
8262M,97.22% ,439 ,,,,
 10/01/2018,157569,130 ,(49),GWV01,,
 10/04/2018,157443,13 ,(62),GWV01,,
 10/04/2018,157444,4 ,(66),GWV01,,
 10/08/2018,157450,39 ,(105),GWV01,,
136147,Gar/O 6/Tub Monarch,30 ,,,,
8257M,94.44% ,30 ,,,,
 09/26/2018,157396,78 ,(48),GOV01,,
 09/26/2018,157397,39 ,(87),GOV01,,
 09/26/2018,157398,39 ,(126),GOV01,,
 09/26/2018,157399,48 ,(174),GOV01,,
 09/26/2018,157402,78 ,(252),GOV01,,
 09/27/2018,157425,52 ,(304),GOV01,,
 09/27/2018,157515,130 ,(434),GOV01,,
 10/01/2018,157414,52 ,(486),GOV01,,
 10/01/2018,157449,182 ,(668),GOV01,,
 10/01/2018,157453,24 ,(692),GOV01,,
 10/01/2018,157454,16 ,(708),GOV01,,
 10/01/2018,157569,143 ,(851),GOV01,,
 10/03/2018,157531,117 ,(968),GOV01,,
140036,Gar/W 6/Tub-V Arrez,753 ,,,,
8261M,96.67% ,753 ,,,,
8267M,100.00% ,"1,037 ",,,,
 10/04/2018,157540,78 ,(12),GWV01,,**CHEP**
 10/04/2018,157548,120 ,(132),GWV01,,**CHEP**
162125,Pesto 2/Tub Roseli,28 ,,,,
8257M,94.44% ,28 ,,,,
 09/26/2018,157396,240 ,(212),PES01,,
 09/26/2018,157398,80 ,(292),PES01,,
 09/26/2018,157399,40 ,(332),PES01,,
 10/01/2018,157569,80 ,(412),PES01,,
 10/04/2018,157443,40 ,(452),PES01,,
174001,Gar/O 6/Tub Tulk,8 ,,,,
8250M,90.56% ,8 ,,,,
 10/02/2018,157517,26 ,(18),GOR01,,
174036,Gar/O 6/Tub Arrez,153 ,,,,
8257M,94.44% ,153 ,,,,
 10/01/2018,157437,234 ,(181),GOR01,,**CHEP**
 10/01/2018,157447,260 ,(441),GOR01,,
 10/04/2018,157538,52 ,(493),GOR01,,**CHEP**
195001,Ging Puree 6/Tub Tulk,1 ,,,,
09052019M,96.11% ,1 ,,,,
 10/01/2018,157569,65 ,(64),GIP01,,
 10/10/2018,157561,1 ,(65),GIP01,,**CHEP**
195036,Ging Puree 6/Tub Arrez,49 ,,,,
09052019M,96.11% ,49 ,,,,
 09/28/2018,157391,72 ,(24),GIP01,,**CHEP**
 10/04/2018,157538,52 ,(76),GIP01,,**CHEP**
199001,Ging Puree 2/Tub Tulk,2 ,,,,
09142019M,98.61% ,2 ,,,,
 10/01/2018,157453,80 ,(78),GIP01,,
200037,Gar/Olive Oil 6/Tub SysCl,162 ,,,,
8262M,97.22% ,162 ,,,,
 10/01/2018,157447,260 ,(176),GOO02,,
257213,Garlic/W V 6/Tub Cul Exp,21 ,,,,
8241M,85.56% ,21 ,,,,
 10/01/2018,157569,26 ,(5),GWV02,,
370213S,Chpt Chi Aio 6/Tub Tulk,304 ,,,,
8253M,92.22% ,10 ,,,,
8264M,98.33% ,294 ,,,,
 10/02/2018,157579,20 ,(14),CCA01S,,
 10/02/2018,157580,5 ,(19),CCA01S,,
 10/02/2018,157585,10 ,(29),CCA01S,,
 10/02/2018,157587,3 ,(32),CCA01S,,
 10/02/2018,157588,10 ,(42),CCA01S,,
 10/02/2018,157592,3 ,(45),CCA01S,,
 10/02/2018,157593,4 ,(49),CCA01S,,
 10/02/2018,157594,3 ,(52),CCA01S,,
 10/02/2018,157599,10 ,(62),CCA01S,,
 10/02/2018,157601,2 ,(64),CCA01S,,
 10/02/2018,157606,10 ,(74),CCA01S,,
 10/02/2018,157607,4 ,(78),CCA01S,,
 10/02/2018,157609,3 ,(81),CCA01S,,
 10/02/2018,157611,16 ,(97),CCA01S,,
'''