#!/usr/bin/env python

import unittest

from solver.shifts import ShiftsModel


class TestShiftsModel(unittest.TestCase):

    def testIsScheduleValid(self):
        m = ShiftsModel(data={
            'num_batches': 4,
            'D': [2 * 24, 2 * 24, 3 * 24, 3 * 24],
            'Tp': [2, 5, 6, 1],
            'Ds': 24,   # skip a day
            'C_time': self.funcChangeoverTime
        })
        results = m.solve(debug=False)
        self.assertTrue(m.isValidSchedule(results))

    def funcChangeoverTime(self, i, j):
        return 1


if __name__ == '__main__':
    unittest.main()
