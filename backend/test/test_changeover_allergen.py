#!/usr/bin/env python
import unittest

from solver.changeover_allergen import ChangeoverAllergenModel
#from datarefine.getdata import *

class TestChangeoverAllergen(unittest.TestCase):

    def testIsScheduleValid(self):
        m = ChangeoverAllergenModel(data={
            'num_batches': 4,
            'D': [20, 20, 20, 20],
            'Tp': [2, 5, 1, 3],
            'Ds': 0,
            'C_time': self.functionChangeover
        })
        results = m.solve(debug=False)
        self.assertTrue(m.isValidSchedule(results))

    def functionChangeover(self, i, j):
        return 0.1

    def testIsScheduleInvalid(self):
        m = ChangeoverAllergenModel(data={
            'num_batches': 2,
            'D': [10, 8],
            'Tp': [8, 2],
            'Ds': 1,
            'C_time': self.functionChangeover
        })
        results = m.solve(debug=False)
        self.assertFalse(m.isValidSchedule(results))


if __name__ == '__main__':
    unittest.main()
