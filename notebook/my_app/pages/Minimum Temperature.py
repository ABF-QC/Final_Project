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

climate_file = 'ECCC/processed/daily/daily_processed.csv'

files = {'co2_file_weak' : 'co2_1850-2099_SSP4_34.csv', 
         'ch4_file_weak' : 'ch4_1850-2099_SSP4_34.csv',
         'co2_file_mod' : 'co2_1850-2099_SSP2_45.csv',
         'ch4_file_mod' : 'ch4_1850-2099_SSP2_45.csv',
         'co2_file_high' : 'co2_1850-2099_SSP4_60.csv',
         'ch4_file_high' : 'ch4_1850-2099_SSP4_60.csv',
         'co2_file_xtrm' : 'co2_1850-2099_SSP5_85.csv',
         'ch4_file_xtrm' : 'ch4_1850-2099_SSP5_85.csv'
         }

scenario = {'weak':'SSP4-34', 
            'mod':'SSP2-45',
            'high':'SSP4-60',
            'xtrm':'SSP5-80'}

color_scenario = {'weak':'green', 
                  'mod':'orange',
                  'high':'red',
                  'xtrm':'darkred'}

#----------------------------
# Define variables
#----------------------------
Tmin =  'Min Temp (°C)'

#----------------------------
# Read data files
#----------------------------
wx_df = pd.read_csv(os.path.join(data_dir, climate_file), index_col=0, parse_dates=True)

#----------------------------
# Remove incomplete start 
# and end year of climate dataset
#----------------------------
tmp = wx_df.groupby(['Year']).count()

start_wx = wx_df.index.min()
end_wx = wx_df.index.max()
print(type(start_wx), end_wx)

for year in [start_wx, end_wx] :

    nbr_days_year = 366 if pd.Period(year, freq='Y').is_leap_year else 365

    yr = int(year.strftime('%Y'))
    nbr_obs_year = tmp[tmp.index == yr]['Station'].values[0]

    print('*',yr, nbr_obs_year, '*')
    
    if nbr_obs_year != nbr_days_year :
        print(f'Not full year. Removing partial {yr} from dataframe')
        wx_df = wx_df[wx_df['Year'] != yr]

        start_wx = wx_df.index.min()
        end_wx = wx_df.index.max()
    else :
        print(f'Full year. Not removing {yr} from obs dataframe.')


#----------------------------
# Define station name
#----------------------------
stn = wx_df['Station'].unique()[0]

#----------------------------
# Define page's title 
#----------------------------
st.markdown(f"<h1 style='text-align: center;'>Daily Maximum Temperature for {stn} from {start_wx.year} to {end_wx.year}</h1>",
            unsafe_allow_html=True)

#----------------------------
# Add text
#----------------------------
text=f"Past and future mean global concentration for carbon dioxide (CO2) and methane (CH4),\
       even though there are more greenhouse gases contributing to climate change than these \
       two, will be shown through the help of a timeseries graph.</br></br> With the help of these graph, \
       we will be able to access past and future evolution of each greenhouse gas through time.</br></br>"

st.write(f"<p style='text-align: left;'></br></br>{text}</p>", unsafe_allow_html=True)


# Show dataset
# if st.checkbox("Show Raw Dataset"):
#     st.write(df)

# Sidebar for user input
# st.sidebar.header("")
# sex_filter = st.sidebar.multiselect("Select Gender", options=df['sex'].unique(), default=df['sex'].unique())
# class_filter = st.sidebar.multiselect("Select Class (Pclass)", options=df['pclass'].unique(), default=df['pclass'].unique())
# embarked_filter = st.sidebar.multiselect("Select Embarkation Point", options=df['embark_town'].dropna().unique(), default=df['embark_town'].unique())

# # Filter dataset based on selections
# filtered_df = df[
#     (df['sex'].isin(sex_filter)) & 
#     (df['pclass'].isin(class_filter)) & 
#     (df['embark_town'].isin(embarked_filter))
# ]


# 



#----------------------------
# Create Tmin plot 
#----------------------------
# Create graph
fig3 = go.Figure()

# Add the scatter plot
fig3.add_trace(go.Scatter(x=wx_df.index, y=wx_df[Tmin], name='Observation',
               mode='markers'))

# Add Temperature = 30 °C line 
fig3.add_shape(type='line', x0=wx_df.index.min(),
              x1=wx_df.index.max(), y0=20, y1=20,
              line=dict(color='red', width=1, dash='dash'),
              name="Temperature = 20 °C",  
              showlegend=True)

# Add Temperature = -20 °C line 
fig3.add_shape(type='line', x0=wx_df.index.min(),
              x1=wx_df.index.max(), y0=-30, y1=-30,
              line=dict(color='blue', width=1, dash='dash'),
              name="Temperature = -30 °C",  
              showlegend=True)

# Add Temperature = 0 °C line 
fig3.add_shape(type='line', x0=wx_df.index.min(),
              x1=wx_df.index.max(), y0=0, y1=0,
              line=dict(color='dodgerblue', width=1, dash='dash'),
              name="Temperature = 0 °C",  
              showlegend=True)

# Add markers and lines
fig3.update_traces(
     mode='markers', 
     marker=dict(size=3, color='darkgrey'),
     showlegend = True,
     hovertemplate='<b>Date</b>: %{x}<br>' +
                   '<b>Min Temperature (°C)</b>: %{y}<extra></extra>')

# Update layout with title and axis ranges
fig3.update_layout(title={'text': 'Daily Minimum Temperature Over The Years',  
                          'x': 0.5,  
                          'xanchor': 'center'},
                   title_font=dict(size=20, family='Arial'),
                   xaxis_title='Date',  
                   yaxis_title='Min. Temperature (°C ) ')


# Display the interactive plot in Streamlit
st.plotly_chart(fig3, use_container_width=True)