import variable
import const
def PI_new_current():
    e = variable.H_requested - variable.H_p
    variable.sum_e += e

    uPI = variable.Kp * (e + (const.T_p / variable.Ti) * variable.sum_e)
    u = min(const.U_max_pi, max(const.U_min_pi, uPI))
    return u

def rescale_u(u):
    new_u = const.U_min + (const.U_max - const.U_min) * (u - const.U_min_pi) / (const.U_max_pi - const.U_min_pi)
    return new_u