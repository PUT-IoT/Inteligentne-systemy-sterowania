import numpy as np
import variable
import const

# Definicje funkcji przynależności

def membership(value, centers, width=1.0):
    memberships = {}
    for label, center in centers.items():
        memberships[label] = max(0.0, 1.0 - abs(value - center) / width)
    return memberships

# Funkcje fuzzifikacji

def fuzzify_e(e):
    centers = {
        'NB': -3,
        'NM': -2,
        'NS': -1,
        'ZE':  0,
        'PS':  1,
        'PM':  2,
        'PB':  3
    }
    return membership(e, centers, width=1.5)

def fuzzify_de(de):
    centers = {
        'NB': -3,
        'NM': -2,
        'NS': -1,
        'ZE':  0,
        'PS':  1,
        'PM':  2,
        'PB':  3
    }
    return membership(de, centers, width=1.5)

# Tablica reguł sterowania (uchyb, zmiana uchybu) -> zmiana Uz
rules = {
    ('NB', 'NB'): 'PB', ('NB', 'NM'): 'PB', ('NB', 'NS'): 'PM', ('NB', 'ZE'): 'PM', ('NB', 'PS'): 'PS', ('NB', 'PM'): 'ZE', ('NB', 'PB'): 'ZE',
    ('NM', 'NB'): 'PB', ('NM', 'NM'): 'PM', ('NM', 'NS'): 'PM', ('NM', 'ZE'): 'PS', ('NM', 'PS'): 'ZE', ('NM', 'PM'): 'NS', ('NM', 'PB'): 'NS',
    ('NS', 'NB'): 'PM', ('NS', 'NM'): 'PM', ('NS', 'NS'): 'PS', ('NS', 'ZE'): 'ZE', ('NS', 'PS'): 'NS', ('NS', 'PM'): 'NM', ('NS', 'PB'): 'NM',
    ('ZE', 'NB'): 'PM', ('ZE', 'NM'): 'PS', ('ZE', 'NS'): 'ZE', ('ZE', 'ZE'): 'ZE', ('ZE', 'PS'): 'ZE', ('ZE', 'PM'): 'NS', ('ZE', 'PB'): 'NM',
    ('PS', 'NB'): 'PS', ('PS', 'NM'): 'ZE', ('PS', 'NS'): 'NS', ('PS', 'ZE'): 'NS', ('PS', 'PS'): 'NM', ('PS', 'PM'): 'NM', ('PS', 'PB'): 'NB',
    ('PM', 'NB'): 'ZE', ('PM', 'NM'): 'NS', ('PM', 'NS'): 'NM', ('PM', 'ZE'): 'NM', ('PM', 'PS'): 'NB', ('PM', 'PM'): 'NB', ('PM', 'PB'): 'NB',
    ('PB', 'NB'): 'NS', ('PB', 'NM'): 'NM', ('PB', 'NS'): 'NB', ('PB', 'ZE'): 'NB', ('PB', 'PS'): 'NB', ('PB', 'PM'): 'NB', ('PB', 'PB'): 'NB'
}

# Wyjściowe zmiany Uz dla etykiet
output_values = {
    'NB': -3,
    'NM': -2,
    'NS': -1,
    'ZE':  0,
    'PS':  1,
    'PM':  2,
    'PB':  3
}

def fuzzy_controller():
    e = -(variable.H_requested - variable.H_p)
    de = (e - variable.e_prev) / const.T_p
    variable.e_prev = e

    e_m = fuzzify_e(e)
    de_m = fuzzify_de(de)

    numerator = 0.0
    denominator = 0.0

    for e_label, e_val in e_m.items():
        for de_label, de_val in de_m.items():
            weight = min(e_val, de_val)
            action = rules.get((e_label, de_label), 'ZE')
            delta_u = output_values[action]

            numerator += weight * delta_u
            denominator += weight

    if denominator == 0:
        output = 0
    else:
        output = numerator / denominator

    variable.fuzzy_u += output * 0.5  # skalowanie zmiany napięcia

    # Ograniczenie napiecia
    variable.fuzzy_u = min(const.U_max_pi, max(const.U_min_pi, variable.fuzzy_u))

    return variable.fuzzy_u

def rescale_u(u):
    new_u = const.U_min + (const.U_max - const.U_min) * (u - const.U_min_pi) / (const.U_max_pi - const.U_min_pi)
    return new_u
