import const
import equations
import variable
import regulator_PD
# import regulator_fuzzy_PI
import regulator_fuzzy_PD
steps = int(const.T_s / const.T_p)
def test_nauki(Uz, M_l, Kp, Td, BDU, DU, SU, MU, Z, MD, SD, DD, BDD, e_aff):
# def update_simulation(Uz, M_l, Kp, Td, e_aff):

    equations.reset_simulation()
    variable.H_requested = Uz
    variable.M_l = M_l

    variable.Kp = Kp
    variable.Td = Td

    variable.BDU = BDU
    variable.DU = DU
    variable.SU = SU
    variable.MU = MU
    variable.Z = Z
    variable.MD = MD
    variable.SD = SD
    variable.DD = DD
    variable.BDD = BDD
    variable.e_aff = e_aff

    height_values2 = []
    equations.reset_simulation()

    # for i in range(steps):
    #     u_regulator = regulator_fuzzy_PI.regulator_fuzzy()
    #     u = regulator_fuzzy_PI.rescale_u(u_regulator)
    #     equations.simulation_step(u)


    for i in range(steps):
        u_regulator = regulator_fuzzy_PD.regulator_fuzzy_PD()
        u = regulator_fuzzy_PD.rescale_u(u_regulator)
        # By rozkład sił był równomierny należy kręcić kołowrotkiem niezależnie od uchybu
        # Z tego powodu liczę jaki procent zajmujenapięcie potrzebne do zachowania równowagi a resztę przydzielam
        balancing_voltage = variable.get_equilibrium_voltage()
        balancing_voltage_percent = balancing_voltage / (abs(const.U_max) + abs(const.U_min))
        equations.simulation_step(balancing_voltage + u * (1 - balancing_voltage_percent))

        height_values2.append(variable.H_p)
        if i % 1000 == 0:
            print(i/1000)

    return height_values2

import random

if __name__ == '__main__':
    new_values = {
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
    # new_values = {
    #     'BDU': 0.5,
    #     'DU': 0.5,
    #     'SU': 0.435,
    #     'MU': 0.5,
    #     'Z': 0.4,
    #     'MD': 0.5,
    #     'SD': 0.5,
    #     'DD': 0.61,
    #     'BDD': 0.5
    # }

    best_values = new_values.copy()
    best_score = float('inf')

    try:
        for x in range(100000):
            # Losowa zmiana jednej wartości w new_values
            key = random.choice(list(new_values.keys()))
            # new_values[key] += random.uniform(-0.1, 0.1) * 0.1
            new_values[key] += random.choice([0.01, -0.01, 0.005, -0.005])
            print(f'Key: {key}, Value: {new_values[key]}')
            height = test_nauki(Uz=5, M_l=0, Kp=6, Td=0.25, **new_values, e_aff=2)
            current_score = sum(abs(variable.H_requested - height[-1*i-1]) for i in range(int(len(height) * 0.7)))

            if current_score < best_score:
                best_values = new_values.copy()
                best_score = current_score
                print(f'New best score: {best_score} with values: {best_values}')
            else:
                # Cofnięcie zmiany, jeśli wynik gorszy
                new_values[key] = best_values[key]
                print(f'Current best score: {best_score}, Tried values: {best_values}, with score: {current_score}')

        print(f'Final best score: {best_score} with values: {best_values}')
    except:
        print(f'Interrupted. Best score so far: {best_score} with values: {best_values}')