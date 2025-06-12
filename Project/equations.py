import const
import variable

def calculate_new_A():
    part_1 = const.k_m / (const.R * (const.R_w + const.L_w / const.T_p))
    part_2 = variable.U_z + (const.L_w / const.T_p) * (variable.U_pz / const.R_w) - const.k_e * variable.omega_s

    part_3 = (
        part_1 * part_2 - (const.M_pw - const.M_w - variable.M_l) * const.G
    )

    part_4 = const.M_wir / 2 - (const.M_w + variable.M_l + const.M_pw)
    return part_3 / part_4

def calculate_new_V_p():
    return variable.V_p + variable.A * const.T_p

def calculate_new_H_p():
    return variable.H_p + variable.V_p * const.T_p + variable.A * const.T_p**2 / 2

def calculate_new_omega_s():
    return variable.omega_s + variable.A * const.T_p / const.R

def simulation_step(new_U):
    variable.U_z = new_U
    variable.A = calculate_new_A()
    variable.omega_s = calculate_new_omega_s()
    variable.V_p = calculate_new_V_p()
    variable.H_p = calculate_new_H_p()
    variable.U_pz = variable.U_z

def reset_simulation():
    # variable.M_l = 0
    variable.U_z = 0
    variable.U_pz = 0
    variable.omega_s = 0
    variable.V_p = 0
    variable.H_p = 0
    variable.A = 0

    # variable.H_requested = 0
    variable.sum_e = 0
    # variable.Kp = 0
    # variable.Ti = 0
    # variable.Td = 0
# https://www.gmv.pl/wytyczne-elektryczne.html
def is_simulation_realistic():
    ok = True
    curr_power = variable.U_z/const.R_w * variable.U_z
    if curr_power > 2200:
        ok = False
        print(f"Prob. too high power (overheat) - {curr_power}")
    intensity = variable.U_z / const.R_w
    if variable.U_z/const.R_w > 65:
        ok = False
        print(f"Too high intensity -> Too high power voltage or too low resistance - {intensity}")
    return ok


def get_equilibrium_voltage():
    """
    Wyznacza napięcie równowagi statycznej dla danej masy ludzi w windzie,
    zakładając, że prędkość i przyspieszenie = 0 (stan ustalony).
    """
    total_mass = const.M_w + variable.M_l
    opposing_mass = const.M_pw
    g = const.G

    numerator = (opposing_mass - total_mass) * g
    # denominator = const.k_m / (const.R * (const.R_w + (const.L_w / const.T_p))) * \
    #               (1 + (const.L_w / (const.T_p * const.R_w)))
    denominator = 1/const.R * (const.k_m / (const.R * (const.R_w + (const.L_w / const.T_p))))

    U_eq = numerator / denominator
    return max(const.U_min, min(U_eq, const.U_max))  # ograniczenie do bezpiecznego zakresu

def get_equilibrium_voltage2():
    part_1 = const.k_m / (const.R * (const.R_w + const.L_w / const.T_p))
    # part_2 = variable.U_z + (const.L_w / const.T_p) * (variable.U_pz / const.R_w) - const.k_e * variable.omega_s
    part_2 =  1 + (const.L_w / const.T_p) * (1 / const.R_w)

    part_3 = (
        variable.U_z * part_1 * part_2 - (const.M_pw - const.M_w - variable.M_l) * const.G
    )

    part_4 = const.M_wir / 2 - (const.M_w + variable.M_l + const.M_pw)
    # a = part_3 / part_4
    # variable.U_z
    return (const.M_pw - const.M_w - variable.M_l) * const.G/part_1 * part_2


def get_equilibrium_voltage3(M_l):
    """
    Oblicza wymagane napięcie wejściowe (U_in), aby przyspieszenie układu wynosiło 0,
    zakładając, że omega_s = 0 i U_z = U_pz.
    """
    # Skróty pomocnicze dla czytelności
    numerator = (const.M_pw - const.M_w - M_l) * const.G * const.R * (const.R_w + const.L_w / const.T_p)
    denominator = const.k_m * (1 + (const.L_w / (const.T_p * const.R_w)))

    return numerator / denominator