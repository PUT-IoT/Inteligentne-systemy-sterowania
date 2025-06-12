import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

import const
import equations
import variable
import regulator_PD
import regulator_fuzzy_PD

steps = int(const.T_s / const.T_p)

# Aplikacja Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Symulacja silnika – sterowanie napięciem"),

    html.Div([
        # Lewa kolumna - suwaki
        html.Div([
            html.H2("Zmienne w układzie:"),
            html.Label("Wysokość zadana H [m]:"),
            dcc.Slider(
                id='uz-slider',
                min=0,
                max=20,
                step=1,
                value=10,
                marks={i: str(i) for i in range(0, 21, 1)},
                className='pastel-slider'
            ),
            html.Label("Masa ludzi - netto windy [kg]:"),
            dcc.Slider(
                id='ml-slider',
                min=0,
                max=200,
                step=1,
                value=100,
                marks={i: str(i) for i in range(0, 201, 10)},
                className='pastel-slider'
            ),

            html.H2("Parametry regulatora klasycznego:"),
            html.Label("Wzmocnienie regulatora - Kp:"),
            dcc.Slider(
                id='kp-slider',
                min=0,
                max=5,
                step=0.1,
                value=2,
                marks={i: str(i) for i in [0] + [round(x * 0.5, 2) for x in range(1, 10)] + [5]},
                className='pastel-slider'
            ),
            html.Label("Czas zdwojenia - Ti:"),
            dcc.Slider(
                id='ti-slider',
                min=0,
                max=1,
                step=0.01,
                value=0,
                marks={int(i) if i.is_integer() else i: str(int(i)) if i.is_integer() else str(i)
                       for i in [round(x * 0.2, 2) for x in range(0, 51)]},
                className='pastel-slider'
            ),
            html.Label("Czas różniczkowania - Td:"),
            dcc.Slider(
                id='td-slider',
                min=0,
                max=5,
                step=0.05,
                value=3.5,
                marks={i: str(i) for i in [0] + [round(x * 0.5, 2) for x in range(1, 10)] + [5]},
                className='pastel-slider'
            ),
        ], style={'width': '30%', 'padding': '10px'}),

        # Prawa kolumna - wykresy
        html.Div([
            html.H2("Wykresy:"),
            dcc.Graph(id='height-plot'),
            dcc.Graph(id='omega-plot'),
            dcc.Graph(id='acc-plot'),
            dcc.Graph(id='combined-voltage-plot'),
        ], className="graph-panel", style={'width': '70%', 'padding': '10px'}),
    ], style={'display': 'flex', 'flexDirection': 'row'})
])


@app.callback(
    [
        Output('omega-plot', 'figure'),
        Output('acc-plot', 'figure'),
        Output('height-plot', 'figure'),
        Output('combined-voltage-plot', 'figure'),
    ],
    [
        Input('uz-slider', 'value'),
        Input('ml-slider', 'value'),
        Input('kp-slider', 'value'),
        Input('ti-slider', 'value'),
        Input('td-slider', 'value'),
    ]
)
def update_simulation(Uz, M_l, Kp, Ti, Td):

    omega_values = []
    acc_values = []
    height_values = []
    time = []
    current_values = []
    requested_h_p = []
    balance_voltage = []

    equations.reset_simulation()
    variable.H_requested = Uz
    variable.M_l = M_l
    variable.Kp = Kp
    variable.Ti = Ti
    variable.Td = Td

    for i in range(steps):
        u_regulator = regulator_PD.PD_new_current()
        u = regulator_PD.rescale_u(u_regulator)
        equations.simulation_step(u)

        time.append(i * const.T_p)
        omega_values.append(variable.omega_s)
        acc_values.append(variable.A)
        height_values.append(variable.H_p)
        current_values.append(variable.U_z)
        requested_h_p.append(variable.H_requested)

    fuzzy = []
    height_values2 = []
    equations.reset_simulation()

    for i in range(steps):
        u_regulator = regulator_fuzzy_PD.regulator_fuzzy_PD()
        balancing_voltage = current_values[-1]
        balance_voltage.append(balancing_voltage)

        equations.simulation_step(u_regulator)

        fuzzy.append(u_regulator)
        height_values2.append(variable.H_p)

    # Wykres prędkości kątowej
    omega_fig = go.Figure()
    omega_fig.add_trace(go.Scatter(x=time, y=omega_values, name='Omega [rad/s]', line=dict(color='#66bb6a')))
    omega_fig.update_layout(title='Prędkość kątowa w czasie', xaxis_title='Czas [s]', yaxis_title='Omega [rad/s]')

    # Wykres przyspieszenia
    acc_fig = go.Figure()
    acc_fig.add_trace(go.Scatter(x=time, y=acc_values, mode='lines', name='Przyspieszenie [m/s²]', line=dict(color='#66bb6a')))
    acc_fig.update_layout(title='Przyspieszenie w czasie', xaxis_title='Czas [s]', yaxis_title='A [rad/s²]')

    # Wykres wysokości - klasyczny i rozmyty
    height_fig = go.Figure()
    height_fig.add_trace(go.Scatter(x=time, y=height_values, mode='lines', name='Wysokość klasyczny [m]', line=dict(color='#66bb6a')))  # zielony
    height_fig.add_trace(go.Scatter(x=time, y=height_values2, mode='lines', name='Wysokość fuzzy [m]', line=dict(color='#ab47bc')))  # fioletowy
    height_fig.add_trace(go.Scatter(x=time, y=requested_h_p, mode='lines', name='Wysokość zadana [m]', line=dict(color='#ff8ecb', dash='dash')))
    height_fig.update_layout(title='Wysokość w czasie - porównanie klasyczny vs rozmyty',
                             xaxis_title='Czas [s]', yaxis_title='H [m]')

    # Wspólny wykres napięcia
    combined_voltage_fig = go.Figure()
    combined_voltage_fig.add_trace(go.Scatter(x=time, y=current_values, mode='lines', name='Napięcie klasyczne [V]', line=dict(color='#66bb6a')))
    combined_voltage_fig.add_trace(go.Scatter(x=time, y=fuzzy, mode='lines', name='Napięcie fuzzy [V]', line=dict(color='#ab47bc')))
    combined_voltage_fig.add_trace(go.Scatter(x=time, y=balance_voltage, mode='lines', name='Napięcie równowagi [V]', line=dict(color='#ff8ecb', dash='dash')))
    combined_voltage_fig.update_layout(title='Napięcie w czasie – klasyczny vs fuzzy',
                                       xaxis_title='Czas [s]', yaxis_title='Napięcie [V]')

    equations.is_simulation_realistic()

    return omega_fig, acc_fig, height_fig, combined_voltage_fig


if __name__ == '__main__':
    app.run(debug=True)
