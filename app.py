import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

from _map import *
from _subgraf import *
from _quant import *


# APP ======================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
server = app.server
app.scripts.config.serve_locally = True
server = app.server

# FIM APP ==================================================

# Início do Dataset ==========================================
df = pd.read_csv("dataset/MODIFICADOaleatorio.csv")
df['PISO'] = pd.to_numeric(df['PISO'], errors='coerce')
df = df.dropna()
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

slider_size = [df['DESPESA_TOTAL'].quantile(0), df['DESPESA_TOTAL'].quantile(0.25), df['DESPESA_TOTAL'].quantile(0.5), df['DESPESA_TOTAL'].quantile(0.75), df['DESPESA_TOTAL'].quantile(1)]
slider_value = ["1%","25%","50%","75%","100%"]

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
    'DESPESA_TOTAL':'DESPESA_TOTAL'
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
    html.H4("PREÇO TOTAL DO ALUGUEL(R$):", style={"margin-top": "20px", "margin-bottom": "10px"}),
    dcc.Slider(
        min=0, max=4,
        id='slider-square-size',
        marks={i: str(j) for i, j in enumerate(slider_size)},
        step=None,
        value=4,
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

card_icon = {
    #'fontSize': '30px',  # Tamanho do ícone
    'backbackground-color': '#FFFFFF',  # Cor do ícone
#'padding': '10px'    # Espaçamento interno (opcional)
}
app.layout = dbc.Container([
        html.Link(
        href="https://fonts.googleapis.com/icon?family=Material+Icons",
        rel="stylesheet"
        ),
        dbc.Row([
                dbc.Col([controllers], md=3),
                dbc.Col([
                    dbc.Row([
                    # lucro bruto 
                        dbc.CardGroup([
                        dbc.Card(
                            html.Div(className="material-icons", children="point_of_sale", style={'fontSize': '48px', 'color': 'white','padding': '22px 12px'}),
                            color='warning',
                            style={'maxWidth':75,'height':100,'margin-left':'10px'} 
                        ),
                        dbc.Card([
                            html.Legend("LUCRO BRUTO:"),
                            html.H5(["R$"],id="p-bruto-dashboard",style={"font-size": "20px"}),
                        ],style={'padding-left':'10px','padding-top':'10px', "color":"#6B1527",}
                        ),
                    ], style={'maxWidth':'30%','height':100,'margin':'1%'} ),
            
                    # Despesa 
                    dbc.CardGroup([
                        dbc.Card(
                            html.Div(className="material-icons", children="sell", style={'fontSize': '48px', 'color': 'white','padding': '22px 12px'}),
                            color='danger',
                            style={'maxWidth':75,'height':100,'margin-left':'10px'} 
                        ),
                        dbc.Card([
                            html.Legend("DESPESAS:"),
                            html.H5(["R$"],id="p-despesa-dashboard",style={"font-size": "20px"}),
                        ],style={'padding-left':'10px','padding-top':'10px', "color":"#6B1527",}),
                    ],style={'maxWidth':'30%','height':100,'margin':'1%'}),

                    # Lucro Liquido
                    dbc.CardGroup([
                        dbc.Card(
                            html.Div(className="material-icons", children="savings", style={'fontSize': '48px', 'color': 'white','padding': '22px 12px'}),
                            color='success',
                            style={'maxWidth':75,'height':100,'margin-left':'10px','color':'white'} 
                        ),
                        dbc.Card([
                            html.Legend("LUCRO LIQUIDO:"),
                            html.H5(["R$"],id="p-liquido-dashboard",style={"font-size": "20px"}),
                        ],style={'padding-left':'10px','padding-top':'10px', "color":"#6B1527",}),
                        
                    ],style={'maxWidth':'30%','height':100,'margin':'1%'}),
                ]),

                html.Hr(style={"margin-top": "22px", "color":"#6B1527"}),                
                dbc.Row([html.H4("IMOBILIÁRIA BRAZILIAN HOUSES & ALUGÉIS", style={"margin-top": "20px", "margin-left": "50px","color": "#6B1527","font-size": "30px",}),]),
                dbc.Row([html.H4("- Dados de casas para alugar (2020)", style={"margin-top": "10px", "margin-left": "50px","color": "#6B1527","font-size": "20px",}),]),
                dbc.Row([dbc.Col([map],md=12),],),
                html.Hr(style={"color":"#6B1527"}),                       
                dbc.Row([dbc.Col([quant],md=12),],),
                html.Hr(style={"color":"#6B1527"}),                     
                dbc.Row([dbc.Col([subb],md=12),],),
                html.Br(),
                html.Hr(style={"color":"#6B1527"}), 

            ])                
         ])
    ], fluid=True, )

# Fim do Layout =========================================

# Início do Calbacks =========================================


@app.callback(
    [Output('map-graph', 'figure'),
     Output('quant-graph', 'figure'),
     Output('sub-graph', 'figure'),
     Output("p-bruto-dashboard", "children"),
     Output("p-despesa-dashboard", "children"),
     Output("p-liquido-dashboard", "children")],
    [Input('local-dropdown', 'value'),
     Input('slider-square-size', 'value'),
     Input('menu-dropdown', 'value')]
)
def update_hist(local, square_size, color_map):
    if local is None:
        df_intermediate = df.copy()   
    else:
        df_intermediate = df[df["CIDADE"] == local] if local != 'All' else df.copy()
        tamanho_limite = slider_size[square_size] if square_size is not None else slider_size[4]
        df_intermediate = df_intermediate[df_intermediate['DESPESA_TOTAL'] <= tamanho_limite]

   
    # // MAPA 
    mean_lat = df_intermediate["LAT"].mean()
    mean_long = df_intermediate["LONG"].mean()

    px.set_mapbox_access_token(open("keys/mapbox_key").read()) 
    map_fig = px.scatter_mapbox(df_intermediate,lat="LAT",lon="LONG",
                                color=color_map,
                                size_max=50,zoom= 12 if local != 'All' else 3,opacity=0.4)  
    map_fig.update_layout(mapbox=dict(center=go.layout.mapbox.Center(lat=mean_lat,lon=mean_long)),
        template="plotly",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=go.layout.Margin(l=10, r=10, t=10, b=10),
    ) 
    # quant
    contagem_por_cidade = df_intermediate['CIDADE'].value_counts().reset_index()
    contagem_por_cidade.columns = ['CIDADE', 'CONTAGEM']
    soma_contagem = contagem_por_cidade['CONTAGEM'].sum()

    quant_fig = px.bar(
        contagem_por_cidade,
        x='CIDADE',
        y='CONTAGEM',
        title='Contagem de IMÓVEIS por CIDADE',
        labels={'CONTAGEM': 'Número de Imóveis', 'CIDADE': 'Cidade'},
        color='CONTAGEM',
        text='CONTAGEM'
    )

    quant_fig.add_annotation(
        xref="paper", yref="paper",
        x=0.5, y=1.1,  
        text=f"Soma Total de Imóveis: {soma_contagem}",
        showarrow=False,
        font=dict(size=14)
    )
    

    # // SUBPLOT
    coluna_quantitativa = ['AREA', 'QUARTOS', 'BANHEIRO', 'ESTACIONAMENTO', 'PISO', 'TAXA', 'ALUGUEL', 'IPTU', 'SEGURO','DESPESA_TOTAL']
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
        pie_fig = px.pie(df_agrupado,names=coluna,values='CONTAGEM',color=coluna)
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
        sub_fig.update_layout(height=700, width=1000,  margin=dict(l=0, r=0), title_text="Dados Quanlitativos  "+ color_map + " por FAIXA DE PREÇO")

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
        text_auto=True  # Exibe os valores nas barras,

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
        values = valorY,
        color=coluna,
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
        sub_fig.update_layout(height=900, width=1000,showlegend=False, margin=dict(l=0, r=0),title_text="Dados Quantitativos n° MÉDIO DE "+ color_map + " por FAIXA DE PREÇO")

        # Mostrar o gráfico
        #sub_fig.show()

    else:
        print(f'A coluna {coluna} não foi encontrada nas listas.')


    bruto_calc = df_intermediate["DESPESA_TOTAL"].sum() 
    bruto =  f"R$ {bruto_calc:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    despesa_calc = df_intermediate["TAXA"].sum() + df_intermediate["IPTU"].sum() + df_intermediate["SEGURO"].sum()   
    despesa =  f"R$ {despesa_calc:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    liquido_calc = bruto_calc - despesa_calc   
    liquido =  f"R$ {liquido_calc:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    return map_fig,quant_fig,sub_fig,bruto,despesa,liquido

# Início do Calbacks =========================================


if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(host="0.0.0.0", port=8050)
