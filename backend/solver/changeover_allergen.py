#!/usr/bin/env python

import pyomo.environ

from pyomo.environ import *

from deadline_overlapping import DeadlineOverlappingModel


class ChangeoverAllergenModel(DeadlineOverlappingModel):

    def __init__(self, data):
        DeadlineOverlappingModel.__init__(self, data)

        ChangeoverAllergenModel.setupConstraints(self)

    def setupConstraints(self):
        pass
        # def changeover_rule(model, i, j):
        #     return (model.Ts[j] - model.Ts[i] - self.Tp[i]) * model.P[i, j] >= 0
        # self.model.changeover = Constraint(self.ij_pairs, rule=changeover_rule)
