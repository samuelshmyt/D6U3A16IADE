import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from _map import *
from _subgraf import *
from _quant import *


# INICIAR SERVIDORWEB ======================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
server = app.server
app.scripts.config.serve_locally = True
server = app.server


#  DATASET  ==========================================
df = pd.read_csv("dataset/MODIFICADOaleatorio.csv")
df['PISO'] = pd.to_numeric(df['PISO'], errors='coerce')
df = df.dropna()


# VARIAVEIS  =============================================
lista_cidades = {
    'All': 'All',
    'São Paulo': 'São Paulo',
    'Porto Alegre': 'Porto Alegre',
    'Rio de Janeiro': 'Rio de Janeiro',
    'Campinas': 'Campinas',
    'Belo Horizonte': 'Belo Horizonte',
}

slider_size = [df['DESPESA_TOTAL'].quantile(0), df['DESPESA_TOTAL'].quantile(0.25), df['DESPESA_TOTAL'].quantile(0.5), df['DESPESA_TOTAL'].quantile(0.75), df['DESPESA_TOTAL'].quantile(1)]
slider_value =["E:" + str(df['DESPESA_TOTAL'].quantile(.01)), 
               "D:" + str(df['DESPESA_TOTAL'].quantile(.25)), 
               "C:" + str(df['DESPESA_TOTAL'].quantile(.5)),  
               "B:" + str(df['DESPESA_TOTAL'].quantile(.75)), 
               "A:" + str(df['DESPESA_TOTAL'].quantile(1)), 
                ]

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

# PARTE CONTROLE DO SITE
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
        marks={i: str(j) for i, j in enumerate(slider_value)},
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
    ),
       html.H4("MENU:",
            style={"margin-top": "20px", "margin-bottom": "10px"}),
    dcc.Dropdown(
        id="menu-dropdown",
        options=[{"label": i, "value": j} for i, j in lista_menu.items()],
        value="AREA",
        clearable=False,
    ),
])
#   PARTE PRINCIPAL DO SITE 
app.layout = dbc.Container([
        html.Link( href="https://fonts.googleapis.com/icon?family=Material+Icons", rel="stylesheet" ),
        dbc.Row([
                dbc.Col([controllers], md=3),
                dbc.Col([
                    dbc.Col([
                        dbc.Row([html.H1("ANÁLISE FINANCEIRA DA IMOBILIÁRIA BRAZILIAN HOUSES", style={"margin-top": "20px", "margin-left": "50px","color": "#6B1527","font-size": "30px",}),]),
                        dbc.Row([html.H3("1.MISSÃO: Foi feita uma ANÁLISE FINANCEIRA na esfera ADMINISTRATIVA ESTRATÉGICA com o objetivo é AVALIAR A LUCRATIVIDADE DO ALUGUEL DE CASAS", style={"margin-top": "10px", "margin-left": "50px","color": "#6B1527",}),]),
                        html.Hr(style={"margin-top": "22px", "color":"#6B1527"}),
                    ]),
                    dbc.Col([
                        dbc.Row([html.H3("2.ONDE ESTÃO LOCALIZADOS AS PROPRIEDADES PARA ALOCAÇÃO?", style={"margin-top": "10px", "margin-left": "50px","color": "#6B1527",}),]),
                        dbc.Row([dbc.Col([map],md=12),],),
                        html.Hr(style={"color":"#6B1527"}), 
                    ]),
                    dbc.Col([
                        dbc.Row([html.H3("3.QUAL A SÍNTESE FINANCEIRA DO NEGÓCIO?", style={"margin-top": "10px", "margin-left": "50px","color": "#6B1527",}),]),
                        dbc.Row([
                                # lucro bruto 
                                    dbc.CardGroup([
                                    dbc.Card(
                                        html.Div(className="material-icons", children="point_of_sale", style={"font-size": "2vw", 'color': 'white','padding': '22px 12px'}),
                                        color='warning',
                                        style={'maxWidth':75,'maxheight':100,'margin-left':'10px','text-align': 'center',} 
                                    ),
                                    dbc.Card([
                                        html.Legend("LUCRO BRUTO:",style={"font-size": "1vw",'font-weight': 'bold'}),
                                        html.H5(["R$"],id="p-bruto-dashboard",style={"font-size": "1vw"}),
                                    ],style={'padding-left':'10px','padding-top':'10px', "color":"#6B1527",}
                                    ),
                                ], style={'maxWidth':'30%','maxheight':100,'margin':'1%'} ),

                                # Despesa 
                                dbc.CardGroup([
                                    dbc.Card(
                                        html.Div(className="material-icons", children="sell", style={"font-size": "2vw", 'color': 'white','padding': '22px 12px'}),
                                        color='danger',
                                        style={'maxWidth':75,'maxheight':100,'margin-left':'10px','text-align': 'center',} 
                                    ),
                                    dbc.Card([
                                        html.Legend("DESPESAS:",style={"font-size": "1vw",'font-weight': 'bold'}),
                                        html.H5(["R$"],id="p-despesa-dashboard",style={"font-size": "1vw"}),
                                    ],style={'padding-left':'10px','padding-top':'10px', "color":"#6B1527",}),
                                ],style={'maxWidth':'30%','maxheight':100,'margin':'1%'}),

                                # Lucro Liquido
                                dbc.CardGroup([
                                    dbc.Card(
                                        html.Div(className="material-icons", children="savings", style={"font-size": "2vw", 'color': 'white','padding': '22px 12px'}),
                                        color='success',
                                        style={'maxWidth':75,'maxheight':100,'margin-left':'10px','color':'white','text-align': 'center',} 
                                    ),
                                    dbc.Card([
                                        html.Legend("LUCRO LIQUIDO:",style={"font-size": "1vw",'font-weight': 'bold'}),
                                        html.H5(["R$"],id="p-liquido-dashboard",style={"font-size": "1vw"}),
                                    ],style={'padding-left':'10px','padding-top':'10px', "color":"#6B1527",}),
                                    
                                ],style={'maxWidth':'30%','maxheight':100,'margin':'1%'}),
                                html.Hr(style={"margin-top": "38px", "color":"#6B1527"}),
                            ]),
                    ], md=12, style={"margin-bottom": "10px" }), 
                    dbc.Col([
                        dbc.Col([ 
                                dbc.Row([html.H3("4.QUAL OS FATORES ECONÔMICOS GERAIS DO NEGÔCIO?", style={"margin-top": "10px", "margin-left": "50px","color": "#6B1527",}),]),                                    
                                dbc.Row([dbc.Col([quant],md=12),],style={"height": "1100px"}),
                                html.Hr(style={"color":"#6B1527"}),  
                                dbc.Row([html.H3("5.QUAIS AS CARACTERISTICAS QUALITATIVAS E QUANTITATIVAS X FAIXA DE PREÇO?", style={"margin-top": "10px", "margin-left": "50px","color": "#6B1527",}),]),                    
                                dbc.Row([dbc.Col([subb],md=12),],style={"height": "1100px","width":"1000px"}),
                                html.Br(),
                                html.Hr(style={"color":"#6B1527"}), 
                        ]),
                    ], md=12),   
                ], md=9),               
         ])
    ], fluid=True, )

# FUNÇÃO  =========================================
def Resumo_financeiro(df_intermediate):
       
    bruto_calc = df_intermediate["DESPESA_TOTAL"].sum() 
    bruto =  f"R$ {bruto_calc:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    despesa_calc = df_intermediate["TAXA"].sum() + df_intermediate["IPTU"].sum() + df_intermediate["SEGURO"].sum()   
    despesa =  f"R$ {despesa_calc:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    liquido_calc = bruto_calc - despesa_calc   
    liquido =  f"R$ {liquido_calc:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    return bruto, despesa,liquido

def Mapa_geografico(df_intermediate,color_map, local):
        
    mean_lat = df_intermediate["LAT"].mean()
    mean_long = df_intermediate["LONG"].mean()
    px.set_mapbox_access_token(open("keys/mapbox_key").read()) 
    map_fig = px.scatter_mapbox(df_intermediate,lat="LAT",lon="LONG", color=color_map,size_max=50,zoom= 12 if local != 'All' else 3,opacity=0.4,hover_data=["CIDADE", "LAT", "LONG",color_map])  
    map_fig.update_layout(mapbox=dict(center=go.layout.mapbox.Center(lat=mean_lat,lon=mean_long)),
        template="plotly", paper_bgcolor="rgba(0,0,0,0)", margin=go.layout.Margin(l=10, r=10, t=10, b=10),
    ) 
    return map_fig

def sub_grafico_global(df_intermediate):
    # Gráfico de contagem de imóveis
    contagem_por_cidade = df_intermediate['CIDADE'].value_counts().reset_index()
    contagem_por_cidade.columns = ['CIDADE', 'CONTAGEM']
    soma_contagem = contagem_por_cidade['CONTAGEM'].sum()
    colunas_despesa = ['TAXA', 'IPTU', 'SEGURO']
    ordem_cidades = ['São Paulo', 'Rio de Janeiro', 'Porto Alegre', 'Campinas', 'Belo Horizonte']

    quant_fig = px.bar(
        contagem_por_cidade,
        x='CIDADE',
        y='CONTAGEM',
        title='Contagem de IMÓVEIS por CIDADE',
        labels={'CONTAGEM': 'Número de Imóveis', 'CIDADE': 'Cidade'},
        text='CONTAGEM',
        color_discrete_sequence=['blue', '#696969', '#A9A9A9', '#D3D3D3', '#808080']
    )
    quant_fig.update_traces(marker_color='green')  
    quant_fig.add_annotation(
        xref="paper", yref="paper",
        x=0.5, y=1.1,  
        text=f"Soma Total de Imóveis: {soma_contagem}",
        showarrow=False,
        font=dict(size=14)
    )
    quant_fig.update_layout(
        showlegend=True,
        legend=dict(
            x=0.8,  # Posição da legenda no eixo X (ajustar conforme necessário)
            y=0.9,  # Posição da legenda no eixo Y
            bgcolor="rgba(255, 255, 255, 0.5)",  # Fundo branco semi-transparente
            bordercolor="Black",
            borderwidth=1
        )
    )

     # Gráfico financeiro
    colunas_quantitativas = ['ALUGUEL', 'TAXA', 'IPTU', 'SEGURO']
    receita_por_cidade = df_intermediate.groupby('CIDADE', observed=False)[colunas_quantitativas].sum().reset_index()
    receita_por_cidade[colunas_quantitativas] = receita_por_cidade[colunas_quantitativas] / 1e6

    graf_finc = px.bar(
        receita_por_cidade.melt(id_vars='CIDADE', value_vars=colunas_quantitativas),
        x='CIDADE',
        y='value',
        color='variable',
        title='Lucro Bruto a Recolher por Cidade',
        labels={'value': 'Valor (Milhões)', 'variable': 'Tipo'},
        text='value',
        color_discrete_sequence=['blue', '#696969', '#A9A9A9', '#D3D3D3']
    )

    graf_finc.update_traces(texttemplate='%{text:.2f}M', textposition='outside')

    soma_total_por_cidade = receita_por_cidade[colunas_despesa].sum(axis=1)

    graf_finc.add_trace(go.Scatter(
        x=receita_por_cidade['CIDADE'],
        y=soma_total_por_cidade + 0.5,
        mode='markers+text',
        name='Soma das Despesas',
        marker=dict(color='#696969', size=10),
        text=soma_total_por_cidade,
        textposition='top center',
        texttemplate='%{text:.2f}M',
        textfont=dict(size=12),
        
    ))

    soma_total = receita_por_cidade[colunas_quantitativas].sum().sum()
    graf_finc.add_annotation(
        xref="paper", yref="paper",
        x=0.5, y=1.1,
        text=f"Soma Total: {soma_total:.2f}M",
        showarrow=False,
        font=dict(size=14)
    )

    graf_finc.update_layout(barmode='group', showlegend=True, xaxis={'categoryorder': 'array', 'categoryarray': ordem_cidades})

    #graf_finc.update_traces(texttemplate='%{text:.2f}M', textposition='outside')
    graf_finc.update_layout(
        legend=dict(
            x=0.8,
            y=0.9,
            bgcolor="rgba(255, 255, 255, 0.5)",
            bordercolor="Black",
            borderwidth=1
        )
    )

    # Gráfico de correlação
    numerical_columns = df_intermediate.select_dtypes(include=['number'])
    subset_x = numerical_columns.iloc[:, 7:12]
    subset_y = numerical_columns.iloc[:, 2:7]

    correlation_matrix_cross = pd.DataFrame(np.corrcoef(subset_y.T, subset_x.T)[:len(subset_y.columns), len(subset_y.columns):],
                                            index=subset_y.columns, columns=subset_x.columns)

    heatmap = go.Figure(data=go.Heatmap(
        z=correlation_matrix_cross.values,
        x=correlation_matrix_cross.columns,
        y=correlation_matrix_cross.index,
        colorscale='RdYlGn',
        zmin=-1, zmax=1,
        colorbar=dict(title="Correlação"),
        text=np.round(correlation_matrix_cross.values, 2),
        texttemplate="%{text}",
        showscale=False
    ))

    # Subplots
    fig = make_subplots(rows=3, cols=1, row_heights=[0.15, 0.5, 0.3],
                        subplot_titles=("CONTAGEM DE IMOVEIS POR CIDADE", 
                                        "DRE - DEMOSTRAÇÃO DO RESULTADO DO EXERCÍCIO (Receita = Azul e Despeza = Cinza)", 
                                        "CORRELAÇÃO DE FATORES ECONÔMICOS E CARACTERISTICAS DO IMÓVEL"))

    # Adicionar gráficos aos subplots
    for trace in quant_fig['data']:
        fig.add_trace(trace, row=1, col=1)

    for trace in graf_finc['data']:
        fig.add_trace(trace, row=2, col=1)

    for trace in heatmap['data']:
        fig.add_trace(trace, row=3, col=1)

    # Atualizar layout do subplot
    fig.update_layout(
        title_text="ANÁLISE ECONÔMICA GLOBAL",
        showlegend=True,
        height=1100,
        width=1000,
        margin=dict(t=100)
    )

    # Atualizar layout específico para cada gráfico
    fig.update_layout(
        legend=dict(
            x=0.05, y=0.7,  # Ajustar a posição da legenda dentro do gráfico
            bgcolor="rgba(255,255,255,0.6)",  # Fundo branco com opacidade
            bordercolor="black",
            borderwidth=1
        )
    )

    return fig


def sub_grafico_especifico_quantitativo(df_intermediate, color_map, frequencia, coluna):
    df_intermediate['CATEGORIA_DESPESA'] = pd.cut(df_intermediate['DESPESA_TOTAL'], bins=frequencia, 
                                                  labels=[f'{frequencia[i]} - {frequencia[i+1]}' for i in range(len(frequencia) - 1)])
    df_agrupado = df_intermediate.groupby('CATEGORIA_DESPESA', observed=False)[coluna].mean().reset_index()
    valorX = df_agrupado.CATEGORIA_DESPESA
    valorY = df_agrupado[coluna]

    print(f'A coluna {coluna} é quantitativa.')

    # Criar os gráficos
    his_fig = px.histogram(df_intermediate, x=color_map, opacity=0.75)

    corr_fig = px.box(valorY, orientation='h')

    bar_fig = px.bar(
        x=valorX,
        y=valorY,
        labels={'CATEGORIA_DESPESA': 'Intervalo de Despesa (R$)', coluna: 'Despesa Total Média (R$)'},
        text_auto=True
    )

    pie_fig = px.pie(
        df_agrupado,
        names=valorX,
        values=valorY,
        color=coluna,
    )

    rela_fig = px.scatter(
        df_intermediate,  # O DataFrame com os dados
        x=df_intermediate[color_map],  # O eixo X é o mapeamento de cores que você usou
        y=df_intermediate['DESPESA_TOTAL'],  # O eixo Y é a coluna 'DESPESA_TOTAL'
        trendline='ols',  # Adiciona a linha de regressão usando OLS (mínimos quadrados ordinários)
        labels={'x': color_map, 'y': 'Despesa Total'},  # Títulos para os eixos
        opacity=0.75,  # Ajusta a opacidade dos pontos
        title='Importância do '+color_map+' X DESPESA TOTAL '#'Gráfico de Dispersão com Regressão'
    )

    

    # Criar os subplots
    sub_fig = make_subplots(
        rows=5, cols=1,
        specs=[[{'type': 'xy'}], [{'type': 'xy'}], [{'type': 'xy'}], [{'type': 'domain'}], [{'type': 'xy'}]]
    )

    # Adicionar o gráfico de histogramas
    for trace in his_fig['data']:
        sub_fig.add_trace(trace, row=1, col=1)

# Adicionar o gráfico de box
    for trace in corr_fig['data']:
        sub_fig.add_trace(trace, row=2, col=1)

    # Adicionar o gráfico de barras
    for trace in bar_fig['data']:
        sub_fig.add_trace(trace, row=3, col=1)

    # Adicionar o gráfico de pizza
    for trace in pie_fig['data']:
        sub_fig.add_trace(trace, row=4, col=1)

    # Adicionar o gráfico de pizza
    for trace in rela_fig['data']:
        sub_fig.add_trace(trace, row=5, col=1)

    # Atualizar layout
    sub_fig.update_layout(
        height=1000,
        width=1000,
        showlegend=False,
        margin=dict(l=0, r=0),
        title_text="CARACTERÍSTICA QUANTITATIVA: " + color_map + "",
    )

   # Adicionar subtítulos
    sub_fig.add_annotation(
        text="Análise da Distribuição da Variavel: " + color_map,
        xref="paper", yref="paper",
        x=0.5, y=1.03,  # Ajustar a posição do subtítulo
        showarrow=False,
        font=dict(size=18)
    )

    sub_fig.add_annotation(
        text="Box Plot: "  + color_map,
        xref="paper", yref="paper",
        x=0.5, y=0.82,  # Ajustar a posição do subtítulo
        showarrow=False,
        font=dict(size=18)
    )

    sub_fig.add_annotation(
        text="Classificação Média: " + color_map + " X FAIXA DE PREÇO",
        xref="paper", yref="paper",
        x=0.5, y=0.59,  # Ajustar a posição do subtítulo 
        showarrow=False,
        font=dict(size=18)
    )

    sub_fig.add_annotation(
        text="Percentagem de " + color_map + " por Faixa de Preço",
        xref="paper", yref="paper",
        x=0.5, y=0.38,  # Ajustar a posição do subtítulo
        showarrow=False,
        font=dict(size=18)
    )

    sub_fig.add_annotation(
        text="Importância da "+color_map+ " X DESPESA TOTAL",
        xref="paper", yref="paper",
        x=0.5, y=0.15,  # Ajustar a posição do subtítulo
        showarrow=False,
        font=dict(size=18)
    )
 
    return sub_fig

def sub_grafico_especifico_qualitativo(df_intermediate,color_map, frequencia,coluna):
    df_intermediate['CATEGORIA_DESPESA'] = pd.cut(df_intermediate['DESPESA_TOTAL'], bins=frequencia, labels=[f'{frequencia[i]} - {frequencia[i+1]}' for i in range(len(frequencia)-1)])
    df_agrupado = df_intermediate.groupby(['CATEGORIA_DESPESA', coluna], observed=False).size().reset_index(name='CONTAGEM')
    valorX = df_agrupado.CATEGORIA_DESPESA
    valorY = df_agrupado.CONTAGEM

    print(f'A coluna {coluna} é qualitativa.')

    sub_fig = make_subplots(rows=4, cols=1, specs=[[{'type': 'xy'}], [{'type': 'xy'}], [{'type': 'xy'}], [{'type': 'domain'}]])

    hist_fig =  px.histogram(df_agrupado, x=color_map, opacity=0.75)
    bar_fig = px.bar(df_agrupado,x=valorX,y=valorY,color=coluna, barmode='group', text_auto=True)
    corr_fig = px.box(df_agrupado,valorY,color=coluna,orientation='h')
    pie_fig = px.pie(df_agrupado,names=coluna,values='CONTAGEM',color=coluna)
    pie_fig.update_layout()
    
        # Adicionar o gráfico de dispersão
    for trace in hist_fig['data']:
        sub_fig.add_trace(trace, row=1, col=1)

    # Adicionar o gráfico de barras
    for trace in bar_fig['data']:
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
    sub_fig.update_layout(height=700, width=1000, margin=dict(l=0, r=0), title_text="ANÁLISE ESPECÍFICA QUALITATIVA DA "+ color_map + " por FAIXA DE PREÇO")

    # Atualizar layout
    sub_fig.update_layout(
        height=900,
        width=1000,
        showlegend=False,
        margin=dict(l=0, r=0),
        title_text="ANÁLISE ESPECÍFICA QUANTITATIVA DA " + color_map + " por FAIXA DE PREÇO",
    )

    # Adicionar subtítulos
    sub_fig.add_annotation(
        text="Análise da Distribuição da Variavel: " + color_map,
        xref="paper", yref="paper",
        x=0.5, y=1.03,  # Ajustar a posição do subtítulo
        showarrow=False,
        font=dict(size=18)
    )

    sub_fig.add_annotation(
        text="Box Plot: "  + color_map,
        xref="paper", yref="paper",
        x=0.5, y=0.77,  # Ajustar a posição do subtítulo
        showarrow=False,
        font=dict(size=18)
    )

    sub_fig.add_annotation(
        text="Classificação Média: " + color_map + " X FAIXA DE PREÇO",
        xref="paper", yref="paper",
        x=0.5, y=0.47,  # Ajustar a posição do subtítulo
        showarrow=False,
        font=dict(size=18)
    )

    sub_fig.add_annotation(
        text="Percentagem de " + color_map + " por Faixa de Preço",
        xref="paper", yref="paper",
        x=0.5, y=0.20,  # Ajustar a posição do subtítulo
        showarrow=False,
        font=dict(size=18)
    )

    return sub_fig

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

    ## Filtro Geral por cidade e tamanho 
    if local is None:
        df_intermediate = df.copy()   
    else:
        df_intermediate = df[df["CIDADE"] == local] if local != 'All' else df.copy()
        tamanho_limite = slider_size[square_size] if square_size is not None else slider_size[4]
        df_intermediate = df_intermediate[df_intermediate['DESPESA_TOTAL'] <= tamanho_limite]

    bruto,despesa,liquido = Resumo_financeiro(df_intermediate)

    map_fig = Mapa_geografico(df_intermediate,color_map, local)

    sub_global = sub_grafico_global(df_intermediate)

    # 003 SUBPLOT
    coluna_quantitativa = ['AREA', 'QUARTOS', 'BANHEIRO', 'ESTACIONAMENTO', 'PISO', 'TAXA', 'ALUGUEL', 'IPTU', 'SEGURO','DESPESA_TOTAL']
    coluna_qualitativa = ['ANIMAL', 'MOBILIA']
    frequencia = [499.0, 2061.75, 3581.5, 6768.0, 1120000.0]
    coluna = color_map
     
    if coluna in coluna_qualitativa:
        sub_fig = sub_grafico_especifico_qualitativo(df_intermediate,color_map, frequencia,coluna)
        

    elif coluna in coluna_quantitativa:
        sub_fig = sub_grafico_especifico_quantitativo(df_intermediate,color_map, frequencia,coluna)

    else:
        print(f'A coluna {coluna} não foi encontrada nas listas.')


   

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    return map_fig,sub_global,sub_fig,bruto,despesa,liquido

# Início do Calbacks =========================================


if __name__ == '__main__':
    app.run_server(debug=False)
    # app.run_server(host="0.0.0.0", port=8050)