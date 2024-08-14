import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import json
import os

# Load data
with open('D:\data visulization\karnataka.json', 'r') as f:
    geojson = json.load(f)
df = pd.read_csv('D:\data visulization\water_data5.csv')

app = dash.Dash(__name__, assets_folder=os.path.join(os.getcwd(), 'assets'))

# Define color options for the dropdown
color_options = ['cl', 'k', 'ph_gen', 'Level (m)']

app.layout = html.Div([
    html.H1("Groundwater Analysis", style={'textAlign': 'center', 'color': 'blue'}),
    dcc.Dropdown(
        id='color-dropdown',
        options=[{'label': col, 'value': col} for col in color_options],
        value='cl',
        style={'width': '50%', 'margin': '0 auto'}
    ),
    dcc.Slider(
        id='year-slider',
        min=2018,
        max=2020,
        value=2018,
        marks={str(year): str(year) for year in range(2018, 2021)},
        step=None
    ),
    dcc.Graph(id='choropleth', clickData=None, style={'height': '70vh', 'width': '80vw', 'padding': '40px'}),
    html.Br(),
    dcc.Graph(id='scatter_geo', clickData=None, style={'height': '70vh', 'width': '80vw', 'padding': '40px'}),
    html.Br(),
    dcc.Markdown(id='click-data', children="Click on a point in the scatter plot to see more details.", style={'color': 'red'})
])

@app.callback(
    [Output('choropleth', 'figure'),
     Output('scatter_geo', 'figure')],
    [Input('year-slider', 'value'),
     Input('color-dropdown', 'value')]
)
def update_visualizations(selected_year, selected_color):
    filtered_df = df[df['Date Collection'] == selected_year]
    app.selected_color = selected_color  # Store selected color in the app instance

    # Update choropleth map
    fig_choropleth = px.choropleth_mapbox(filtered_df,
                                          geojson=geojson,
                                          locations='District',
                                          color=selected_color,
                                          featureidkey="properties.district",
                                          center={"lat": filtered_df['Latitude'].mean(), "lon": filtered_df['Longitude'].mean()},
                                          mapbox_style="carto-positron",
                                          zoom=5,
                                          hover_data=['Station Name', 'Agency Name', 'District', selected_color])
    fig_choropleth.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    # Update scatter plot
    fig_scatter = px.scatter_geo(filtered_df,
                                 lat='Latitude',
                                 lon='Longitude',
                                 color=selected_color,
                                 hover_data=['Station Name', 'Agency Name', 'District', selected_color])
    fig_scatter.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig_choropleth, fig_scatter

@app.callback(
    Output('click-data', 'children'),
    [Input('scatter_geo', 'clickData'),
     Input('year-slider', 'value')]
)
def display_click_data(clickData, selected_year):
    if clickData is None:
        return "Click on a point in the scatter plot to see more details."
    else:
        # Get the index of the clicked point
        point_index = clickData['points'][0]['pointIndex']
        # Filter the dataframe for the selected year
        filtered_df = df[df['Date Collection'] == selected_year]
        # Get the data of the clicked point
        point_data = filtered_df.iloc[point_index]
        selected_color = app.selected_color  # Retrieve selected color from the app instance
        # Create a custom hover data message with NaN handling
        hover_data_message = "\n".join(
            [f"{property_name}: {point_data[property_name]}" if pd.notna(point_data[property_name]) else f"{property_name}: N/A"
             for property_name in ['Station Name', 'Agency Name', 'District', selected_color]]
        )
        return hover_data_message

if __name__ == '__main__':
    app.run_server(debug=True)
