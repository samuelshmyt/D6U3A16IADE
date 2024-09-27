from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

fig = go.Figure()
fig.update_layout(template="plotly", paper_bgcolor="rgba(0,0,0,0)")
subb = dbc.Row([
    dcc.Graph(id="sub-graph", figure=fig)
], style={"height": "140vh"})