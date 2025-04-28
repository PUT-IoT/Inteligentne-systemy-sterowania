import variable
import const

def PID_new_current():
    # Oblicz uchyb
    e = -(variable.H_requested - variable.H_p)

    # Suma uchybów do części I
    variable.sum_e += e

    # Pochodna uchybu do części D
    de = (e - variable.e_prev) / const.T_p
    variable.e_prev = e  # zapamiętaj obecny błąd dla kolejnego kroku

    # Wyznacz sygnał PID
    uPID = variable.Kp * (e + (const.T_p / variable.Ti) * variable.sum_e + variable.Td * de)

    # Ogranicz wyjście regulatora
    u = min(const.U_max_pi, max(const.U_min_pi, uPID))

    return u

def rescale_u(u):
    # Przeskaluj napięcie regulatora do rzeczywistego zakresu Uz
    new_u = const.U_min + (const.U_max - const.U_min) * (u - const.U_min_pi) / (const.U_max_pi - const.U_min_pi)
    return new_u
