from const import  *
from variable import *

def calculate_new_A():
    part_1 = k_m / [ R * (R_w + L_w / T_p)]
    part_2 = U_z + (L_w / T_p) * (U_pz / R_w) - k_e * omega_s

    part_3 = (
        part_1 * part_2 - (M_pw - M_w - M_l) * G
    )

    part_4 = M_wir / 2 - (M_w + M_l + M_pw)

    return part_3 / part_4

def calculate_new_V_p():
    return  V_p + A*T_p

def calculate_new_H_p():
    return H_p + V_p * T_p + A * T_p**2 / 2

def calculate_new_omega_s():
    return omega_s + A * T_p / R

def simulation_step(new_U):
    global A, omega_s, V_p, H_p, U_pz, U_z
    U_z = new_U
    A = calculate_new_A()
    omega_s = calculate_new_omega_s()
    V_p = calculate_new_V_p()
    H_p = calculate_new_H_p()
    U_pz = U_z
    # print(f"Obliczone A: {A}")
    # print(f"Obliczone omega_s: {omega_s}")
    # print(f"Obliczone V_p: {V_p}")
    # print(f"Obliczone H_p: {H_p}")

if __name__ == "__main__":
    simulation_step(10)
    simulation_step(9)