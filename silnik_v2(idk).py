import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# parametry silnika - losowe
kw = 0.1
Rw = 0.5
Lw = 0.01
ke = 0.01
B = 0.01
Mobc = 0.2
Mpw = 1.0
Mw = 0.5
Ml = 0.3
G = 9.81
R = 0.05
Mwir = 2.0
Vp = [0.0]

Tp = 0.1  # krok czasowy
ts = 20  # czas symulacji (s)
steps = int(ts / Tp)

# apka Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Symulacja silnika – sterowanie napięciem (?)"),

    html.Label("Napięcie Uz (V):"),
    dcc.Slider(
        id='uz-slider',
        min=0,
        max=10,
        step=0.1,
        value=5,
        marks={i: str(i) for i in range(0, 11)}
    ),

    dcc.Graph(id='omega-plot'),
    dcc.Graph(id='acc-plot')
])

@app.callback(
    [Output('omega-plot', 'figure'),
     Output('acc-plot', 'figure')],
    [Input('uz-slider', 'value')]
)
def update_simulation(Uz):
    omega_s = 0.0  # poczatkowa predkosc katowa
    Hp = 0.0       # wysokosc poczatkowa
    V0 = 0.0       # poczatkowa predkosc liniowa
    Upz = 0.0

    omega_values = []
    acc_values = []
    height_values = []
    time = []

    for i in range(steps):
        # obliczanie przyspieszenia
        A = (((kw / (Rw + (Lw / Tp))) * (Uz + (Lw / Tp) * (Upz / Rw) - ke * omega_s)
              - B * omega_s - Mobc) / R - (Mpw - Mw - Ml) * G) / ((Mwir / 2) + (Mw + Ml + Mpw))

        # uaktualnianie v i h
        omega_s += A * Tp #predkosc katowa wirnika
        V0 = Vp[-1] + A * Tp
        Hp += V0 * Tp + (A * Tp ** 2)/2

        # zapisywanie danychs
        time.append(i * Tp)
        omega_values.append(omega_s)
        acc_values.append(A)
        height_values.append(Hp)

    # Tworzenie wykresów
    omega_fig = go.Figure()
    omega_fig.add_trace(go.Scatter(x=time, y=omega_values, name='Omega (rad/s)'))
    omega_fig.update_layout(title='Prędkość kątowa w czasie', xaxis_title='Czas (s)', yaxis_title='Omega (rad/s)')

    acc_fig = go.Figure()
    acc_fig.add_trace(go.Scatter(x=time, y=acc_values, mode='lines', name='Przyspieszenie (rad/s²)'))
    acc_fig.update_layout(title='Przyspieszenie w czasie', xaxis_title='Czas (s)', yaxis_title='A (rad/s²)')

    return omega_fig, acc_fig

if __name__ == '__main__':
    app.run(debug=True)
