#!/usr/bin/env python

import unittest

from solver.changeover_allergen import ChangeoverAllergenModel


class TestChangeoverAllergen(unittest.TestCase):

    @staticmethod
    def funcChangeoverTime(i, j):
        return 1

    def testIsScheduleValid(self):
        m = ChangeoverAllergenModel(data={
            'num_batches': 3,
            'D': [20, 20, 20],
            'Tp': [4, 6, 8],
            'Ds': 0,
            'C_time': self.funcChangeoverTime
        })
        results = m.solve(debug=False)
        self.assertTrue(m.isValidSchedule(results))

    def testWhenChangeoverTimeTooLarge(self):
        m = ChangeoverAllergenModel(data={
            'num_batches': 2,
            'D': [2, 2],
            'Tp': [1, 1],
            'Ds': 0,
            'C_time': self.funcChangeoverTime
        })
        results = m.solve(debug=False)
        self.assertFalse(m.isValidSchedule(results))


if __name__ == '__main__':
    unittest.main()
