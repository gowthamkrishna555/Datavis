# pages/landing_page.py
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from dash import dcc, html

layout = html.Div(style={'backgroundColor': '#f8f9fa', 'height': '100vh'}, children=[
    html.Div(style={'textAlign': 'center', 'padding-top': '150px'}, children=[
        html.H1("Groundwater Analysis", style={'color': '#007BFF'}),
        html.H3("Explore and analyze groundwater data in Karnataka", style={'color': '#6C757D'}),
        dcc.Link(html.Button('Get Started', style={'background-color': '#007BFF', 'color': '#ffffff'}),
                 href='/dashboard')
    ])
])
