import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import variable
import const
import equations

# Zakresy wejściowe
e_range = np.arange(-5, 5.01, 0.01)
de_range = np.arange(-1, 1.01, 0.01)

# Wyjście fuzzy to zmiana względem napięcia równowagi
delta_u_range = np.arange(-120, 120.1, 0.1)

# Tworzenie zmiennych rozmytych
e = ctrl.Antecedent(e_range, 'e')
de = ctrl.Antecedent(de_range, 'de')
delta_u = ctrl.Consequent(delta_u_range, 'delta_u')

# Etykiety
labels = ['BDU', 'DU', 'SU', 'MU', 'Z', 'MD', 'SD', 'DD', 'BDD']

# Szerokość przynależności
aff = 0.5

# Rozkład funkcji przynależności dla e i de
centers_e = np.linspace(-4, 4, 9)
for label, c in zip(labels, centers_e):
    e[label] = fuzz.trimf(e_range, [c - aff, c, c + aff])
    de[label] = fuzz.trimf(de_range, [c / 4 - aff / 2, c / 4, c / 4 + aff / 2])

# Rozkład funkcji przynależności dla delta_u
centers_du = [-120, -80, -40, -20, 0, 20, 40, 80, 120]
for label, c in zip(labels, centers_du):
    delta_u[label] = fuzz.trimf(delta_u_range, [c - 20, c, c + 20])

# Zestaw reguł fuzzy
rules = []

# Reguły podstawowe symetryczne
rules += [
    ctrl.Rule(e['BDU'] & de['BDU'], delta_u['BDD']),
    ctrl.Rule(e['DU'] & de['DU'], delta_u['DD']),
    ctrl.Rule(e['SU'] & de['SU'], delta_u['SD']),
    ctrl.Rule(e['MU'] & de['MU'], delta_u['MD']),
    ctrl.Rule(e['Z'] & de['Z'], delta_u['Z']),
    ctrl.Rule(e['MD'] & de['MD'], delta_u['MU']),
    ctrl.Rule(e['SD'] & de['SD'], delta_u['SU']),
    ctrl.Rule(e['DD'] & de['DD'], delta_u['DU']),
    ctrl.Rule(e['BDD'] & de['BDD'], delta_u['BDU'])
]

# Reguły wyhamowujące
rules += [
    ctrl.Rule(e['Z'] & de['MD'], delta_u['Z']),
    ctrl.Rule(e['Z'] & de['SD'], delta_u['Z']),
    ctrl.Rule(e['MU'] & de['Z'], delta_u['Z']),
    ctrl.Rule(e['MD'] & de['Z'], delta_u['Z']),
    ctrl.Rule(e['SU'] & de['Z'], delta_u['Z']),
    ctrl.Rule(e['SD'] & de['Z'], delta_u['Z']),
    ctrl.Rule(e['Z'] & de['Z'], delta_u['Z']),
    ctrl.Rule(e['MU'] & de['MD'], delta_u['Z']),
    ctrl.Rule(e['MD'] & de['MU'], delta_u['Z'])
]

# Reguły przyspieszające
rules += [
    ctrl.Rule(e['DU'] & de['MD'], delta_u['DD']),
    ctrl.Rule(e['MD'] & de['SD'], delta_u['MD']),
    ctrl.Rule(e['MU'] & de['SD'], delta_u['MU']),
    ctrl.Rule(e['SU'] & de['SD'], delta_u['MD']),
    ctrl.Rule(e['SD'] & de['MD'], delta_u['SU']),
    ctrl.Rule(e['DD'] & de['SD'], delta_u['DD']),
    ctrl.Rule(e['BDD'] & de['SD'], delta_u['BDD'])
]

# Inicjalizacja systemu i symulatora
control_system = ctrl.ControlSystem(rules)
simulator = ctrl.ControlSystemSimulation(control_system, flush_after_run=100)

def regulator_fuzzy_PD():
    e_val = -(variable.H_requested - variable.H_p)
    de_val = e_val - variable.e_prev
    variable.e_prev = e_val

    simulator.input['e'] = e_val
    simulator.input['de'] = de_val

    try:
        simulator.compute()
        # print(simulator.output['delta_u'])
        # return equations.get_equilibrium_voltage() + simulator.output['delta_u']
        return simulator.output['delta_u']
        # return equations.get_equilibrium_voltage()
    except:
        return equations.get_equilibrium_voltage()

def rescale_u(u):
    # u = np.clip(u, const.U_min_pi, const.U_max_pi)

    return const.U_min + (const.U_max - const.U_min) * (u - const.U_min_pi_fuzzy) / (const.U_max_pi_fuzzy - const.U_min_pi_fuzzy)