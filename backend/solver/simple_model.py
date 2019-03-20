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

    def solve(self, debug=False, **kwargs):
        solver = kwargs.get('solver', 'glpk')
        timelimit = kwargs.get('timelimit', 60)

        if solver == 'gurobi':
            opt = SolverFactory('gurobi_direct')
            opt.options['timelimit'] = timelimit
        else:
            opt = SolverFactory('glpk')
            opt.options['tmlim'] = timelimit

        # change tee=False if you don't want to see solver updates
        results = opt.solve(self.model, tee=True)
        if debug:
            results.write()

        return results

    def isValidSchedule(self, results):
        return results.solver.termination_condition != TerminationCondition.infeasible
