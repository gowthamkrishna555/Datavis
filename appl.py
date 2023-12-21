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
st.set_page_config(layout="wide", page_title="Groundwater Analysis", page_icon=":chart_with_upwards_trend:")

# Define the starting page layout
if not st.session_state.get('started', False):
    st.title("Welcome to Groundwater Analysis")
    if st.button('Get Started'):
        st.session_state.started = True
else:
    st.title("Groundwater Analysis")

    # Hide the "Get Started" button on the next page
    st.session_state.started = True

    selected_color = st.selectbox("Select Color:", color_options, index=0)

    year_slider = st.slider("Select Year:", min_value=2018, max_value=2020, value=2018, step=1)

    # Filter data based on selected year
    filtered_df = df[df['Date Collection'] == year_slider]

    # Handle NaN values in 'ca' column
    filtered_df['ca'].fillna(0, inplace=True)  # You can replace NaN with 0 or any other value

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

    # Update scatter plot to show Karnataka map
    fig_scatter = px.scatter_geo(df,
                                 lat=df['Latitude'],
                                 lon=df['Longitude'],
                                 scope='asia',
                                 template='plotly',
                                 color=selected_color,
                                 hover_data=['Station Name', 'Agency Name', 'District', selected_color])
    fig_scatter.update_geos(fitbounds="locations", visible=False)

    # Display choropleth map
    st.plotly_chart(fig_choropleth)

    # Display scatter plot
    scatter_chart = st.plotly_chart(fig_scatter)

    # Additional Plots
    for additional_color in color_options:
        if additional_color == selected_color:
            # Line Plot with more data
            fig_line = px.line(filtered_df, x='Date Collection', y=[selected_color, 'ca', 'mg', 'k'],
                              color='District', labels={'variable': 'Parameter', 'value': 'Value'},
                              title=f"{selected_color.capitalize()} and Other Parameters Over Time")
            st.plotly_chart(fig_line)

            # Bar Chart
            fig_bar = px.bar(filtered_df, x='District', y=selected_color)
            st.plotly_chart(fig_bar)

            # Histogram
            fig_hist = px.histogram(filtered_df, x=selected_color, y='District', nbins=30)
            st.plotly_chart(fig_hist)

            # Bubble Plot
            fig_bubble = px.scatter(filtered_df, x='Longitude', y='Latitude', size='ca', color='District')
            st.plotly_chart(fig_bubble)

            # 3D Scatter Plot
            fig_3d = px.scatter_3d(filtered_df, x='k', y='ph_gen', z=selected_color, color='District')
            st.plotly_chart(fig_3d)
