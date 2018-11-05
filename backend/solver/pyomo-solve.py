#!/usr/bin/env python

import itertools
import pyomo.environ

from pyomo.core.base.expr import Expr_if
from pyomo.environ import *
from pyomo.opt import SolverFactory

model = ConcreteModel()

num_batches = 4  # number of batches
D = [10, 8, 10, 12]  # deadline of batch i
Tp = [2, 5, 1, 3]  # time to finish batch i

Ds = 0  # time when scheduling starts
Dl = max(D)  # last deadline
Tr = Dl - Ds    # total time available


model.Range = Set(initialize=range(num_batches))

## VARIABLES ##

# start time of batch i
model.Ts = Var(model.Range,
               bounds=(0, Tr),
               domain=NonNegativeIntegers)

# P[i, j] = 1 if batch i starts before batch j, 0 otherwise
# i, j = 1, 2,..., num_batches (i != j)
ij_pairs = list(itertools.permutations(range(num_batches), r=2))
model.P = Var(ij_pairs, domain=Binary)


def Pij_cons_rule1(model, i, j):
    return model.Ts[j] >= model.Ts[i] + 1 - 80 * (1 - model.P[i, j])
model.Pij_cons1 = Constraint(ij_pairs, rule=Pij_cons_rule1)


def Pij_cons_rule2(model, i, j):
    return model.Ts[i] >= model.Ts[j] + 1 - 80 * model.P[i, j]
model.Pij_cons2 = Constraint(ij_pairs, rule=Pij_cons_rule2)


## CONSTRAINTS ##

def bounded_rule1(model, i, j):
    """ensure that batches i and j are not separated by more
    than the time available"""
    return model.Ts[i] - model.Ts[j] <= Tr * (1 - model.P[i, j])
model.bounded = Constraint(ij_pairs, rule=bounded_rule1)


def bounded_rule2(model, i, j):
    return -1 * Tr * model.P[i, j] <= model.Ts[i] - model.Ts[j]
model.bounded2 = Constraint(ij_pairs, rule=bounded_rule2)


def overlapping_rule1(model, i, j):
    """ensure that batches i and j do not overlap"""
    return model.Ts[j] - (model.Ts[i] + Tp[i]) >= Tr * (model.P[i, j] - 1)
model.overlapping = Constraint(ij_pairs, rule=overlapping_rule1)


def overlapping_rule2(model, i, j):
    return (model.Ts[j] + Tp[j]) - model.Ts[i] <= Tr * model.P[i, j]
model.overlapping2 = Constraint(ij_pairs, rule=overlapping_rule2)


def deadline_rule(model, i):
    """ensure that deadline is met for batch i"""
    return model.Ts[i] + Tp[i] <= D[i]
model.deadline = Constraint(model.Range, rule=deadline_rule)


## OBJECTIVE ##

total_time_taken = sum(model.Ts[i] for i in range(num_batches))
model.object = Objective(expr=total_time_taken, sense=minimize)


def pyomo_postprocess(options=None, instance=None, results=None):
    model.Ts.display()
    model.P.display()


opt = SolverFactory("glpk")
results = opt.solve(model)
results.write()
pyomo_postprocess(None, model, None)
