#!/usr/bin/env python

import math
from datetime import date

from .changeover_allergen import ChangeoverAllergenModel
from pyomo.environ import *
from .simple_model import SimpleModel

WORKDAY_BEGIN = 8
HOURS_IN_WORKDAY = 8


class ShiftsModel(ChangeoverAllergenModel):
    """IP model with the following constraints
        - Deadline
        - Overlapping
        - Changeover time
        - Shifts
    """

    def _get_allowed_days(self):
        first_day = int(math.ceil(self.Ds / 24.0))
        last_day = int(math.ceil(self.Dl / 24.0))
        offset = date.today().weekday()

        res = []
        for day in range(first_day, last_day):
            if (day + offset) % 7 != 5 and (day + offset) % 7 != 6:
                res.append(day)
        return res

    def __init__(self, data):
        ChangeoverAllergenModel.__init__(self, data)

        # number of (allowed) day on which batch is scheduled
        self.model.d = Var(self.model.Range)

        ShiftsModel.setupConstraints(self)

    def setupConstraints(self):
        allowed = Set(initialize=self._get_allowed_days())
        self.model.select_d = Var(allowed * self.model.Range, domain=Binary)

        def pick_one_d(model, i):
            return 1 == sum(model.select_d[j, i] for j in allowed)

        self.model.pick_one_d = Constraint(self.model.Range, rule=pick_one_d)

        def set_d(model, i):
            return model.d[i] == sum(j * model.select_d[j, i] for j in allowed)

        self.model.set_d = Constraint(self.model.Range, rule=set_d)

        def shift_start_rule1(model, i):
            return 24 * model.d[i] + WORKDAY_BEGIN <= model.Ts[i]

        self.model.shift_start1 = Constraint(
            self.model.Range, rule=shift_start_rule1)

        def shift_end_rule1(model, i):
            return model.Ts[i] <= 24 * model.d[i] + (WORKDAY_BEGIN + HOURS_IN_WORKDAY)

        self.model.shift_end1 = Constraint(
            self.model.Range, rule=shift_end_rule1)

        def shift_start_rule2(model, i):
            return 24 * model.d[i] + WORKDAY_BEGIN <= model.Ts[i] + self.Tp[i]

        self.model.shift_start2 = Constraint(
            self.model.Range, rule=shift_start_rule2)

        def shift_end_rule2(model, i):
            return model.Ts[i] + self.Tp[i] <= 24 * model.d[i] + (WORKDAY_BEGIN + HOURS_IN_WORKDAY)

        self.model.shift_end2 = Constraint(
            self.model.Range, rule=shift_end_rule2)

    def solve(self, debug=False):
        results = SimpleModel.solve(self, debug)
        if debug:
            self.model.Ts.display()
            self.model.P.display()
        return results

    def isValidSchedule(self, results):
        """Checks if the results correspond to a valid or feasible
        schedule
        :param results  solved model results
        :return [boolean] True if schedule is valid, False otherwise
        """
        result = ChangeoverAllergenModel.isValidSchedule(self, results)
        if not result:
            return False

        allowed_days = self._get_allowed_days()
        for i in self.model.Range:
            start = self.model.Ts[i].value
            end = self.model.Ts[i].value + self.Tp[i]

            found = False
            # ensure that batch i production starts and ends within allowed
            # workday(s), this fails if a batch takes longer than HOURS_IN_WORKDAY
            # as start and end times would not be on the same day
            for day in allowed_days:
                if (24 * day + WORKDAY_BEGIN <= start <= 24 * day + WORKDAY_BEGIN + HOURS_IN_WORKDAY
                        and 24 * day + WORKDAY_BEGIN <= end <= 24 * day + WORKDAY_BEGIN + HOURS_IN_WORKDAY):
                    found = True

            if not found:
                return False

        return True
