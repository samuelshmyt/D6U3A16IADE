import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

import plotly.express as px

from _map import *
from _histogram import *
# APP ======================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
server = app.server
app.scripts.config.serve_locally = True
server = app.server

# FIM APP ==================================================

# Início do Dataset ==========================================
df = pd.read_csv("dataset/MODIFICADOaleatorio.csv")

#coordenadas_cidades = {
#    'São Paulo': {'LAT': -23.5505, 'LONG': -46.6333},
#    'Porto Alegre': {'LAT': -30.0346, 'LONG': -51.2177},
#    'Rio de Janeiro': {'LAT': -22.9068, 'LONG': -43.1729},
#    'Campinas': {'LAT': -22.9056, 'LONG': -47.0608},
#    'Belo Horizonte': {'LAT': -19.9167, 'LONG': -43.9345},
#}


#df['LAT'] = df['CIDADE'].map(lambda cidade: coordenadas_cidades[cidade]['LAT'])
#df['LONG'] = df['CIDADE'].map(
#    lambda cidade: coordenadas_cidades[cidade]['LONG'])

# Fim do Dataset ==========================================
# CONTRPÇER =============================================

lista_cidades = {
    'All': 'All',
    'São Paulo': 'São Paulo',
    'Porto Alegre': 'Porto Alegre',
    'Rio de Janeiro': 'Rio de Janeiro',
    'Campinas': 'Campinas',
    'Belo Horizonte': 'Belo Horizonte',
}

slider_size = [df['DESPESA_TOTAL'].quantile(0), df['DESPESA_TOTAL'].quantile(
    0.25), df['DESPESA_TOTAL'].quantile(0.5), df['DESPESA_TOTAL'].quantile(0.75), df['DESPESA_TOTAL'].quantile(1)]

lista_menu = {
    'AREA': 'AREA',
    'QUARTOS': 'QUARTOS',
    'BANHEIRO': 'BANHEIRO',
    'ESTACIONAMENTO': 'ESTACIONAMENTO',
    'PISO': 'PISO',
    'ANIMAL': 'ANIMAL',
    'MOBILIA': 'MOBILIA',
    'TAXA': 'TAXA',
    'ALUGUEL': 'ALUGUEL',
    'IPTU': 'IPTU',
    'SEGURO': 'SEGURO',
}

controllers = dbc.Row([
    html.Div(style={"margin-top": "10px"}),    
    html.Img(id="logo", src=app.get_asset_url(
        "logo_ufma.png"), style={"width": "100%"}),
    html.H2("ATIVIDADE 16", style={"margin-top": "30px;font-weight: bold"}),        
    html.H3("DASHBOARD Brazilian Houses to Rent", style={"margin": "0px;font-weight: bold"}),
    html.P('''1.Disciplina: Visualização de Dados ADIA ''', style={"margin": "0px"}),
    html.P('''2.Professor: Dr.Paulo Rogério de A. Ribeiro  ''', style={"margin": "0px"}),
    html.P('''3.Tutor: Prof. Daniel Duarte Co''', style={"margin": "0px"}),
    html.H4("DESPESA_TOTAL(R$):", style={"margin-top": "20px", "margin-bottom": "10px"}),
    dcc.Slider(
        min=0, max=4,
        id='slider-square-size',
        marks={i: str(j) for i, j in enumerate(slider_size)},
        step=None,
        value=1,
    ),
    html.H4("CIDADE:",
            style={"margin-top": "20px", "margin-bottom": "10px"}),
    dcc.Dropdown(
        id="local-dropdown",
        options=[{"label": i, "value": j} for i, j in lista_cidades.items()],
        value='All',
        clearable=False,
       # placeholder="Selecione a CIDADE:",
    ),
       html.H4("MENU:",
            style={"margin-top": "20px", "margin-bottom": "10px"}),
    dcc.Dropdown(
        id="menu-dropdown",
        options=[{"label": i, "value": j} for i, j in lista_menu.items()],
        value="AREA",
        clearable=False,
       # placeholder="Selecione a MENU:",
    ),

])

# FIM CONTROLLER =======================================
# Início do Layout =========================================
app.layout = dbc.Container(
    children=[
        dbc.Row([
                dbc.Col([controllers], md=3),
                dbc.Col([map, hist], md=9),
                ])

    ], fluid=True, )

# Fim do Layout =========================================

# Início do Calbacks =========================================


@app.callback(
    [Output('hist-graph', 'figure'),Output('map-graph', 'figure')],
    [Input('local-dropdown', 'value'),
     Input('slider-square-size', 'value'),
     Input('menu-dropdown', 'value')]
)
def update_hist(local, square_size, color_map):
    if local is None:
        df_intermediate = df.copy()   
    else:
        df_intermediate = df[df["CIDADE"] == local] if local != 'All' else df.copy()
        tamanho_limite = slider_size[square_size] if square_size is not None else df['DESPESA_TOTAL'].min()
        df_intermediate = df_intermediate[df_intermediate['DESPESA_TOTAL'] <= tamanho_limite]
        hist_fig = px.histogram(df_intermediate, x=color_map, opacity=0.75)
        hist_layout = go.Layout(
            margin=go.layout.Margin(l=10, r=0, t=0, b=50),
            showlegend=False,
            template="plotly",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        hist_fig.layout = hist_layout

    mean_lat = df_intermediate["LAT"].mean()
    mean_long = df_intermediate["LONG"].mean()

    px.set_mapbox_access_token(open("keys/mapbox_key").read()) 
    
    map_fig = px.scatter_mapbox(df_intermediate,lat="LAT",lon="LONG",
                                color=color_map,
                                size_max=50,zoom= 12 if local != 'All' else 4,opacity=0.4)  
    map_fig.update_layout(mapbox=dict(center=go.layout.mapbox.Center(lat=mean_lat,lon=mean_long)),
        template="plotly",
        paper_bgcolor="rgba(0,0,0,0)",
         margin=go.layout.Margin(l=10, r=10, t=10, b=10),
    ) 
    return hist_fig, map_fig

# Início do Calbacks =========================================


if __name__ == '__main__':
    app.run_server(debug=False)
    # app.run_server(host="0.0.0.0", port=8050)
