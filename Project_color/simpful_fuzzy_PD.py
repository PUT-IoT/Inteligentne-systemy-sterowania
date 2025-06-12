from simpful import *
import variable
import const
import equations

FS = FuzzySystem()

# Funkcje przynależności - uchyb (e)
FS.add_linguistic_variable("e", LinguisticVariable([
    FuzzySet(function=Triangular_MF(-5.1, -4, -3), term="BDU"),
    FuzzySet(function=Triangular_MF(-4, -3, -2), term="DU"),
    FuzzySet(function=Triangular_MF(-3, -2, -1), term="ŚU"),
    FuzzySet(function=Triangular_MF(-2, -1,  0), term="MU"),
    FuzzySet(function=Triangular_MF(-1,  0,  1), term="Z"),
    FuzzySet(function=Triangular_MF( 0,  1,  2), term="MD"),
    FuzzySet(function=Triangular_MF( 1,  2,  3), term="ŚD"),
    FuzzySet(function=Triangular_MF( 2,  3,  4), term="DD"),
    FuzzySet(function=Triangular_MF( 3,  4,  5.1), term="BDD"),
], universe_of_discourse=[-5.1, 5.1]))

# Funkcje przynależności - pochodna uchybu (de)
FS.add_linguistic_variable("de", LinguisticVariable([
    FuzzySet(function=Triangular_MF(-1.2, -1, -0.8), term="BDU"),
    FuzzySet(function=Triangular_MF(-1, -0.75, -0.5), term="DU"),
    FuzzySet(function=Triangular_MF(-0.75, -0.5, -0.25), term="ŚU"),
    FuzzySet(function=Triangular_MF(-0.5, -0.25, 0), term="MU"),
    FuzzySet(function=Triangular_MF(-0.1, 0, 0.1), term="Z"),
    FuzzySet(function=Triangular_MF(0, 0.25, 0.5), term="MD"),
    FuzzySet(function=Triangular_MF(0.25, 0.5, 0.75), term="ŚD"),
    FuzzySet(function=Triangular_MF(0.5, 0.75, 1), term="DD"),
    FuzzySet(function=Triangular_MF(0.8, 1, 1.2), term="BDD"),
], universe_of_discourse=[-1.1, 1.1]))

# Funkcje przynależności - napięcie wyjściowe
FS.add_linguistic_variable("u", LinguisticVariable([
    FuzzySet(function=Triangular_MF(-120, -100, -80), term="BDU"),
    FuzzySet(function=Triangular_MF(-100, -80, -60), term="DU"),
    FuzzySet(function=Triangular_MF(-80, -60, -40), term="ŚU"),
    FuzzySet(function=Triangular_MF(-40, -20, 0), term="MU"),
    FuzzySet(function=Triangular_MF(-10, 0, 10), term="Z"),
    FuzzySet(function=Triangular_MF(0, 20, 40), term="MD"),
    FuzzySet(function=Triangular_MF(40, 60, 80), term="ŚD"),
    FuzzySet(function=Triangular_MF(60, 80, 100), term="DD"),
    FuzzySet(function=Triangular_MF(80, 100, 120), term="BDD"),
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
        return delta_u + u_eq
    except Exception as ex:
        print(f"[Fuzzy] Błąd podczas inferencji: {ex}")
        return equations.get_equilibrium_voltage3(variable.M_l)

# Nie jest obecnie wykorzystywana, ale zostawiona dla kompatybilności z main.py
def rescale_u(u):
    return const.U_min + (const.U_max - const.U_min) * (u - const.U_min_pi_fuzzy) / (const.U_max_pi_fuzzy - const.U_min_pi_fuzzy)
