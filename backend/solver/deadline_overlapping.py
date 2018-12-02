#!/usr/bin/env python

import itertools

from pyomo.environ import *
from .simple_model import SimpleModel


class DeadlineOverlappingModel(SimpleModel):
    """IP model with the following constraints
        - Deadline
        - Overlapping
        - Changeover time
    """

    def __init__(self, data):
        SimpleModel.__init__(self, data)

        self.D = data['D']                  # batch deadlines
        self.Tp = data['Tp']                # time to finish batch
        self.Ds = data.get('Ds', 0)         # hours to skip
        self.Dl = max(self.D)               # last deadline
        self.Tr = self.Dl - self.Ds         # total time available

        # batch start time
        self.model.Ts = Var(self.model.Range,
                            bounds=(self.Ds, self.Dl),
                            domain=NonNegativeIntegers)

        # P[i, j] = 1 if batch i starts before batch j, 0 otherwise
        # i, j = 1, 2,..., num_batches (i != j)
        self.ij_pairs = list(itertools.permutations(
            range(self.num_batches), r=2))
        self.model.P = Var(self.ij_pairs, domain=Binary)

        DeadlineOverlappingModel.setupConstraints(self)
        DeadlineOverlappingModel.addObjective(self)

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
            return model.Ts[j] - (model.Ts[i] + self.Tp[i]) >= self.Tr * (model.P[i, j] - 1)
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
        totalTimeTaken = sum(self.model.Ts[i]
                             for i in range(self.num_batches))
        self.model.object = Objective(expr=totalTimeTaken, sense=minimize)

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
        result = SimpleModel.isValidSchedule(self, results)
        if not result:
            return False

        startTimes = []
        for i in self.model.Range:
            start = self.model.Ts[i].value
            # ensure batch i is finished before deadline
            if start < 0 or (start + self.Tp[i]) > self.D[i]:
                return False
            startTimes.append((start, i))

        startTimes.sort()
        for i in range(self.num_batches - 1):
            batchIdx = startTimes[i][1]
            # ensure batch i's production does not overlap with the
            # upcoming batch
            if startTimes[i][0] + self.Tp[batchIdx] > startTimes[i + 1][0]:
                return False

        return True
