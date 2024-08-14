# app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from pages import landing_page, dashboard_page

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dashboard':
        return dashboard_page.layout
    else:
        return landing_page.layout

if __name__ == '__main__':
    app.run_server(debug=True)
