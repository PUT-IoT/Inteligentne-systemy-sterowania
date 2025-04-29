import math

import variable
def affiliation_function(x, tri_num, aff):
    b = aff * tri_num / 2
    a = b - aff / 2
    c = b + aff / 2
    return max(min(x-a/b-a, c-x/c-b), 0)

def right_sigm_function(x):
    b = variable.aff * 3 / 2
    a = b - variable.aff / 2
    return 1/(1 + math.e **(a*b-a*x))

def left_sigm_function(x):
    b = variable.aff * (-3) / 2
    a = b - variable.aff / 2
    return math.e **(a*b-a*x)/(1 + math.e **(a*b-a*x))

def regulator_fuzzy():
    e = -(variable.H_requested - variable.H_p)
    ce = (e - variable.e_prev)
    variable.e_prev = e

    # Rozmywanie
    e_values = {
        'DU' : left_sigm_function(e),
        'SU' : affiliation_function(e, -2, variable.e_aff),
        'MU' : affiliation_function(e, -1, variable.e_aff),
        'Z' : affiliation_function(e, 0, variable.e_aff),
        'MD' : affiliation_function(e, 1, variable.e_aff),
        'SD' : affiliation_function(e, 2, variable.e_aff),
        'DD' : right_sigm_function(e)
    }

    ce_values = {
        'DU' : left_sigm_function(ce),
        'SU' : affiliation_function(ce, -2, variable.ce_aff),
        'MU' : affiliation_function(ce, -1, variable.ce_aff),
        'Z' : affiliation_function(ce, 0, variable.ce_aff),
        'MD' : affiliation_function(ce, 1, variable.ce_aff),
        'SD' : affiliation_function(ce, 2, variable.ce_aff),
        'DD' : right_sigm_function(ce)
    }

    # Wnioskowanie - baza reguł
    rule_base ={
        ('DU', 'DU'): 'BDU', ('DU', 'SU'): 'BDU', ('DU', 'MU'): 'BDU', ('DU', 'Z'): 'DU', ('DU', 'MD'): 'SU', ('DU', 'SD'): 'MU', ('DU', 'DD'): 'Z',
        ('SU', 'DU'): 'BDU', ('SU', 'SU'): 'BDU', ('SU', 'MU'): 'DU', ('SU', 'Z'): 'SU', ('SU', 'MD'): 'MU', ('SU', 'SD'): 'Z', ('SU', 'DD'): 'MD',
        ('MU', 'DU'): 'BDU', ('MU', 'SU'): 'DU', ('MU', 'MU'): 'SU', ('MU', 'Z'): 'MU', ('MU', 'MD'): 'Z', ('MU', 'SD'): 'MD', ('MU', 'DD'): 'SD',
        ('Z', 'DU'): 'DU', ('Z', 'SU'): 'SU', ('Z', 'MU'): 'MU', ('Z', 'Z'): 'Z', ('Z', 'MD'): 'MD', ('Z', 'SD'): 'SD', ('Z', 'DD'): 'DD',
        ('MD', 'DU'): 'SU', ('MD', 'SU'): 'MU', ('MD', 'MU'): 'Z', ('MD', 'MD'): 'SD', ('MD', 'SD'): 'DD', ('MD', 'DD'): 'BDD',
        ('SD', 'DU'): 'MU', ('SD', 'SU'): 'Z', ('SD', 'MU'): 'MD', ('SD', 'Z'): 'SD', ('SD', 'MD'): 'DD', ('SD', 'SD'): 'BDD', ('SD', 'DD'): 'BDD',
        ('DD', 'DU'): 'Z', ('DD', 'SU'): 'MD', ('DD', 'MU'): 'SD', ('DD', 'Z'): 'DD', ('DD', 'MD'): 'BDD', ('DD', 'SD'): 'BDD', ('DD', 'DD'): 'BDD' 
    }

    if e == 2 and ce == 4:
        # u = ...
        pass