import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

import const
import equations
import variable
import regulator_PI

steps = int(const.T_s / const.T_p)

# apka Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Symulacja silnika – sterowanie napięciem"),

    html.Label("Wysokość zadana H (m):"),
    dcc.Slider(
        id='uz-slider',
        min=0,
        max=40,
        step=1,
        value=5,
        marks={i: str(i) for i in range(0, 41, 1)}
    ),
    html.Label("Masa ludzi - tara windy (kg):"),
    dcc.Slider(
        id='ml-slider',
        min=0,
        max=200,
        step=10,
        value=0,
        marks={i: str(i) for i in range(0, 201, 10)}
    ),
    html.Label("Wzmocnienie regulatora - Kp:"),
    dcc.Slider(
        id='kp-slider',
        min=0,
        max=40,
        step=0.25,
        value=2,
        marks={i: str(i) for i in range(0, 41, 1)}
    ),
    html.Label("Czas zdwojenia - Ti:"),
    dcc.Slider(
        id='ti-slider',
        min=0,
        max=100,
        step=5,
        value=80,
        marks={i: str(i) for i in range(0, 101, 5)}
    ),
    html.Label("Czas rozniczkowania - Td (0 dla regulatora PI):"),
    dcc.Slider(
        id='td-slider',
        min=0,
        max=40,
        step=1,
        value=2,
        marks={i: str(i) for i in range(0, 41, 1)}
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
     Output('current-plot', 'figure')],
    [Input('uz-slider', 'value'),
     Input('kp-slider', 'value'),
     Input('ti-slider', 'value'),
     Input('td-slider', 'value'),
     Input('ml-slider', 'value'),]
)
def update_simulation(Uz, Kp, Ti, Td, M_l):

    omega_values = []
    acc_values = []
    height_values = []
    time = []
    current_values = []
    equations.reset_simulation()
    if variable.H_requested != Uz:
        variable.H_requested = Uz
    if variable.Kp != Kp:
        variable.Kp = Kp
    if variable.Ti != Ti:
        variable.Ti = Ti
    if variable.Td != Td:
        variable.Td = Td
    if variable.M_l != M_l:
        variable.M_l = M_l

    for i in range(steps):
        u_regulator = regulator_PI.PI_new_current()
        u = regulator_PI.rescale_u(u_regulator)
        equations.simulation_step(u)

        time.append(i * const.T_p)
        omega_values.append(variable.omega_s)
        acc_values.append(variable.A)
        height_values.append(variable.H_p)
        current_values.append(variable.U_z)

    # Tworzenie wykresów
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
    return omega_fig, acc_fig, height_fig, current_fig

if __name__ == '__main__':
    app.run(debug=True)
