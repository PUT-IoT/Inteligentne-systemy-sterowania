import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

from const import *
from equations import *
from variable import *

ts = 20  # czas symulacji (s)
steps = int(ts / T_p)

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
def update_simulation(uz):
    global U_z
    U_z = uz
    omega_values = []
    acc_values = []
    height_values = []
    time = []

    for i in range(steps):
        # uruchomienie jednego kroku w symulacji
        simulation_step(U_z)

        # zapisywanie danych
        time.append(i * T_p)
        omega_values.append(omega_s)
        acc_values.append(A)
        height_values.append(H_p)

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