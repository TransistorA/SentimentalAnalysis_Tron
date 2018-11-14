#!/usr/bin/env python

import pyomo.environ

from pyomo.environ import *

from deadline_overlapping import DeadlineOverlappingModel

TOTALTIME = 7 * 24 * 60  # number of minutes in a week to make it large enough


class ChangeoverAllergenModel(DeadlineOverlappingModel):
    """IP model with the following constraints
        - Normal Changeover time
        - Changeover time for Allergens
    """

    def __init__(self, data):
        DeadlineOverlappingModel.__init__(self, data)

		ChangeoverAllergenModel.setupConstraints(self)

    def get_changeovertime(self, i, j):
        return 0.1

    def get_allergen_time(self, i, j):
        return 0.1

    def setupConstraints(self):
        def changeovertime_rule(model, i, j):
            """end time of i + changeover time between i & j <= start time of j"""
            return model.Ts[j] - model.Ts[i] - self.Tp[i] + TOTALTIME * (1 - model.P[i, j]) >= self.get_changeovertime(
                i, j) + self.get_allergen_time(i, j)


    def solve(self, debug=False):
        results = SimpleModel.solve(self, debug)
        return results

