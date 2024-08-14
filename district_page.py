import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Load data
with open('karnataka.json', 'r') as f:
    geojson = json.load(f)

df = pd.read_csv('water_data5.csv')

# Define color options for the dropdown
color_options = ['cl', 'k', 'ph_gen', 'Level (m)']

# Define the starting page layout
start_page_layout = st.button('Get Started')

# Main app layout
def main_app_layout():
    st.title("Groundwater Analysis")

    selected_color = st.selectbox("Select Color:", color_options, index=0)

    year_slider = st.slider("Select Year:", min_value=2018, max_value=2020, value=2018, step=1)

    # Filter data based on selected year
    filtered_df = df[df['Date Collection'] == year_slider]

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

    st.plotly_chart(fig_choropleth)
    st.plotly_chart(fig_scatter)

# Display starting page or main app layout based on button click
if start_page_layout:
    st.title("Welcome to Groundwater Analysis")
else:
    main_app_layout()
