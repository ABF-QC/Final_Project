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
Tmax = 'Max Temp (°C)'

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
# Create Tmax plot 
#----------------------------
# Create graph
fig3 = go.Figure()

# Add the scatter plot
fig3.add_trace(go.Scatter(x=wx_df.index, y=wx_df[Tmax], name='Observation',
               mode='markers'))

# Add Temperature = 30 °C line 
fig3.add_shape(type='line', x0=wx_df.index.min(),
              x1=wx_df.index.max(), y0=30, y1=30,
              line=dict(color='red', width=1, dash='dash'),
              name="Temperature = 30 °C",  
              showlegend=True)

# Add Temperature = 0 °C line 
fig3.add_shape(type='line', x0=wx_df.index.min(),
              x1=wx_df.index.max(), y0=0, y1=0,
              line=dict(color='dodgerblue', width=1, dash='dash'),
              name="Temperature = 0 °C",  
              showlegend=True)

# Add Temperature = -20 °C line 
fig3.add_shape(type='line', x0=wx_df.index.min(),
              x1=wx_df.index.max(), y0=-20, y1=-20,
              line=dict(color='blue', width=1, dash='dash'),
              name="Temperature = -20 °C",  
              showlegend=True)

# Add markers and lines
fig3.update_traces(
     mode='markers', 
     marker=dict(size=3, color='darkgrey'),
     showlegend = True,
     hovertemplate='<b>Date</b>: %{x}<br>' +
                   '<b>Max Temperature (°C)</b>: %{y}<extra></extra>')

# Update layout with title and axis ranges
fig3.update_layout(title={'text': 'Daily Maximum Temperature Over The Years',  
                          'x': 0.5,  
                          'xanchor': 'center'},
                   title_font=dict(size=20, family='Arial'),
                   xaxis_title='Date',  
                   yaxis_title='Max. Temperature (°C ) ')


# Display the interactive plot in Streamlit
st.plotly_chart(fig3, use_container_width=True)

# chart = alt.Chart(tmp).mark_line().encode(
#     x='Year:O',
#     y=alt.Y('Station:Q', scale=alt.Scale(domain=[ tmp['Station'].min(), tmp['Station'].max() + 1]))  # Adjust min here
# ).properties(
#     width=700,
#     height=400
# )

# st.altair_chart(chart, use_container_width=True)
# Viz 1: Survival countplot
# st.subheader("Survival Count")
# survival_count = filtered_df['survived'].value_counts()
# st.line_chart(tmp['Station'])
# #st.bar_chart(survival_count.rename(index={0: 'Did not survive', 1: 'Survived'}))

# # Viz 2: Survival by gender
# st.subheader("Survival Rate by Gender")

# gender_survival = filtered_df.groupby('sex')['survived'].mean().reset_index()

# fig = px.pie(
#     gender_survival,
#     names='sex',
#     values='survived',
#     title="Survival Rate by Gender",
# )

# # Display the pie chart
# st.plotly_chart(fig)

# Viz 3: Age distribution
# Prepare data for histogram
#age_bins = pd.cut(filtered_df['age'].dropna(), bins=20)  # Create 20 bins for ages
#hist_data = age_bins.value_counts(sort=False)  # Count ages in each bin

# Convert to DataFrame for plotting
#hist_df = pd.DataFrame({
#    'Age Range': [f"{int(bin.left)}-{int(bin.right)}" for bin in hist_data.index],  # Bin ranges as labels
#    'Count': hist_data.values
#})

# Display histogram using Streamlit
#st.bar_chart(hist_df.set_index('Age Range'))



# tmp = wx_df[wx_df['Total Precip (mm)'] > 75.].groupby('Year').count()
# tmp = tmp.rename(columns={'Station':'Count'}).reset_index()
# #tmp['Year'] = pd.to_datetime(tmp['Year'], format='%Y')
# #tmp.set_index('Year', inplace=True)
# #st.write(tmp)

# fig = go.Figure()
# fig.add_trace(go.Bar(x=tmp['Year'], 
#                      y=tmp['Count'],
#                      name='Rain Events',
#                      hovertemplate='<b>Year</b>: %{x}<br>' +
#                                    '<b># of events</b>: %{y}<extra></extra>'))

# fig.update_layout(
#      yaxis=dict(range=[0, tmp['Count'].max()],
#                 tickmode='linear',     
#                 dtick=1),
#      #xaxis=dict(range=[tmp.index.min(), tmp.index.max()],
#      #           tickmode='linear',     
#      #           dtick=1),
#      title="Quantity of daily rain event > 75 mm per year"
# )

# st.plotly_chart(fig, use_container_width=True)

#st.bar_chart(tmp['Station'])


#----------------------------
# Add Sources
#----------------------------
st.markdown("""
Sources:
  - [Past data](https://dd.weather.gc.ca/climate/observations/)
  - [Predicted data](https://github.com/ABF-QC/Final_Project)
""")

st.write(f"<p style='text-align: left;'></br></br></p>", unsafe_allow_html=True)