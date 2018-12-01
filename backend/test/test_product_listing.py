from __future__ import print_function

import os
import unittest

import src.constants as constants
import src.product_listing as product_listing
from src.allergen import Allergen


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

        expected = ['GARLIC IN OIL',
                    '400# Drum',
                    'Tulkoff',
                    'GOR01',
                    'na',
                    '',
                    '',
                    '',
                    Allergen.NONE,
                    'PAIL',
                    7,
                    30]
        self.assertEqual(pl.getItem('086001'), expected)

        # pl.saveProductListing(savedListing)
        # pl2 = prodList.ProductListing()
        # pl2.loadProductListing(savedListing)
        # assert len(pl.items) == len(pl2.items)
        # assert pl.getItem('043113') == pl2.getItem('043113')

    def testConstants(self):
        assert constants.ALLERGEN_VALUE == 8
