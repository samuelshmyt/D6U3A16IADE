from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

fig = go.Figure()
fig.update_layout(template="plotly", paper_bgcolor="rgba(0,0,0,0)")
quant = dbc.Row([
    dcc.Graph(id="quant-graph", figure=fig)
], style={"height": "50vh"})
