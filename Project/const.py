R = 0.2 # promień kołowrotka (m)
M_w = 500 # masa pustej windy (tara masy windy) (kg)
M_pw = 600 # masa przeciwwagi (kg)
G = 9.81 # przyspieszenie ziemskie (m/s^2)
M_wir = 20 # masa wirnika (kg)
R_w = 5 # rezystancja zastępcza uzwojeń wirnika (Ω)
L_w = 10 # indukcyjność zastępcza uzwojeń wirnika (H)
k_e = 5 # stała elektryczna, zależna m.in. od strumienia magnetycznego stojana oraz liczby zwojów w uzwojeniach wirnika
k_m = 10 # stała mechaniczna, zależna m.in. od strumienia magnetycznego stojana oraz liczby zwojów w uzwojeń wirnika
T_p = 0.01 # czas próbkowania (s)
T_s = 600  # czas symulacji (s)

U_max = 120 # maksymalne napiecie dostarczane do silnika
U_min = -120 # minimalne napiecie dostarczane do silnika

# Regulator PI
U_min_pi = -10 # maksymalne napiecie z regulatora
U_max_pi = 10 # minimalne napiecie z regulatora