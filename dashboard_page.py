# pages/dashboard_page.py
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import json
import os

# Load data
with open('D:\data visulization\karnataka.json', 'r') as f:
    geojson = json.load(f)
df = pd.read_csv('D:\data visulization\water_data5.csv')

# ... Other imports and code specific to the dashboard page ...

layout = html.Div(style={'backgroundColor': '#f2f2f2'}, children=[
    dcc.Location(id='url', refresh=False),
    html.H1("Groundwater Analysis", style={'textAlign': 'center', 'color': '#333333'}),
    # ... Rest of the dashboard layout ...
])
