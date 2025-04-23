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
    variable.M_l = 0
    variable.U_z = 0
    variable.U_pz = 0
    variable.omega_s = 0
    variable.V_p = 0
    variable.H_p = 0
    variable.A = 0
