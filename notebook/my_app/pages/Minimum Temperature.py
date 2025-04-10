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

climate_file = 'ECCC/processed/daily/daily_processed.csv'

forecast_dir = os.path.join(data_dir, 'Forecast')

files = {'weak' : 'Temperature_SSP4-34entire', 
         'mod' : 'Temperature_SSP2-45entire',
         'high' : 'Temperature_SSP4-60entire',
         'xtrm' : 'Temperature_SSP5-85entire',
         }

scenario = {'weak':'SSP4-34', 
            'mod':'SSP2-45',
            'high':'SSP4-60',
            'xtrm':'SSP5-80'
            }

color_scenario = {'weak':'green', 
                  'mod':'orange',
                  'high':'red',
                  'xtrm':'darkred'}

#----------------------------
# Define variables
#----------------------------
Tmin =  'Min Temp (°C)'
Tmax = 'Max Temp (°C)'

#----------------------------
# Read data files
#----------------------------
wx_df = pd.read_csv(os.path.join(data_dir, climate_file), index_col=0, parse_dates=True)

for idx,sc in enumerate(scenario):

    file = files[sc]

    if idx == 0 :
        fcst_df = pd.read_csv(os.path.join(forecast_dir, file), index_col=0, parse_dates=True)
        fcst_df.rename(columns={Tmin+'model':sc}, inplace=True)
        fcst_df.drop(columns=[Tmax+'model'], inplace=True)
    else :
        tmp = pd.read_csv(os.path.join(forecast_dir, file), index_col=0, parse_dates=True)
        tmp.rename(columns={Tmin+'model':sc}, inplace=True)       
        tmp.drop(columns=[Tmax+'model'], inplace=True)
        fcst_df = pd.concat([fcst_df, tmp], axis=1)


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
st.markdown(f"<h1 style='text-align: center;'>Daily Minimum Temperature for {stn} from {start_wx.year} to {end_wx.year}</h1>",
            unsafe_allow_html=True)

#----------------------------
# Add text
#----------------------------
text=f"At first, this page will allow you to navigate through the history of \
       minimum temperature of downtown Montreal spanning more than a century.\
       </br></br> Minimum temperature are quite important, since they can have \
       a significant impact on someone health and safety. During a heat wave, night time temperature above 20 °C\
       greatly limits the opportunities to cool down and recover from the day's heat.\
       Which means that the heat stress on the body remains high even at nighttime \
       leading to a greater health risk over consecutive days of such heat stress.\
       At the other end of the spectrum, minimum \
       temperature lower than -30 °C can lead to a frostbite on exposed skin in a few minutes \
       and is a major health hazard for vulnerable communities.</br></br> \
       The second portion of the page will allow you to explore the yearly frequency \
       of some weather events regarding the minimum temperature and see their evolution\
       over the last century.</br></br> Finally, the last portion of the page will give\
       you an insight of what minimum temperature could look like over the next 50 years\
       given various greenhouse gases scenario from the Shared Socioeconomic Pathways (SSPs)\
       of the IPCC Sixth Assessment Report on climate change of 2021.</br></br>\
       "

st.write(f"<p style='text-align: left;'></br></br>{text}</p>", unsafe_allow_html=True)

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

# Add Temperature = 0 °C line 
fig3.add_shape(type='line', x0=wx_df.index.min(),
              x1=wx_df.index.max(), y0=0, y1=0,
              line=dict(color='dodgerblue', width=1, dash='dash'),
              name="Temperature = 0 °C",  
              showlegend=True)

# Add Temperature = -20 °C line 
fig3.add_shape(type='line', x0=wx_df.index.min(),
              x1=wx_df.index.max(), y0=-30, y1=-30,
              line=dict(color='blue', width=1, dash='dash'),
              name="Temperature = -30 °C",  
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

#----------------------------
# Create Event Frequency section (menu and plot)
#----------------------------
# Define type of events to choose from
events = ['Daily Minimum Temperature higher than 25 °C ',
          'Daily Minimum Temperature higher than 20 °C ',
          'Daily Minimum Temperature higher than 15 °C ',
          'Daily Minimum Temperature higher than 0 °C ',
          'Daily Minimum Temperature lower than -20 °C ',
          'Daily Minimum Temperature lower than -30 °C '
          ]

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
    tmp = wx_df.groupby('Year').agg(Count=(Tmin, lambda x: (x > 25.).sum()))
    tmp = tmp.rename(columns={'Station':'Count'}).reset_index()
elif event == events[1]:
    tmp = wx_df.groupby('Year').agg(Count=(Tmin, lambda x: (x > 20.).sum()))
    tmp = tmp.rename(columns={'Station':'Count'}).reset_index()
elif event == events[2]:
    tmp = wx_df.groupby('Year').agg(Count=(Tmin, lambda x: (x > 15.).sum()))
    tmp = tmp.rename(columns={'Station':'Count'}).reset_index()
elif event == events[3]:
    tmp = wx_df.groupby('Year').agg(Count=(Tmin, lambda x: (x > 0.).sum()))
    tmp = tmp.rename(columns={'Station':'Count'}).reset_index()
elif event == events[4]:
    tmp = wx_df.groupby('Year').agg(Count=(Tmin, lambda x: (x < -20.).sum()))
    tmp = tmp.rename(columns={'Station':'Count'}).reset_index()
elif event == events[5]:
    tmp = wx_df.groupby('Year').agg(Count=(Tmin, lambda x: (x < -30.).sum()))
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
                   yaxis=dict(range=[tmp['Count'].min(), tmp['Count'].max()]),
                   xaxis=dict(range=[wx_df.index.year.min()-2, wx_df.index.year.max()+2]))

# Display the interactive plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

#----------------------------
# Create Tmin fcst plot 
#----------------------------
# Create graph
fig3 = go.Figure()

for sc in reversed(list(scenario.keys())):

    # Add the scatter plot
    fig3.add_trace(go.Scatter(x=fcst_df.index,
                              y=fcst_df[sc], 
                              name='Forecast'+f' ({scenario[sc]})',
                              mode='lines',
                              line=dict(color=color_scenario[sc]),
                              opacity=0.6))

# Add markers and lines
fig3.update_traces(
     showlegend = True,
     hovertemplate='<b>Date</b>: %{x}<br>' +
                   '<b>Min Temperature (°C)</b>: %{y}<extra></extra>')

# Update layout with title and axis ranges
fig3.update_layout(title={'text': 'Daily Minimum Temperature Forecast by Recurrent Neural Network (RNN)',  
                          'x': 0.5,  
                          'xanchor': 'center'},
                   title_font=dict(size=20, family='Arial'),
                   xaxis_title='Date',  
                   yaxis_title='Min. Temperature (°C ) ')


# Display the interactive plot in Streamlit
st.plotly_chart(fig3, use_container_width=True)

#----------------------------
# Create Tmin fcst plot summer
#----------------------------
# Create graph
fig3 = go.Figure()

fcst_df['Year'] = fcst_df.index.year
tmp = fcst_df.groupby('Year').max()

for sc in reversed(list(scenario.keys())):

    # Add the scatter plot
    fig3.add_trace(go.Scatter(x=tmp.index,
                              y=tmp[sc], 
                              name='Forecast'+f' ({scenario[sc]})',
                              mode='lines',
                              line=dict(color=color_scenario[sc]),
                              opacity=0.6))

# Add markers and lines
fig3.update_traces(
     showlegend = True,
     hovertemplate='<b>Date</b>: %{x}<br>' +
                   '<b>Min Temperature (°C)</b>: %{y:.2f}<extra></extra>')

# Update layout with title and axis ranges
fig3.update_layout(title={'text': 'Yearly highest Minimum Temperature Forecast by Recurrent Neural Network (RNN)',  
                          'x': 0.5,  
                          'xanchor': 'center'},
                   title_font=dict(size=20, family='Arial'),
                   xaxis_title='Date',  
                   yaxis_title='Min. Temperature (°C ) ')


# Display the interactive plot in Streamlit
st.plotly_chart(fig3, use_container_width=True)

#----------------------------
# Create Tmin fcst plot winter
#----------------------------
# Create graph
fig3 = go.Figure()

fcst_df['Year'] = fcst_df.index.year
tmp = fcst_df.groupby('Year').min()

for sc in reversed(list(scenario.keys())):

    # Add the scatter plot
    fig3.add_trace(go.Scatter(x=tmp.index,
                              y=tmp[sc], 
                              name='Forecast'+f' ({scenario[sc]})',
                              mode='lines',
                              line=dict(color=color_scenario[sc]),
                              opacity=0.6))

# Add markers and lines
fig3.update_traces(
     showlegend = True,
     hovertemplate='<b>Date</b>: %{x}<br>' +
                   '<b>Min Temperature (°C)</b>: %{y:.2f}<extra></extra>')

# Update layout with title and axis ranges
fig3.update_layout(title={'text': 'Yearly lowest Minimum Temperature Forecast by Recurrent Neural Network (RNN)',  
                          'x': 0.5,  
                          'xanchor': 'center'},
                   title_font=dict(size=20, family='Arial'),
                   xaxis_title='Date',  
                   yaxis_title='Min. Temperature (°C ) ')


# Display the interactive plot in Streamlit
st.plotly_chart(fig3, use_container_width=True)

#----------------------------
# Add Sources
#----------------------------
st.markdown("""
Sources:
  - [Past data](https://dd.weather.gc.ca/climate/observations/)
  - [Predicted data](https://github.com/ABF-QC/Final_Project)
""")

st.write(f"<p style='text-align: left;'></br></br></p>", unsafe_allow_html=True)