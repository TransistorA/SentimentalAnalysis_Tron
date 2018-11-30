from __future__ import print_function

import os
import unittest

import src.cases_needed as cases_needed


class TestCasesNeeded(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testFunc(self):
        cn = cases_needed.CasesNeeded()
        casesNeededFile = os.path.join(os.path.dirname(__file__),
                                       'fixtures',
                                       'cases_needed.csv')
        cn.readFile(casesNeededFile)

        result = cn.getItem('009037')
        expected = [(' 09/28/2018', 29, 29),
                    (' 10/01/2018', 488, 517),
                    (' 10/04/2018', 128, 645),
                    (' 10/08/2018', 100, 745)]
        self.assertEqual(result, expected)

        self.assertEqual(cn.getItem('123456'), [])
