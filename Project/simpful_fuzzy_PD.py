from simpful import *
import variable
import const
import equations

FS = FuzzySystem()

# Funkcje przynależności - uchyb (e)
FS.add_linguistic_variable("e", LinguisticVariable([
    FuzzySet(function=Triangular_MF(-10, -9, -8), term="BDU"),
    FuzzySet(function=Triangular_MF(-9, -8, -7), term="DU"),
    FuzzySet(function=Triangular_MF(-6, -4, -2), term="ŚU"),
    FuzzySet(function=Triangular_MF(-4, -2,  0), term="MU"),
    FuzzySet(function=Triangular_MF(-2,  0,  2), term="Z"),
    FuzzySet(function=Triangular_MF( 0,  2,  4), term="MD"),
    FuzzySet(function=Triangular_MF( 2,  4,  6), term="ŚD"),
    FuzzySet(function=Triangular_MF( 7,  8,  9), term="DD"),
    FuzzySet(function=Triangular_MF( 8,  9, 10), term="BDD"),
], universe_of_discourse=[-10, 10]))

# Funkcje przynależności - pochodna uchybu (de)
FS.add_linguistic_variable("de", LinguisticVariable([
    FuzzySet(function=Triangular_MF(-0.3, -0.25, -0.2), term="BDU"),
    FuzzySet(function=Triangular_MF(-0.25, -0.1875, -0.125), term="DU"),
    FuzzySet(function=Triangular_MF(-0.1875, -0.125, -0.0625), term="ŚU"),
    FuzzySet(function=Triangular_MF(-0.125, -0.0625, 0), term="MU"),
    FuzzySet(function=Triangular_MF(-0.025, 0, 0.025), term="Z"),
    FuzzySet(function=Triangular_MF(0, 0.0625, 0.125), term="MD"),
    FuzzySet(function=Triangular_MF(0.0625, 0.125, 0.1875), term="ŚD"),
    FuzzySet(function=Triangular_MF(0.125, 0.1875, 0.25), term="DD"),
    FuzzySet(function=Triangular_MF(0.2, 0.25, 0.3), term="BDD"),
], universe_of_discourse=[-0.275, 0.275]))




# Funkcje przynależności - napięcie wyjściowe
FS.add_linguistic_variable("u", LinguisticVariable([
    FuzzySet(function=Triangular_MF(-120, -110, -100), term="BDU"),
    FuzzySet(function=Triangular_MF(-100, -80, -60), term="DU"),
    FuzzySet(function=Triangular_MF(-80, -70, -50), term="ŚU"),
    FuzzySet(function=Triangular_MF(-50, -40, 5), term="MU"),
    FuzzySet(function=Triangular_MF(-5, 0, 5), term="Z"),
    FuzzySet(function=Triangular_MF(5, 40, 50), term="MD"),
    FuzzySet(function=Triangular_MF(50, 70, 80), term="ŚD"),
    FuzzySet(function=Triangular_MF(60, 80, 100), term="DD"),
    FuzzySet(function=Triangular_MF(100, 110, 120), term="BDD"),
], universe_of_discourse=[-120, 120]))

# Tabela reguł z przesłanego obrazka
tabela_regul = [
    ["BDU", "BDU", "BDU", "DU",  "ŚU",  "MU", "Z"],
    ["BDU", "BDU", "DU",  "ŚU",  "MU",  "Z",  "MD"],
    ["BDU", "DU",  "ŚU",  "MU",  "Z",   "MD", "ŚD"],
    ["DU",  "ŚU",  "MU",  "Z",   "MD",  "ŚD", "DD"],
    ["ŚU",  "MU",  "Z",   "MD",  "ŚD",  "DD", "BDD"],
    ["MU",  "Z",   "MD",  "ŚD",  "DD",  "BDD", "BDD"],
    ["Z",   "MD",  "ŚD",  "DD",  "BDD", "BDD", "BDD"]
]

etykiety = ["DU", "ŚU", "MU", "Z", "MD", "ŚD", "DD"]

# Dodawanie reguł
for i, e_term in enumerate(etykiety):
    for j, de_term in enumerate(etykiety):
        u_term = tabela_regul[i][j]
        FS.add_rules([f"IF (e IS {e_term}) AND (de IS {de_term}) THEN (u IS {u_term})"])

# Reguły brzegowe
FS.add_rules([
    "IF (e IS BDU) AND (de IS BDU) THEN (u IS BDU)",
    "IF (e IS BDD) AND (de IS BDD) THEN (u IS BDD)",
    "IF (e IS BDU) AND (de IS ŚU) THEN (u IS BDU)",
    "IF (e IS ŚU) AND (de IS BDU) THEN (u IS BDU)",
    "IF (e IS BDD) AND (de IS ŚD) THEN (u IS BDD)",
    "IF (e IS ŚD) AND (de IS BDD) THEN (u IS BDD)"
])

# --- reguły dla skrajnych wartości ------------------------------------------
EXTREME = ["BDU", "BDD"]
ALL     = ["BDU","DU","ŚU","MU","Z","MD","ŚD","DD","BDD"]

for e_term in EXTREME:
    for de_term in ALL:
        FS.add_rules([f"IF (e IS {e_term}) AND (de IS {de_term}) THEN (u IS {e_term})"])

for de_term in EXTREME:
    for e_term in ALL:
        FS.add_rules([f"IF (e IS {e_term}) AND (de IS {de_term}) THEN (u IS {de_term})"])

# Regulator rozmyty PD z uwzględnieniem napięcia równowagi
def regulator_fuzzy_PD():
    e_val = -(variable.H_requested - variable.H_p)
    de_val = e_val - variable.e_prev
    variable.e_prev = e_val

    # ograniczenie na wejścia
    e_val = max(-5, min(5, e_val))
    de_val = max(-1, min(1, de_val))

    FS.set_variable("e", e_val)
    FS.set_variable("de", de_val)

    try:
        result = FS.inference()
        delta_u = result.get("u", 0)
        u_eq = equations.get_equilibrium_voltage3(variable.M_l)
        # u_eq =0
        u = min(const.U_max, max(const.U_min, delta_u + u_eq))
        return u
    except Exception as ex:
        print(f"[Fuzzy] Błąd podczas inferencji: {ex}")
        return equations.get_equilibrium_voltage3(variable.M_l)

# Nie jest obecnie wykorzystywana, ale zostawiona dla kompatybilności z main.py
def rescale_u(u):
    return const.U_min + (const.U_max - const.U_min) * (u - const.U_min_pi_fuzzy) / (const.U_max_pi_fuzzy - const.U_min_pi_fuzzy)
