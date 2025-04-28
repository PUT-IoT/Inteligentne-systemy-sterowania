import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

import const
import equations
import variable
import regulator_PID

steps = int(const.T_s / const.T_p)

# apka Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Symulacja silnika – sterowanie napięciem"),

    html.Div(id='current-values'),

    html.Label("Wysokość zadana H (m):"),
    dcc.Slider(
        id='uz-slider',
        min=0,
        max=40,
        step=1,
        value=0,
        marks={i: str(i) for i in range(-40, 41, 5)}
    ),

    html.Label("Kp (wzmocnienie):"),
    dcc.Slider(
        id='kp-slider',
        min=0,
        max=10,
        step=0.1,
        value=6,
        marks={i: str(i) for i in range(0, 11)}
    ),

    html.Label("Ti (czas zdwojenia):"),
    dcc.Slider(
        id='ti-slider',
        min=1,
        max=100,
        step=1,
        value=14,
        marks={i: str(i) for i in range(0, 101, 10)}
    ),

    html.Label("Td (czas różniczkowania):"),
    dcc.Slider(
        id='td-slider',
        min=0,
        max=10,
        step=0.1,
        value=5,
        marks={i: str(i) for i in range(0, 11)}
    ),

    html.Label("Liczba osób w windzie (1 osoba = 70kg):"),
    dcc.Slider(
        id='people-slider',
        min=0,
        max=20,
        step=1,
        value=0,
        marks={i: str(i) for i in range(0, 21)}
    ),

    html.Label("Ciężar pustej windy (kg):"),
    dcc.Slider(
        id='empty-weight-slider',
        min=100,
        max=1000,
        step=10,
        value=500,
        marks={i: str(i) for i in range(100, 1001, 100)}
    ),

    dcc.Graph(id='height-plot'),
    dcc.Graph(id='omega-plot'),
    dcc.Graph(id='acc-plot'),
    dcc.Graph(id='current-plot')
])

@app.callback(
    [Output('omega-plot', 'figure'),
     Output('acc-plot', 'figure'),
     Output('height-plot', 'figure'),
     Output('current-plot', 'figure'),
     Output('current-values', 'children')],
    [Input('uz-slider', 'value'),
     Input('kp-slider', 'value'),
     Input('ti-slider', 'value'),
     Input('td-slider', 'value'),
     Input('people-slider', 'value'),
     Input('empty-weight-slider', 'value')]
)
def update_simulation(Uz, kp, ti, td, people, empty_weight):

    omega_values = []
    acc_values = []
    height_values = []
    time = []
    current_values = []

    equations.reset_simulation()

    variable.H_requested = Uz
    variable.Kp = kp
    variable.Ti = ti
    variable.Td = td
    const.M_w = empty_weight
    variable.M_l = people * 70

    for i in range(steps):
        u_regulator = regulator_PID.PID_new_current()
        u = regulator_PID.rescale_u(u_regulator)
        equations.simulation_step(u)

        time.append(i * const.T_p)
        omega_values.append(variable.omega_s)
        acc_values.append(variable.A)
        height_values.append(variable.H_p)
        current_values.append(variable.U_z)

    omega_fig = go.Figure()
    omega_fig.add_trace(go.Scatter(x=time, y=omega_values, name='Omega (rad/s)'))
    omega_fig.update_layout(title='Prędkość kątowa w czasie', xaxis_title='Czas (s)', yaxis_title='Omega (rad/s)')

    acc_fig = go.Figure()
    acc_fig.add_trace(go.Scatter(x=time, y=acc_values, mode='lines', name='Przyspieszenie (m/s²)'))
    acc_fig.update_layout(title='Przyspieszenie w czasie', xaxis_title='Czas (s)', yaxis_title='A (rad/s²)')

    height_fig = go.Figure()
    height_fig.add_trace(go.Scatter(x=time, y=height_values, mode='lines', name='Wysokość (m)'))
    height_fig.update_layout(title='Wysokość w czasie', xaxis_title='Czas (s)', yaxis_title='H (m)')

    current_fig = go.Figure()
    current_fig.add_trace(go.Scatter(x=time, y=current_values, mode='lines', name='Napiecie (V)'))
    current_fig.update_layout(title='Napięcie w czasie', xaxis_title='Czas (s)', yaxis_title='Napiecie (V)')

    equations.is_simulation_realistic()

    current_vals_text = html.Div([
        html.H3(f"Aktualne parametry:"),
        html.P(f"Wysokość zadana: {Uz} m"),
        html.P(f"Kp: {kp}"),
        html.P(f"Ti: {ti}"),
        html.P(f"Td: {td}"),
        html.P(f"Liczba osób: {people}"),
        html.P(f"Ciężar pustej windy: {empty_weight} kg")
    ])

    return omega_fig, acc_fig, height_fig, current_fig, current_vals_text

if __name__ == '__main__':
    app.run(debug=True)
