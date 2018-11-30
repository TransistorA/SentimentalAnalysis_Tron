#!/usr/bin/env python

import unittest
from datetime import date
from unittest.mock import patch, Mock

from solver.shifts import ShiftsModel


class TestShiftsModel(unittest.TestCase):

    @staticmethod
    def funcChangeoverTime(i, j):
        return 1

    def setUp(self):
        self.patcher = patch('solver.shifts.date')
        self.mocker = self.patcher.start()

        # Monday :: Nov 26, 2018
        self.mocker.today = Mock(return_value=date(2018, 11, 26))
        self.addCleanup(self.patcher.stop)

    def testGetAllowedDaysWithSkippedDays(self):
        m = ShiftsModel(data={
            'num_batches': 2,
            'D': [2 * 24, 4 * 24],
            'Tp': [2, 5],
            'Ds': 48,  # skip two days
            'C_time': self.funcChangeoverTime
        })
        result = m._get_allowed_days()
        expected = [2, 3]
        self.assertEqual(result, expected)

    def testGetAllowedDaysOnWeekend(self):
        self.mocker.today = Mock(return_value=date(2018, 11, 30))
        m = ShiftsModel(data={
            'num_batches': 2,
            'D': [2 * 24, 4 * 24],
            'Tp': [2, 5],
            'Ds': 0,
            'C_time': self.funcChangeoverTime
        })
        result = m._get_allowed_days()
        expected = [0, 3]
        self.assertEqual(result, expected)

    def testValidScheduleWhenDaySkipped(self):
        m = ShiftsModel(data={
            'num_batches': 4,
            'D': [2 * 24, 2 * 24, 3 * 24, 3 * 24],
            'Tp': [2, 5, 6, 1],
            'Ds': 24,  # skip a day
            'C_time': self.funcChangeoverTime
        })
        results = m.solve(debug=False)
        #self.assertTrue(m.isValidSchedule(results))

    def testWhenBatchNeedsOvertime(self):
        # an hr for changeover
        m = ShiftsModel(data={
            'num_batches': 2,
            'D': [1 * 24, 1 * 24],
            'Tp': [2, 6],
            'Ds': 0,
            'C_time': self.funcChangeoverTime
        })
        results = m.solve(debug=False)
        #self.assertFalse(m.isValidSchedule(results))

    def testWhenBatchCannotFinishWithinWorkday(self):
        # all deadlines at the end of the first day
        m = ShiftsModel(data={
            'num_batches': 2,
            'D': [1 * 24, 1 * 24],
            'Tp': [8, 0],
            'Ds': 0,
            'C_time': self.funcChangeoverTime
        })
        results = m.solve(debug=False)
        #self.assertFalse(m.isValidSchedule(results))


if __name__ == '__main__':
    unittest.main()
