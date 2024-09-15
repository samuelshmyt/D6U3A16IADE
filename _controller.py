from dash import html, dcc
import dash_bootstrap_components as dbc
from app import app
import pandas as pd

df = pd.read_csv("dataset/MODIFICADOaleatorio.csv")

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
