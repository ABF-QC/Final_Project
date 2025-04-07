#----------------------------
# Import libraries
#----------------------------
import os
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go

#----------------------------
# Adjust page config
#----------------------------
st.set_page_config(layout="wide")

#----------------------------
# Define paths and filenames
#----------------------------
data_dir = '../../data/'

population_file = 'Population/processed/Montreal.csv'

#----------------------------
# Read data files
#----------------------------
pop_df = pd.read_csv(os.path.join(data_dir, population_file), index_col=0, parse_dates=True)

#----------------------------
# Define page's title 
#----------------------------
# Title and description
st.markdown(f"<h1 style='text-align: center;'> Montreal's Population Past and Futur</h1>",
            unsafe_allow_html=True)

#----------------------------
# Add text
#----------------------------
text=f"Population density significantly impact the land surface of a city. \
    The surface type consequently influence the surface albedo, \
    its capacity to retain moisture, and so much more. \
    When to population is dense enough and has change the surface type from vegetation to \
    a dense building surface area, the urban heat island effect is created over the urban area. \
    It means that the urban area accumulate heat more than its surroundings rural area and, consequently, \
    the maximum temperature and minimum temperature will frequently be warmer in the urban area \
    than in the surroundings rural area. </br></br> Here we can have a look at the past and\
    predicted data for Montreal's population.</br></br>"

st.write(f"<p style='text-align: left;'></br></br>{text}</p>", unsafe_allow_html=True)

#----------------------------
# Create Greenhouse gases plot (CO2)
#----------------------------
pop_df['Year'] = pop_df.index.year
pop_df = pop_df.astype(int)

# Create graph
fig4 = go.Figure()

# Add the scatter plot 
fig4.add_trace(go.Scatter(x=pop_df[pop_df['Year'] < 2022]['Year'],
                          y=pop_df[pop_df['Year'] < 2022]['Population'],
                          mode='lines',
                          name='Observation',
                          line=dict(color='darkgrey'),
                          hovertemplate='<b>Year</b>: %{x}<br>' +
                                        '<b>Population </b>: %{y}<extra></extra>'))

# Add the prediction
fig4.add_trace(go.Scatter(x=pop_df[pop_df['Year'] >= 2022]['Year'],
                          y=pop_df[pop_df['Year'] >= 2022]['Population'],
                          mode='lines',
                          name=f'Forecast',
                          line=dict(color='red', 
                                    dash='dash'),
                          hovertemplate='<b>Year</b>: %{x}<br>' +
                                        '<b>CO2 (ppm)</b>: %{y:.3s}<extra></extra>'))



# Update layout with title and axis ranges
fig4.update_layout(title={'text': "Montreal's Population over the Years",  
                          'x': 0.5,  
                          'xanchor': 'center', 
                          #'y': 0.95,  # Adjust the vertical position (optional)
                          #'yanchor': 'top'  # Anchor the title at the top of the plot area
                         },
                   title_font=dict(size=20, family='Arial'),
                   xaxis_title='Year',  
                   yaxis_title='Population',
                   yaxis=dict(tickformat=".3s"))

# Display the interactive plot in Streamlit
st.plotly_chart(fig4, use_container_width=True)