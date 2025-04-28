import math

import variable
def affiliation_function(x, tri_num):
    b = variable.aff * tri_num / 2
    a = b - variable.aff / 2
    c = b - variable.aff / 2
    return max(min(x-a/b-a, c-x/c-b), 0)

def right_sigm_function(x):
    b = variable.aff * 4 / 2
    a = b - variable.aff / 2
    return 1/(1 + math.e **(a*b-a*x))

def left_sigm_function(x):
    b = variable.aff * (-4) / 2
    a = b - variable.aff / 2
    return math.e **(a*b-a*x)/(1 + math.e **(a*b-a*x))

def regulator_fuzzy():
    e = 2
    ce = 4
    if e == 2 and ce == 4:
        # u = ...
        pass