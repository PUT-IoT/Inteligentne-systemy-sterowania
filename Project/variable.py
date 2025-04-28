M_l = 0 # masa ludzi i towaru w windzie (masa netto windy)
U_z = 0 # napięcie zasilające wirnik
U_pz = 0 # napięcie poprzednie zasilające wirnik
omega_s = 0 # prędkość kątowa wirnika
V_p = 0 # prędkość poprzednia windy
H_p = 0 # wysokość poprzednia windy (czas próbkowania temu)
A = 0 # przyspieszenie układu

H_requested = 0 # wysokość zadana

#Regulator PI
sum_e = 0 # suma uchybów
e_prev = 0  # poprzedni uchyb
Kp = 2 # wzmocnienie regulatora
Ti = 16 # czas zdwojenia
Td = 2   # czas różniczkowania