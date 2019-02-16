from __future__ import print_function

import os
import unittest

import src.product_listing as product_listing
from src.allergen import Allergen
from src.constants import *


class TestProductListing(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testFunc(self):
        pl = product_listing.ProductListing()
        productListingFile = os.path.join(os.path.dirname(__file__),
                                          'fixtures',
                                          'product_listing.csv')

        pl.readNewFile(productListingFile)

        expected = ['HR WHITE', 
                    '6/32 OZ', 
                    'Sysco Classic', 
                    'HRF01', 
                    'na', 
                    'blue pallet', 
                    '', 
                    '', 
                    Allergen.NONE, 
                    'TUB', 
                    165, 
                    0.35, 
                    0]

        self.assertEqual(pl.getItem('009037'), expected)

        # pl.saveProductListing(savedListing)
        # pl2 = prodList.ProductListing()
        # pl2.loadProductListing(savedListing)
        # assert len(pl.items) == len(pl2.items)
        # assert pl.getItem('043113') == pl2.getItem('043113')

    def testConstants(self):
        assert ALLERGEN_VALUE == 8
