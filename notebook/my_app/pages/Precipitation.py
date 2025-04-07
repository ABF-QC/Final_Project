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

#----------------------------
# Define variables
#----------------------------
pcpn =  'Total Precip (mm)'

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
st.markdown(f"<h1 style='text-align: center;'>Daily Total Precipitation for {stn} from {start_wx.year} to {end_wx.year}</h1>",
            unsafe_allow_html=True)

#----------------------------
# Add text
#----------------------------
text=f"Past and future mean global concentration for carbon dioxide (CO2) and methane (CH4),\
       even though there are more greenhouse gases contributing to climate change than these \
       two, will be shown through the help of a timeseries graph.</br></br> With the help of these graph, \
       we will be able to access past and future evolution of each greenhouse gas through time.</br></br>"

st.write(f"<p style='text-align: left;'></br></br>{text}</p>", unsafe_allow_html=True)

#----------------------------
# Create Tmin plot 
#----------------------------
# Create graph
fig3 = go.Figure()

# Add the scatter plot
fig3.add_trace(go.Scatter(x=wx_df.index, y=wx_df[pcpn], name='Observation',
               mode='markers'))

# Add Precipitation = 75 mm line 
fig3.add_shape(type='line', x0=wx_df.index.min(),
              x1=wx_df.index.max(), y0=100, y1=100,
              line=dict(color='darkred', width=1, dash='dash'),
              name="Precipitation = 100 mm",  
              showlegend=True)

# Add Precipitation = 75 mm line 
fig3.add_shape(type='line', x0=wx_df.index.min(),
              x1=wx_df.index.max(), y0=75, y1=75,
              line=dict(color='red', width=1, dash='dash'),
              name="Precipitation = 75 mm",  
              showlegend=True)

# Add Precipitation = 50 mm line 
fig3.add_shape(type='line', x0=wx_df.index.min(),
              x1=wx_df.index.max(), y0=50, y1=50,
              line=dict(color='lightsalmon', width=2, dash='dash'),
              name="Precipitation = 50 mm",  
              showlegend=True)

# Add markers and lines
fig3.update_traces(
     mode='markers', 
     marker=dict(size=3, color='darkgrey'),
     showlegend = True,
     hovertemplate='<b>Date</b>: %{x}<br>' +
                   '<b>Precipitation (mm)</b>: %{y}<extra></extra>')

# Update layout with title and axis ranges
fig3.update_layout(title={'text': 'Daily Minimum Temperature Over The Years',  
                          'x': 0.5,  
                          'xanchor': 'center'},
                   title_font=dict(size=20, family='Arial'),
                   xaxis_title='Date',  
                   yaxis_title='Total Precipitation (mm) ')


# Display the interactive plot in Streamlit
st.plotly_chart(fig3, use_container_width=True)

#----------------------------
# Create Event Frequency section (menu and plot)
#----------------------------
# Define type of events to choose from
events = ['Daily Total Precipitation higher than 100 mm ',
          'Daily Total Precipitation higher than 75 mm ',
          'Daily Total Precipitation higher than 50 mm ',
          'Daily Total Precipitation higher than 25 mm ']

# Split section into columns
col1, col2, col3 = st.columns(3)

# Add selectbox in the first column
with col1:
    text=f"Select the weather event:"

    st.write(f"<h5 style='text-align: left;'></br></br>{text}</h5>", unsafe_allow_html=True)
    
    event = st.selectbox('', options=events, index=1, label_visibility="collapsed")

with col2:
    pass

# Filter the weather dataset based on the chosen event
if event == events[0] :
    tmp = wx_df.groupby('Year').agg(Count=(pcpn, lambda x: (x > 100.).sum()))
    tmp = tmp.rename(columns={'Station':'Count'}).reset_index()
elif event == events[1]:
    tmp = wx_df.groupby('Year').agg(Count=(pcpn, lambda x: (x > 75.).sum()))
    tmp = tmp.rename(columns={'Station':'Count'}).reset_index()
elif event == events[2]:
    tmp = wx_df.groupby('Year').agg(Count=(pcpn, lambda x: (x > 50.).sum()))
    tmp = tmp.rename(columns={'Station':'Count'}).reset_index()
elif event == events[3]:
    tmp = wx_df.groupby('Year').agg(Count=(pcpn, lambda x: (x > 25.).sum()))
    tmp = tmp.rename(columns={'Station':'Count'}).reset_index()
else :
    pass

#----------------------------
# Create event frequency plot 
#----------------------------
# Create graph
fig = go.Figure()

# Add bar plot
fig.add_trace(go.Bar(x=tmp['Year'], 
                     y=tmp['Count'],
                     name='Rain Events',
                     hovertemplate='<b>Year</b>: %{x}<br>' +
                                   '<b># of events</b>: %{y}<extra></extra>'))

# Adjust/set title and axis
fig.update_layout(title={'text': f'Frequency of {event} over the Years',  
                          'x': 0.5,  
                          'xanchor': 'center'},
                   title_font=dict(size=20, family='Arial'),
                   xaxis_title='Date',  
                   yaxis_title='# of events',
                   yaxis=dict(range=[0, tmp['Count'].max()]),
                   xaxis=dict(range=[wx_df.index.year.min()-2, wx_df.index.year.max()+2]))

# Display the interactive plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

#----------------------------
# Add Sources
#----------------------------
st.markdown("""
Sources:
  - [Past data](https://dd.weather.gc.ca/climate/observations/)
  - [Predicted data](https://github.com/ABF-QC/Final_Project)
""")

st.write(f"<p style='text-align: left;'></br></br></p>", unsafe_allow_html=True)