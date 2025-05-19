import math
import const
import variable
def affiliation_function(x, tri_num, aff):
    b = aff * tri_num / 2
    a = b - aff / 2
    c = b + aff / 2
    return max(min((x-a)/(b-a), (c-x)/(c-b)), 0)

def affiliation_function_left(x, aff):
    b = aff * -3 / 2
    c = b + aff / 2
    return max(min(1, (c - x) / (c - b)), 0)

def affiliation_function_right(x, aff):
    b = aff * 3 / 2
    a = b - aff / 2
    return max(min((x-a)/(b-a), 1), 0)

def right_sigm_function(x, aff):
    b = aff * 3 / 2
    a = b - aff / 2
    return 1/(1 + math.e **(a*b-a*x))

def left_sigm_function(x, aff):
    b = aff * (-3) / 2
    a = b - aff / 2
    return math.e **(a*b-a*x)/(1 + math.e **(a*b-a*x))

def defuzzify(aggregated_output, output_mapping, aff):
    min_x = -4 * aff  # lub dopasuj do swoich danych
    max_x = 4 * aff
    step = 0.01
    x_values = [min_x + i * step for i in range(int((max_x - min_x) / step))]

    numerator = 0
    denominator = 0

    for x in x_values:
        mu_total = 0
        for label, strength in aggregated_output.items():
            center = output_mapping[label]
            mu = affiliation_function(x, center / aff, aff)  # tri_num = center / aff
            mu_total = max(mu_total, mu * strength)

        numerator += x * mu_total
        denominator += mu_total

    return numerator / denominator if denominator != 0 else 0

def regulator_fuzzy():
    e = variable.H_requested - variable.H_p
    ce = (e - variable.e_prev)
    variable.e_prev = e

    # Rozmywanie
    e_values = {
        'DU' : affiliation_function_left(e, variable.e_aff),
        'SU' : affiliation_function(e, -2, variable.e_aff),
        'MU' : affiliation_function(e, -1, variable.e_aff),
        'Z' : affiliation_function(e, 0, variable.e_aff),
        'MD' : affiliation_function(e, 1, variable.e_aff),
        'SD' : affiliation_function(e, 2, variable.e_aff),
        'DD' : affiliation_function_right(e, variable.e_aff)
    }

    ce_values = {
        'DU' : affiliation_function_left(ce, variable.ce_aff),
        'SU' : affiliation_function(ce, -2, variable.ce_aff),
        'MU' : affiliation_function(ce, -1, variable.ce_aff),
        'Z' : affiliation_function(ce, 0, variable.ce_aff),
        'MD' : affiliation_function(ce, 1, variable.ce_aff),
        'SD' : affiliation_function(ce, 2, variable.ce_aff),
        'DD' : affiliation_function_right(ce, variable.ce_aff)
    }

    # Wnioskowanie - baza reguł
    rule_base ={
        ('DU', 'DU'): 'BDU', ('DU', 'SU'): 'BDU', ('DU', 'MU'): 'BDU', ('DU', 'Z'): 'DU', ('DU', 'MD'): 'SU', ('DU', 'SD'): 'MU', ('DU', 'DD'): 'Z',
        ('SU', 'DU'): 'BDU', ('SU', 'SU'): 'BDU', ('SU', 'MU'): 'DU', ('SU', 'Z'): 'SU', ('SU', 'MD'): 'MU', ('SU', 'SD'): 'Z', ('SU', 'DD'): 'MD',
        ('MU', 'DU'): 'BDU', ('MU', 'SU'): 'DU', ('MU', 'MU'): 'SU', ('MU', 'Z'): 'MU', ('MU', 'MD'): 'Z', ('MU', 'SD'): 'MD', ('MU', 'DD'): 'SD',
        ('Z', 'DU'): 'DU', ('Z', 'SU'): 'SU', ('Z', 'MU'): 'MU', ('Z', 'Z'): 'Z', ('Z', 'MD'): 'MD', ('Z', 'SD'): 'SD', ('Z', 'DD'): 'DD',
        ('MD', 'DU'): 'SU', ('MD', 'SU'): 'MU', ('MD', 'MU'): 'Z', ('MD', 'Z'): 'MD', ('MD', 'MD'): 'SD', ('MD', 'SD'): 'DD', ('MD', 'DD'): 'BDD',
        ('SD', 'DU'): 'MU', ('SD', 'SU'): 'Z', ('SD', 'MU'): 'MD', ('SD', 'Z'): 'SD', ('SD', 'MD'): 'DD', ('SD', 'SD'): 'BDD', ('SD', 'DD'): 'BDD',
        ('DD', 'DU'): 'Z', ('DD', 'SU'): 'MD', ('DD', 'MU'): 'SD', ('DD', 'Z'): 'DD', ('DD', 'MD'): 'BDD', ('DD', 'SD'): 'BDD', ('DD', 'DD'): 'BDD'
    }

    # output_mapping = {
    #     'BDU': variable.BDU,
    #     'DU': variable.DU,
    #     'SU': variable.SU,
    #     'MU': variable.MU,
    #     'Z': variable.Z,
    #     'MD': variable.MD,
    #     'SD': variable.SD,
    #     'DD': variable.DD,
    #     'BDD': variable.BDD
    # }
    output_mapping = {
        'BDU': 8.2,
        'DU': 1.9,
        'SU': 1.8,
        'MU': 1.6,
        'Z': 1.8,
        'MD': 1.6,
        'SD': 1.8,
        'DD': 1.8,
        'BDD': 8
    }


    # Wnioskowanie - cd.

    aggregated_output = {label: 0 for label in output_mapping}

    for e_key, e_mu in e_values.items():
        for ce_key, ce_mu in ce_values.items():
            if e_mu > 0 and ce_mu > 0:
                # Operator T-normy -> MIN
                strength = min(e_mu, ce_mu)
                rule_lable = rule_base.get((e_key, ce_key))
                # # operator S-normy -> MAX
                aggregated_output[rule_lable] = max(aggregated_output[rule_lable], strength)


    # TODO
    # Wysotrzanie
    output = defuzzify(aggregated_output, output_mapping, variable.output_aff)
    return output

def rescale_u(u):
    new_u = const.U_min + (const.U_max - const.U_min) * (u - const.U_min_pi_fuzzy) / (const.U_max_pi_fuzzy - const.U_min_pi_fuzzy)
    return new_u