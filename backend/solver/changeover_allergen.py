#!/usr/bin/env python

from deadline_overlapping import DeadlineOverlappingModel
from pyomo.environ import *
from simple_model import SimpleModel

TOTAL_TIME = 7 * 24 * 60  # number of minutes in a week to make it large enough


class ChangeoverAllergenModel(DeadlineOverlappingModel):
    """IP model with the following constraints
        - Normal Changeover time
        - Changeover time for Allergens
    """

    def __init__(self, data):
        DeadlineOverlappingModel.__init__(self, data)

        self.C_time = data['C_time']

        ChangeoverAllergenModel.setupConstraints(self)

    def setupConstraints(self):
        def changeover_rule(model, i, j):
            """end time of i + changeover time between i & j <= start time of j"""
            return model.Ts[j] - (model.Ts[i] + self.Tp[i]) + TOTAL_TIME * (1 - model.P[i, j]) >= self.C_time(i, j)

        self.model.changeover = Constraint(self.ij_pairs, rule=changeover_rule)

    def solve(self, debug=False):
        results = SimpleModel.solve(self, debug)
        if debug:
            self.model.Ts.display()
            self.model.P.display()
        return results
