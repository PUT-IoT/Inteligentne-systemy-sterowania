import numpy as np
import matplotlib.pyplot as plt
import equations
import variable
import regulator_PID as regulator_PID
import const

# Zakres testowanych wartosci PID
Kp_values = np.linspace(0.5, 5, 6)    # np. 0.5, 1, 1.5, ..., 5
Ti_values = np.linspace(10, 100, 10)  # np. 10, 20, ..., 100
Td_values = np.linspace(0.01, 2, 5)   # np. 0.01, 0.5, 1, 1.5, 2

steps = int(const.T_s / const.T_p)    # Liczba kroków symulacji

# Wyniki
results = []

# Wysokosc zadana do testowania
H_target = 0  # metrow

# Funkcja symulacji dla danych Kp, Ti, Td
def simulate_system(Kp, Ti, Td, H_target):
    # Ustaw parametry regulatora
    variable.Kp = Kp
    variable.Ti = Ti
    variable.Td = Td

    # Reset symulacji
    equations.reset_simulation()
    variable.H_requested = H_target

    total_error = 0

    for _ in range(steps):
        u_regulator = regulator_PID.PID_new_current()
        u = regulator_PID.rescale_u(u_regulator)
        equations.simulation_step(u)

        # Liczenie calkowitego uchybu
        error = abs(variable.H_requested - variable.H_p)
        total_error += error

    return total_error

# Główna petla testująca
for kp in Kp_values:
    for ti in Ti_values:
        for td in Td_values:
            error = simulate_system(kp, ti, td, H_target)
            results.append((kp, ti, td, error))

# Wybór najlepszego zestawu
best = min(results, key=lambda x: x[3])

print("\n=== Najlepsze znalezione parametry PID ===")
print(f"Kp = {best[0]:.2f}, Ti = {best[1]:.2f}, Td = {best[2]:.2f}, Calkowity blad = {best[3]:.2f}")

# Wykres 3D wyników
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

kp_list, ti_list, td_list, error_list = zip(*results)

sc = ax.scatter(kp_list, ti_list, td_list, c=error_list, cmap='viridis')
ax.set_xlabel('Kp')
ax.set_ylabel('Ti')
ax.set_zlabel('Td')
fig.colorbar(sc, label='Total Error')
ax.set_title('Wyniki strojenia PID')

plt.show()
