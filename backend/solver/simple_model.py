#!/usr/bin/env python

from pyomo.environ import *
from pyomo.opt import SolverFactory, TerminationCondition


class SimpleModel:
    """Barebone IP model"""

    def __init__(self, data):
        self.model = ConcreteModel()

        self.num_batches = data['num_batches']
        # Range = {0, 1, ..., num_batches - 1}
        self.model.Range = Set(initialize=range(self.num_batches))

    def modelInstance(self):
        return self.model

    def solve(self, debug=False):
        opt = SolverFactory("glpk")
        results = opt.solve(self.model)
        if debug:
            results.write()

        return results

    def isValidSchedule(self, results):
        return results.solver.termination_condition != TerminationCondition.infeasible
