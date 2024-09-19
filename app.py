import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

from _map import *
from _histogram import *
from _subgraf import *
# APP ======================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
server = app.server
app.scripts.config.serve_locally = True
server = app.server

# FIM APP ==================================================

# Início do Dataset ==========================================
df = pd.read_csv("dataset/MODIFICADOaleatorio.csv")

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
    html.H4("|", style={"margin-top": "10px","color": "white"}),        
    html.H3("DASHBOARD Brazilian Houses to Rent", style={"margin": "0px;font-weight: bold"}),
    html.P('''1.Disciplina: Visualização de Dados ADIA ''', style={"margin": "0px"}),
    html.P('''2.Professor: Dr.Paulo Rogério de A. Ribeiro  ''', style={"margin": "0px"}),
    html.P('''3.Tutor: Prof. Daniel Duarte Co''', style={"margin": "0px"}),
    html.P('''4.Aluno: Samuel G Alves''', style={"margin": "0px"}),
    html.H4("DESPESA_TOTAL(R$):", style={"margin-top": "20px", "margin-bottom": "10px"}),
    dcc.Slider(
        min=0, max=4,
        id='slider-square-size',
        marks={i: str(j) for i, j in enumerate(slider_size)},
        step=None,
        value=2,
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
                dbc.Col([
                    dbc.Row([
                        html.H4("IMOBILIÁRIA BRAZILIAN HOUSES X ALUGÉIS", style={"margin-top": "20px", "margin-left": "50px","color": "#6B1527","font-size": "30px",}),
                    ]),
                    dbc.Row([dbc.Col([map],md=12),
                    ],),
                    dbc.Row([
                    dbc.Col([
                        html.H4("Distribuição dos preços por Menu", style={"margin-top": "10px", "margin-left": "50px","color": "#6B1527","font-size": "15px",})
                        ,hist
                        ],md=11),
                    ],),
                    dbc.Row([dbc.Col([subb],md=12),
                    ],),                        
                ], md=9),

                ])

    ], fluid=True, )

# Fim do Layout =========================================

# Início do Calbacks =========================================


@app.callback(
    [Output('hist-graph', 'figure'),Output('map-graph', 'figure'),Output('sub-graph', 'figure')],
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
    
    # // HISTORIOGRAMA 
    hist_fig = px.histogram(df_intermediate, x=color_map, opacity=0.75)
    hist_layout = go.Layout(
            margin=go.layout.Margin(l=10, r=0, t=0, b=50),
            showlegend=False,
            template="plotly",
            paper_bgcolor="rgba(0,0,0,0)",
            title="Aluguel x Despesas Finais",
        )
    hist_fig.layout = hist_layout
    
    # // MAPA 
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

    # // SUBPLOT
    coluna_quantitativa = ['AREA', 'QUARTOS', 'BANHEIRO', 'ESTACIONAMENTO', 'PISO', 'TAXA', 'ALUGUEL', 'IPTU', 'SEGURO']
    coluna_qualitativa = ['ANIMAL', 'MOBILIA']
    frequencia = [499.0, 2061.75, 3581.5, 6768.0, 1120000.0]
    coluna = color_map
    square_size = square_size

    if coluna in coluna_qualitativa:

        df_intermediate['CATEGORIA_DESPESA'] = pd.cut(df_intermediate['DESPESA_TOTAL'], bins=frequencia, labels=[f'{frequencia[i]} - {frequencia[i+1]}' for i in range(len(frequencia)-1)])
        df_agrupado = df_intermediate.groupby(['CATEGORIA_DESPESA', coluna], observed=False).size().reset_index(name='CONTAGEM')
        valorX = df_agrupado.CATEGORIA_DESPESA
        valorY = df_agrupado.CONTAGEM

        print(f'A coluna {coluna} é qualitativa.')

        sub_fig = make_subplots(rows=4, cols=1, specs=[[{'type': 'xy'}], [{'type': 'xy'}], [{'type': 'xy'}], [{'type': 'domain'}]])

        bar_fig = px.bar(df_agrupado,x=valorX,y=valorY,color=coluna, barmode='group', text_auto=True)
        line_fig = px.line(df_agrupado,x= valorX,y= valorY,color=coluna,markers=True, labels={'CATEGORIA_DESPESA': 'Categoria de Despesa', 'CONTAGEM': 'Contagem de Imóveis'})
        corr_fig = px.box(df_agrupado,valorY,color=coluna,orientation='h')
        pie_fig = px.pie(
        df_agrupado,
        names=coluna,# Diferenciar entre "Sim" e "Não" para ANIMAL
        values='CONTAGEM',  # Usar a contagem de imóveis para as fatias
        color=coluna, # Diferenciar as fatias por "ANIMAL" (Sim ou Não)
        #title='Relação entre Categoria de Despesa Total e Presença de Animais',
        #labels={'ANIMAL': 'Presença de Animais', 'CONTAGEM': 'Contagem de Imóveis'},
        #facet_col='CATEGORIA_DESPESA'  # Adiciona as categorias de despesa como facetas separadas
        )
        pie_fig.update_layout()
        
        # Adicionar o gráfico de barras
        for trace in bar_fig['data']:
            sub_fig.add_trace(trace, row=1, col=1)

        # Adicionar o gráfico de dispersão
        for trace in line_fig['data']:
            sub_fig.add_trace(trace, row=2, col=1)

        # Adicionar o gráfico de dispersão
        for trace in corr_fig['data']:
            sub_fig.add_trace(trace, row=3, col=1)

        # Adicionar o gráfico de dispersão
        for trace in pie_fig['data']:
            sub_fig.add_trace(trace, row=4, col=1)

        # Ajustar a largura do gráfico de pizza no subplot
        sub_fig.update_traces(domain=dict(x=[0, 1]), row=4, col=1)

        # Atualizar layout
        sub_fig.update_layout(height=700, width=1000,  margin=dict(l=0, r=0), title_text="Subplots com Plotly Express Qualitativa")

        # Mostrar o gráfico
        #sub_fig.show()

    elif coluna in coluna_quantitativa:
        df_intermediate['CATEGORIA_DESPESA'] = pd.cut(df_intermediate['DESPESA_TOTAL'], bins=frequencia, labels=[f'{frequencia[i]} - {frequencia[i+1]}' for i in range(len(frequencia)-1)])
        df_agrupado = df_intermediate.groupby('CATEGORIA_DESPESA', observed=False)[coluna].mean().reset_index()
        valorX = df_agrupado.CATEGORIA_DESPESA
        valorY = df_agrupado[coluna]

        print(f'A coluna {coluna} é quantitativa.')

        # Criar os subplots - Exemplo com 1 linha e 2 colunas
        #sub_fig = make_subplots(rows=4, cols=1)
        sub_fig = make_subplots(rows=4, cols=1, specs=[[{'type': 'xy'}], [{'type': 'xy'}], [{'type': 'xy'}], [{'type': 'domain'}]])

        bar_fig = px.bar(
        x= valorX,
        y= valorY,
        title='Relação entre Categoria de Área e Despesa Total',
        labels={'CATEGORIA_AREA': 'Intervalo de Área (m²)', 'DESPESA_TOTAL': 'Despesa Total Média (R$)'},
        text_auto=True  # Exibe os valores nas barras
        )
        line_fig = px.line(
        x= valorX,
        y= valorY,
        title='Relação entre Categoria de Área e Despesa Total',
        labels={'CATEGORIA_AREA': 'Intervalo de Área (m²)', 'DESPESA_TOTAL': 'Despesa Total Média (R$)'},
        #text_auto=True  # Exibe os valores nas barras
        )
        pie_fig = px.pie(
        df_agrupado,
        names = valorX,
        values = valorY
        )
        corr_fig = px.box(valorY,orientation='h')
        # Atualizar o layout do gráfico para esconder o eixo X

        # Adicionar o gráfico de barras
        for trace in bar_fig['data']:
            sub_fig.add_trace(trace, row=1, col=1)

        # Adicionar o gráfico de dispersão
        for trace in line_fig['data']:
            sub_fig.add_trace(trace, row=2, col=1)

        # Adicionar o gráfico de dispersão
        for trace in corr_fig['data']:
            sub_fig.add_trace(trace, row=3, col=1)

        # Adicionar o gráfico de dispersão
        for trace in pie_fig['data']:
            sub_fig.add_trace(trace, row=4, col=1)

        # Atualizar layout
        sub_fig.update_layout(height=700, width=1000,  margin=dict(l=0, r=0),title_text="Subplots com Plotly Express Quantitativa")

        # Mostrar o gráfico
        #sub_fig.show()

    else:
        print(f'A coluna {coluna} não foi encontrada nas listas.')




    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    return hist_fig, map_fig,sub_fig

# Início do Calbacks =========================================


if __name__ == '__main__':
    app.run_server(debug=False)
    # app.run_server(host="0.0.0.0", port=8050)
