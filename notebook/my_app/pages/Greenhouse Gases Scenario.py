#----------------------------
# Import libraries
#----------------------------
import os
import streamlit as st
import pandas as pd
#import numpy as np
#import seaborn as sns
#import matplotlib.pyplot as plt
#import plotly.express as px
import plotly.graph_objs as go

#----------------------------
# Adjust page config
#----------------------------
st.set_page_config(layout="wide")

#----------------------------
# Define paths and filenames
#----------------------------
data_dir = 'data/'

ghg = 'GreenHouse_Gases/processed/'

files = {'co2_file_weak' : 'co2_1850-2099_SSP4_34.csv', 
         'ch4_file_weak' : 'ch4_1850-2099_SSP4_34.csv',
         'co2_file_mod' : 'co2_1850-2099_SSP2_45.csv',
         'ch4_file_mod' : 'ch4_1850-2099_SSP2_45.csv',
         'co2_file_high' : 'co2_1850-2099_SSP4_60.csv',
         'ch4_file_high' : 'ch4_1850-2099_SSP4_60.csv',
         'co2_file_xtrm' : 'co2_1850-2099_SSP5_85.csv',
         'ch4_file_xtrm' : 'ch4_1850-2099_SSP5_85.csv'
         }

#----------------------------
# Define variables
#----------------------------
scenario = {'weak':'SSP4-34', 
            'mod':'SSP2-45',
            'high':'SSP4-60',
            'xtrm':'SSP5-80'}

color_scenario = {'weak':'green', 
                  'mod':'orange',
                  'high':'red',
                  'xtrm':'darkred'}

text_scenario = {'SSP4-34' : 'Intermediate GHG emissions with a desire to implement climate policies', 
                 'SSP2-45' : 'Low to intermediate GHG emissions with large social disparities',
                 'SSP4-60' : 'Intermediate to high GHG emissions with deep social inequalities',
                 'SSP5-80' : 'Very high GHG emissions (worst case scenario)'}

#----------------------------
# Read data files
#----------------------------
for idx,sc in enumerate(scenario):
    tmp_sc = scenario[sc].replace('-', '_')

    for gas in ['co2', 'ch4']:
        file = gas+'_file_'+ sc
        if idx == 0 :
            if gas == 'co2':
                co2_df = pd.read_csv(os.path.join(data_dir, ghg, files[file]), index_col=0, parse_dates=True)
                co2_df.drop(columns = 'Data Source', inplace=True)
                co2_df.rename(columns={'CO2':sc}, inplace=True)
            elif gas == 'ch4':              
                ch4_df = pd.read_csv(os.path.join(data_dir, ghg, files[file]), index_col=0, parse_dates=True)
                ch4_df.rename(columns={'CH4':sc}, inplace=True)
            else :
                print('Error: Gas in not co2 or ch4')
        else :
            if gas == 'co2':
                tmp = pd.read_csv(os.path.join(data_dir, ghg, files[file]), index_col=0, parse_dates=True)
                tmp.drop(columns = 'Data Source', inplace=True)
                tmp.rename(columns={'CO2':sc}, inplace=True)
                co2_df = pd.concat([co2_df, tmp], axis=1)
            elif gas == 'ch4':
                tmp = pd.read_csv(os.path.join(data_dir, ghg, files[file]), index_col=0, parse_dates=True)
                tmp.rename(columns={'CH4':sc}, inplace=True)
                ch4_df = pd.concat([ch4_df, tmp], axis=1)
            else :
                print('Error: Gas in not co2 or ch4')


#----------------------------
# Define page's title 
#----------------------------
# Title and description
st.markdown(f"<h1 style='text-align: center;'>Greenhouse Gases Past and Futur</h1>",
            unsafe_allow_html=True)

#----------------------------
# Add text
#----------------------------
text=f"Past and future mean global concentration for carbon dioxide (CO2) and methane (CH4),\
       even though there are more greenhouse gases (GHG) contributing to climate change than these \
       two, will be shown through the help of a timeseries graph.</br></br> With the help of these graph, \
       we will be able to access past and future evolution of each GHG through \
       time.</br></br> The forecast of the GHG are based from the Shared Socioeconomic Pathways (SSPs), \
       which are climate change scenarios of projected socioeconomic global changes up to 2100 as defined in the \
       IPCC Sixth Assessment Report on climate change in 2021. They are used to derive GHG emissions \
       scenarios with different climate policies."

st.write(f"<p style='text-align: left;'></br></br>{text}</p>", unsafe_allow_html=True)

table = pd.DataFrame(list(text_scenario.items()), columns=['SSP', 'Scenario']).set_index('SSP')

st.table(table)

#----------------------------
# Create Greenhouse gases plot (CO2)
#----------------------------
co2_df['Year'] = co2_df.index.year
co2_df = co2_df.astype(int)

# Create graph
fig4 = go.Figure()

# Add the scatter plot 
fig4.add_trace(go.Scatter(x=co2_df[co2_df['Year'] < 2025]['Year'],
                          y=co2_df[co2_df['Year'] < 2025]['weak'],
                          mode='lines',
                          name='Observation',
                          line=dict(color='darkgrey'),
                          hovertemplate='<b>Year</b>: %{x}<br>' +
                                        '<b>CO2 (ppm)</b>: %{y}<extra></extra>'))

# Add the 4 scenario predictions
for sc in scenario :
    tmp_sc = scenario[sc].replace('-', '_')
    fig4.add_trace(go.Scatter(x=co2_df[co2_df['Year'] >= 2025]['Year'],
                              y=co2_df[co2_df['Year'] >= 2025][sc],
                              mode='lines',
                              name=f'Forecast ({tmp_sc})',
                              line=dict(color=color_scenario[sc], 
                                        dash='dash'),
                              hovertemplate='<b>Year</b>: %{x}<br>' +
                                            '<b>CO2 (ppm)</b>: %{y}<extra></extra>'))



# Update layout with title and axis ranges
fig4.update_layout(title={'text': 'Carbon Dioxide Global mean Concentration (ppm) over the Years',  
                          'x': 0.5,  
                          'xanchor': 'center', 
                          #'y': 0.95,  # Adjust the vertical position (optional)
                          #'yanchor': 'top'  # Anchor the title at the top of the plot area
                         },
                   title_font=dict(size=20, family='Arial'),
                   xaxis_title='Year',  
                   yaxis_title='CO2 Concentration (ppm)')

# Display the interactive plot in Streamlit
st.plotly_chart(fig4, use_container_width=True)

#----------------------------
# Create Greenhouse gases plot (CH4)
#----------------------------
ch4_df['Year'] = ch4_df.index.year
ch4_df = ch4_df.astype(int)

# Create graph
fig4 = go.Figure()

# Add the scatter plot 
fig4.add_trace(go.Scatter(x=ch4_df[ch4_df['Year'] < 2025]['Year'],
                          y=ch4_df[ch4_df['Year'] < 2025]['weak'],
                          mode='lines',
                          name='Observation',
                          line=dict(color='darkgrey'),
                          hovertemplate='<b>Year</b>: %{x}<br>' +
                                        '<b>CH4 (ppb)</b>: %{y}<extra></extra>'))

# Add the 4 scenario predictions
for sc in scenario :
    tmp_sc = scenario[sc].replace('-', '_')
    fig4.add_trace(go.Scatter(x=ch4_df[ch4_df['Year'] >= 2025]['Year'],
                              y=ch4_df[ch4_df['Year'] >= 2025][sc],
                              mode='lines',
                              name=f'Forecast ({tmp_sc})',
                              line=dict(color=color_scenario[sc], 
                                        dash='dash'),
                              hovertemplate='<b>Year</b>: %{x}<br>' +
                                            '<b>CH4 (ppb)</b>: %{y}<extra></extra>' ))



# Update layout with title and axis ranges
fig4.update_layout(title={'text': 'Methane Global mean Concentration (ppb) over the Years',  
                          'x': 0.5,  
                          'xanchor': 'center', 
                          #'y': 0.95,  # Adjust the vertical position (optional)
                          #'yanchor': 'top'  # Anchor the title at the top of the plot area
                         },
                   title_font=dict(size=20, family='Arial'),
                   xaxis_title='Year',  
                   yaxis_title='CH4 Concentration (ppb)')

# Display the interactive plot in Streamlit
st.plotly_chart(fig4, use_container_width=True)

#----------------------------
# Add Sources
#----------------------------
st.markdown("""
Sources:
- [Carbon dioxide (C02) Past data (1850-2011)](https://data.giss.nasa.gov/modelforce/ghgases/Fig1A.ext.txt)
- [Carbon dioxide (C02) Past data (1959-2024)](https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_mlo.txt)
- [Methane (CH4) Past data (1010-1992)](https://sealevel.info/EthCH498B.txt)
- [Methane(CH4) Past data (1884-2023)](https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_annmean_gl.txt)
- [Carbon dioxide (C02) and Methane (CH4) Predicted data](https://greenhousegases.science.unimelb.edu.au/#!/view)
""")

st.write(f"<p style='text-align: left;'></br></br></p>", unsafe_allow_html=True)

