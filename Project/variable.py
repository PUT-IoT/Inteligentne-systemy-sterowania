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
Kp = 3 # wzmocnienie regulatora 0.25 - 0.5
Ti = 80 # czas zdwojenia 2-5
Td = 1.5
e_prev = 0

#Regulator PI rozmyty
BDU = 0 # bardzo duzy ujemny
DU =  0 # duzy ujemny
SU = 0 # sredni ujemny
MU = 0 # maly ujemny
Z = 0 # okolo zera
MD = 0 # maly dodatni
SD = 0 # sredni dodatni
DD = 0 # duzy dodatni
BDD = 0 # bardzo duzy dodatni

aff = 2 # przynależność