#!/usr/bin/env python

import pyomo.environ

from pyomo.environ import *

from changeover_allergen import ChangeoverAllergenModel
from simple_model import SimpleModel

class KosherModel(ChangeoverAllergenModel):
    """IP model with the following constraints
        - Normal Changeover time
        - Changeover time for Allergens
    """

    def __init__(self, data):
        ChangeoverAllergenModel.__init__(self, data)

        self.C_time = data['C_time']

        KosherModel.setupConstraints(self)

    def setupConstraints(self):
        def changeovertime_rule(model, i, j):
            return model.Ts[j] - model.Ts[i] - self.Tp[i] + TOTALTIME * (1 - model.P[i, j]) >= self.C_time(
                i, j)
        
    def addObjective(self):
        totalTimeTaken = sum(self.model.Ts[i]
                             for i in range(self.num_batches))
        self.model.object = Objective(expr=totalTimeTaken, sense=minimize)
        

    def solve(self, debug=False):
        results = SimpleModel.solve(self, debug)
        return results

