#!/usr/bin/env python

import itertools
import pyomo.environ

from pyomo.environ import *

from simple_model import SimpleModel


class DeadlineOverlappingModel(SimpleModel):
    """IP model with the following constraints
        - Deadline
        - Overlapping
    """

    def __init__(self, data):
        SimpleModel.__init__(self, data)

        self.D = data['D']                  # batch deadlines
        self.Tp = data['Tp']                # time to finish batch
        self.Tr = max(self.D) - data['Ds']  # total time available

        # batch start time
        self.model.Ts = Var(self.model.Range,
                            bounds=(0, Tr),
                            domain=NonNegativeIntegers)

        # P[i, j] = 1 if batch i starts before batch j, 0 otherwise
        # i, j = 1, 2,..., num_batches (i != j)
        self.ij_pairs = list(itertools.permutations(
            range(self.num_batches), r=2))
        self.model.P = Var(self.ij_pairs, domain=Binary)

        self.setupConstraints()
        self.addObjective()

    def setupConstraints(self):
        """Adds rules specific to deadline and overlapping constraints"""
        def Pij_cons_rule1(model, i, j):
            return model.Ts[j] >= model.Ts[i] + 1 - 80 * (1 - model.P[i, j])
        self.model.Pij_cons1 = Constraint(self.ij_pairs, rule=Pij_cons_rule1)

        def Pij_cons_rule2(model, i, j):
            return model.Ts[i] >= model.Ts[j] + 1 - 80 * model.P[i, j]
        self.model.Pij_cons2 = Constraint(self.ij_pairs, rule=Pij_cons_rule2)

        def bounded_rule1(model, i, j):
            """ensure that batches i and j are not separated by more
            than the time available"""
            return model.Ts[i] - model.Ts[j] <= self.Tr * (1 - model.P[i, j])
        self.model.bounded = Constraint(self.ij_pairs, rule=bounded_rule1)

        def bounded_rule2(model, i, j):
            return -1 * self.Tr * model.P[i, j] <= model.Ts[i] - model.Ts[j]
        self.model.bounded2 = Constraint(self.ij_pairs, rule=bounded_rule2)

        def overlapping_rule1(model, i, j):
            """ensure that batches i and j do not overlap"""
            return model.Ts[j] - (model.Ts[i] + Tp[i]) >= self.Tr * (model.P[i, j] - 1)
        self.model.overlapping = Constraint(
            self.ij_pairs, rule=overlapping_rule1)

        def overlapping_rule2(model, i, j):
            return (model.Ts[j] + self.Tp[j]) - model.Ts[i] <= self.Tr * model.P[i, j]
        self.model.overlapping2 = Constraint(
            self.ij_pairs, rule=overlapping_rule2)

        def deadline_rule(model, i):
            """ensure that deadline is met for batch i"""
            return model.Ts[i] + self.Tp[i] <= self.D[i]
        self.model.deadline = Constraint(self.model.Range, rule=deadline_rule)

    def addObjective(self):
        total_time_taken = sum(self.model.Ts[i]
                               for i in range(self.num_batches))
        self.model.object = Objective(expr=total_time_taken, sense=minimize)

    def solve(self, debug=False):
        results = SimpleModel.solve(self, debug)
        if debug:
            self.model.Ts.display()
            self.model.P.display()

        return results


num_batches = 4  # number of batches
D = [10, 8, 10, 12]  # deadline of batch i
Tp = [2, 5, 1, 3]  # time to finish batch i

Ds = 0  # time when scheduling starts
Dl = max(D)  # last deadline
Tr = Dl - Ds    # total time available


m = DeadlineOverlappingModel(data={
    'num_batches': num_batches,
    'D': D,
    'Tp': Tp,
    'Ds': Ds
})

results = m.solve(debug=True)
