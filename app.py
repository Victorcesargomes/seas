import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px 


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server 
app.scripts.config.serve_locally = True
server = app.server



# ==== CARREGAR DADOS ==== #
df_dados = pd.read_csv('abordagem_seas.csv') 
lat_media = df_dados['lat'].mean()
long_media = df_dados['long'].mean()


# ==== MAPA ==== #
fig = go.Figure()

fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0, 0, 0, 0)")


map_ = dbc.Row([
    dcc.Graph(id="map-graph", figure=fig)
], style={"height": "80vh"})


# ==== CONTROLADORES BAIRRO ==== #
lista_bairro = {
    "TODOS":0,
    "SAO JOSE": 1,
    "BOA VISTA": 2,
    "SANTO AMARO":3,
    "SANTO ANTONIO": 4
}


# ==== CONTROLADORES USUÁRIOS ==== #
lista_usuario = {
    "TODOS": 0,
    "A1":1,
    "A2": 2,
    "A3": 3,
    "A4": 4,
    "A5": 5
}

# ==== CONTROLADORES DIVERSOS ==== #
controlers = dbc.Row([
    html.Img(id="logo", src=app.get_asset_url("logo.png"), style={"width": "80%"}),
    html.H1("Serviço Especializado em Abordagem Social - SEAS", style={"margin-top": "30px", "textAlign": "center"}),


    html.H2("Bairro", style={"margin-top": "50px"}),
    dcc.Dropdown(
        id="location-dropdown",
        options=[{"label": i, "value": j} for i, j in lista_bairro.items()],
        value=0,
        placeholder="Selecione o Bairro"
    ),

    html.H2("Usuário", style={"margin-top": "50px"}),
    dcc.Dropdown(
        id="location-usuario",
        options=[{"label": i, "value": j} for i, j in lista_usuario.items()],
        value=0,
        placeholder="Selecione o Usuário"
    ),
    html.Hr(style={'margin-top': '30px'}),

    html.H2("Variáveis de Controle", style={"margin-bottom": "20px", "margin-top": "25px"}),

    dcc.Dropdown(
        options=[
            {'label': 'sexo', 'value': 'sexo'},
            {'label': 'genero', 'value': 'genero'},
            {'label': 'pop_rua', 'value': 'pop_rua'},
            {'label': 'idade', 'value': 'idade'},
        ],value='pop_rua',
        id="dropdown-color"
    )
])



# ==== LAYOUT PRINCIPAL ==== #]
app.layout = dbc.Container(
    children=[
        dbc.Row([
            dbc.Col([controlers], md=3),
            dbc.Col([map_], md=9),
        ])

    ], fluid=True,)




# ==== CALLBACKS ==== #
@app.callback(Output('map-graph', 'figure'),
             Input('location-dropdown', 'value'),
             Input('location-usuario', 'value'),
             Input('dropdown-color', 'value'))

def update_map(location, usuario, color_map):
    if location == 0 and usuario == 0:
        df_intermediate = df_dados.copy()
    else:
        if location != 0:
            df_intermediate = df_dados[df_dados['bairros'] == location].copy()
        else:
            df_intermediate = df_dados.copy()

        if usuario != 0:
            df_intermediate = df_intermediate[df_intermediate['usuarios'] == usuario].copy()

    px.set_mapbox_access_token(open("keys/mapbox_key").read())

    map_fig = px.scatter_mapbox(df_intermediate, lat="lat", lon="long", color=color_map,
                                size="idade", size_max=15, zoom=14, opacity=0.9, color_continuous_scale='darkmint', hover_data={"nome": True,"descricao": True, "lat":False,
                                                                                                                                "long":False, "idade": True, "sexo": True, "cpf": True, "bairro": True})
    
    map_fig.update_layout(mapbox=dict(center=go.layout.mapbox.Center(lat=lat_media, lon=long_media)),
                          template="plotly_dark", paper_bgcolor="rgba(0, 0, 0, 0)",
                          margin=go.layout.Margin(l=10, r=10, t=10, b=10))

    return map_fig











if __name__ == '__main__':
    app.run_server(debug=True)