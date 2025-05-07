import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

import const
import equations
import variable
import regulator_PD
import regulator_fuzzy_PI
steps = int(const.T_s / const.T_p)

# apka Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Symulacja silnika – sterowanie napięciem"),
    html.H2("Zmienne w układzie:"),
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

    html.H2("Parametry regulatora klasycznego:"),
    html.Label("Wzmocnienie regulatora - Kp:"),
    dcc.Slider(
        id='kp-slider',
        min=0,
        max=40,
        step=0.25,
        value=6,
        marks={i: str(i) for i in range(0, 41, 1)}
    ),
    html.Label("Czas rozniczkowania - Td (0 dla regulatora PD):"),
    dcc.Slider(
        id='td-slider',
        min=0,
        max=5,
        step=0.1,
        value=0.25,
        marks={i: str(i) for i in range(0, 41, 1)}
    ),

    html.H2("Parametry regulatora rozmytego PD:"),
    html.Label("Regulator PI rozmyty - wartość bardzo duzy ujemny:"),
    dcc.Slider(
        id='bdu-slider',
        min=0,
        max=1,
        step=0.01,
        value=0,
        marks={i: str(i) for i in [x / 10 for x in range(11)]}
    ),
    html.Label("Regulator PI rozmyty - wartość duzy ujemny:"),
    dcc.Slider(
        id='du-slider',
        min=0,
        max=1,
        step=0.01,
        value=0.1,
        marks={i: str(i) for i in [x / 10 for x in range(11)]}
    ),
    html.Label("Regulator PI rozmyty - wartość średni ujemny:"),
    dcc.Slider(
        id='su-slider',
        min=0,
        max=1,
        step=0.01,
        value=0.3,
        marks={i: str(i) for i in [x / 10 for x in range(11)]}
    ),
    html.Label("Regulator PI rozmyty - wartość mały ujemny:"),
    dcc.Slider(
        id='mu-slider',
        min=0,
        max=1,
        step=0.01,
        value=0.45,
        marks={i: str(i) for i in [x / 10 for x in range(11)]}
    ),
    html.Label("Regulator PI rozmyty - wartość około zera:"),
    dcc.Slider(
        id='z-slider',
        min=0,
        max=1,
        step=0.01,
        value=0.5,
        marks={i: str(i) for i in [x / 10 for x in range(11)]}
    ),
    html.Label("Regulator PI rozmyty - wartość mały dodatni:"),
    dcc.Slider(
        id='md-slider',
        min=0,
        max=1,
        step=0.01,
        value=0.55,
        marks={i: str(i) for i in [x / 10 for x in range(11)]}
    ),
    html.Label("Regulator PI rozmyty - wartość średni dodatni:"),
    dcc.Slider(
        id='sd-slider',
        min=0,
        max=1,
        step=0.01,
        value=0.7,
        marks={i: str(i) for i in [x / 10 for x in range(11)]}
    ),
    html.Label("Regulator PI rozmyty - wartość duzy dodatni:"),
    dcc.Slider(
        id='dd-slider',
        min=0,
        max=1,
        step=0.01,
        value=0.9,
        marks={i: str(i) for i in [x / 10 for x in range(11)]}
    ),
    html.Label("Regulator PI rozmyty - wartość bardzo duzy dodatni:"),
    dcc.Slider(
        id='bdd-slider',
        min=0,
        max=1,
        step=0.01,
        value=1,
        marks={i: str(i) for i in [x / 10 for x in range(11)]}
    ),

    html.Label("Regulator PD rozmyty - wartość przynależności trójkąta:"),
    dcc.Slider(
        id='affiliation-slider',
        min=0,
        max=10,
        step=0.25,
        value=2,
        marks={i: str(i) for i in range(0, 11, 1)}
    ),




    dcc.Graph(id='height-plot'),
    dcc.Graph(id='omega-plot'),
    dcc.Graph(id='acc-plot'),
    dcc.Graph(id='current-plot'),
    dcc.Graph(id='height2-plot'),
    dcc.Graph(id='fuzzy-plot'),
    dcc.Graph(id='fuzzy2-plot'),
])

@app.callback(
    [Output('omega-plot', 'figure'),
     Output('acc-plot', 'figure'),
     Output('height-plot', 'figure'),
     Output('current-plot', 'figure'),
     Output('fuzzy-plot', 'figure'),
     Output('fuzzy2-plot', 'figure'),
     Output('height2-plot', 'figure'),],
    [Input('uz-slider', 'value'),
     Input('ml-slider', 'value'),

     Input('kp-slider', 'value'),
     Input('td-slider', 'value'),

    Input('bdu-slider', 'value'),
    Input('du-slider', 'value'),
    Input('su-slider', 'value'),
    Input('mu-slider', 'value'),
    Input('z-slider', 'value'),
    Input('md-slider', 'value'),
    Input('sd-slider', 'value'),
    Input('dd-slider', 'value'),
    Input('bdd-slider', 'value'),

    Input('affiliation-slider', 'value'),]
)
def update_simulation(Uz, M_l, Kp, Td, BDU, DU, SU, MU, Z, MD, SD, DD, BDD, e_aff):
# def update_simulation(Uz, M_l, Kp, Td, e_aff):

    omega_values = []
    acc_values = []
    height_values = []
    time = []
    current_values = []
    equations.reset_simulation()
    variable.H_requested = Uz
    variable.M_l = M_l

    variable.Kp = Kp
    variable.Td = Td

    variable.BDU = BDU
    variable.DU = DU
    variable.SU = SU
    variable.MU = MU
    variable.Z = Z
    variable.MD = MD
    variable.SD = SD
    variable.DD = DD
    variable.BDD = BDD
    variable.e_aff = e_aff

    for i in range(steps):  
        u_regulator = regulator_PD.PD_new_current()
        u = regulator_PD.rescale_u(u_regulator)
        equations.simulation_step(u)

        time.append(i * const.T_p)
        omega_values.append(variable.omega_s)
        acc_values.append(variable.A)
        height_values.append(variable.H_p)
        current_values.append(variable.U_z)


    fuzzy = []
    fuzzy2 = []
    height_values2 = []
    equations.reset_simulation()


    for i in range(steps):
        u_regulator = regulator_fuzzy_PI.regulator_fuzzy()
        u = regulator_fuzzy_PI.rescale_u(u_regulator)
        equations.simulation_step(u)

        fuzzy.append(u_regulator)
        fuzzy2.append(u)
        height_values2.append(variable.H_p)
        if i % 10 == 0:
            print(i)

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

    fuzzy_fig = go.Figure()
    fuzzy_fig.add_trace(go.Scatter(x=time, y=fuzzy, mode='lines', name='Z regulatora rozmytego'))
    fuzzy_fig.update_layout(title='Wartości w czasie', xaxis_title='Czas (s)', yaxis_title='Wartosci')
    equations.is_simulation_realistic()

    fuzzy2_fig = go.Figure()
    fuzzy2_fig.add_trace(go.Scatter(x=time, y=fuzzy2, mode='lines', name='Napiecie (V)'))
    fuzzy2_fig.update_layout(title='Napięcie w czasie z rozmytego', xaxis_title='Czas (s)', yaxis_title='Napiecie (V)')

    height2_fig = go.Figure()
    height2_fig.add_trace(go.Scatter(x=time, y=height_values2, mode='lines', name='Wysokość (m)'))
    height2_fig.update_layout(title='Wysokość w czasie dla rozmytego', xaxis_title='Czas (s)', yaxis_title='H (m)')
    return omega_fig, acc_fig, height_fig, current_fig, fuzzy_fig, fuzzy2_fig, height2_fig

if __name__ == '__main__':
    app.run(debug=True)
