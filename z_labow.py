import math
import plotly.express as px
import pandas as pd

A = 1.5
beta = 0.035
tp = 0.1
ts = 1800
h0 = 0.0
qd = 0.05
hn = [h0]
qd_history = []

#Ograniczenia
qd_min = 0.0
qd_max = 0.05
u_min = 0.0
u_max = 10.0
# u =10

h_sp = 1.5      # poziom zadany
Kp = 0.25       # wzmocnienie
Ti = 2.7      # czas całkowania
sum_e = 0.0


#Algorytm pozycyjny
for i in range(0, ts*10):
    h_current = hn[-1]

    e = h_sp - h_current
    sum_e += e

    uPI = Kp * (e + (tp / Ti) * sum_e)
    u = min(u_max, max(u_min, uPI))

    qd = qd_min + (qd_max - qd_min) * (u - u_min) / (u_max - u_min)
    qd_history.append(qd)


    x = tp / A * (qd - beta * math.sqrt(h_current)) + h_current
    hn.append(x)





# print(hn)

y = [i/36000 for i in range(-1, ts*10)]

df = pd.DataFrame({'x': hn})

# df = px.data.gapminder().query("country=='Canada'")
fig = px.line(df, x=y, y=hn,
              labels={'x': 'Czas (h)', 'y': 'Wysokość (m)'})

fig.show()

qd_history.append(qd)
df2 = pd.DataFrame({'x': qd_history})

fig2 = px.line(df2, x=y, y=qd_history,
              labels={'x': 'Czas (h)', 'y': 'q (m)'})
fig2.show()