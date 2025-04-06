# import streamlit as st

# st.set_page_config(
#     page_title="🛠️ Admin Dashboard",  # <- This becomes the name in the sidebar
#     page_icon="🛠️",
# )

# st.title("🔧 Admin Page")
# st.write("Manage your stations, datasets, and config here.")


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
import altair as alt
import plotly.graph_objs as go
from menu import admin_sidebar

#----------------------------
# Adjust page config
#----------------------------
st.set_page_config(layout="wide")

#----------------------------
# Define paths and filenames
#----------------------------
data_dir = '../data/'
model_dir = '../model/'

ghg = 'GreenHouse_Gases/processed/'

frequency = 'DLY'

climate_file = 'ECCC/processed/daily/daily_processed.csv'

population_file = 'Population/processed/Montreal.csv'

co2_file_weak = 'co2_1850-2099_SSP4_34.csv'
ch4_file_weak = 'ch4_1850-2099_SSP4_34.csv'

co2_file_mod = 'co2_1850-2099_SSP2_45.csv'
ch4_file_mod = 'ch4_1850-2099_SSP2_45.csv'

co2_file_high = 'co2_1850-2099_SSP4_60.csv'
ch4_file_high = 'ch4_1850-2099_SSP4_60.csv'

co2_file_xtrm = 'co2_1850-2099_SSP5_80.csv'
ch4_file_xtrm = 'ch4_1850-2099_SSP5_80.csv'


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
Tmin =  'Min Temp (°C)' 
Tmean = 'Mean Temp (°C)'

cols = ['Max Temp (°C)', 'Max Temp Flag', 'Min Temp (°C)', 'Min Temp Flag',
       'Mean Temp (°C)', 'Mean Temp Flag', 'Heat Deg Days (°C)',
       'Heat Deg Days Flag', 'Cool Deg Days (°C)', 'Cool Deg Days Flag',
       'Total Rain (mm)', 'Total Rain Flag', 'Total Snow (cm)',
       'Total Snow Flag', 'Total Precip (mm)', 'Total Precip Flag',
       'Snow on Grnd (cm)', 'Snow on Grnd Flag', 'Dir of Max Gust (10s deg)',
       'Dir of Max Gust Flag', 'Spd of Max Gust (km/h)',
       'Spd of Max Gust Flag']

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


# co2_df = pd.read_csv(os.path.join(data_dir, ghg, co2_file), index_col=0, parse_dates=True)
# co2_df.drop(columns = 'Data Source', inplace=True)

# ch4_df = pd.read_csv(os.path.join(data_dir, ghg, ch4_file), index_col=0, parse_dates=True)


# pop_df = pd.read_csv(os.path.join(data_dir, population_file), index_col=0, parse_dates=True)

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


df = pd.read_csv('titanic.csv')

# Title and description
st.markdown(f"<h1 style='text-align: center;'>Historic data for {stn} from {start_wx.year} to {end_wx.year}</h1>",
            unsafe_allow_html=True)
#st.title(f'Historic data for {stn} from {start_wx.year} to {end_wx.year}')
st.write("This app provides basic visualizations for the Titanic dataset.")

# Show dataset
if st.checkbox("Show Raw Dataset"):
    st.write(df)

# Sidebar for user input
st.sidebar.header("Filter Options")
sex_filter = st.sidebar.multiselect("Select Gender", options=df['sex'].unique(), default=df['sex'].unique())
class_filter = st.sidebar.multiselect("Select Class (Pclass)", options=df['pclass'].unique(), default=df['pclass'].unique())
embarked_filter = st.sidebar.multiselect("Select Embarkation Point", options=df['embark_town'].dropna().unique(), default=df['embark_town'].unique())

# Filter dataset based on selections
filtered_df = df[
    (df['sex'].isin(sex_filter)) & 
    (df['pclass'].isin(class_filter)) & 
    (df['embark_town'].isin(embarked_filter))
]


# 

fig4 = go.Figure()

fig4.add_trace(go.Scatter(x=co2_df[co2_df.index < pd.to_datetime(2025, format='%Y')].index,
                          y=co2_df[co2_df.index < pd.to_datetime(2025, format='%Y')]['weak'],
                          mode='lines',
                          name='Observation',
                          line=dict(color='darkgrey')))

for sc in scenario :
    tmp_sc = scenario[sc].replace('-', '_')
    fig4.add_trace(go.Scatter(x=co2_df[co2_df.index >= pd.to_datetime(2025, format='%Y')].index,
                              y=co2_df[co2_df.index >= pd.to_datetime(2025, format='%Y')][sc],
                              mode='lines',
                              name=f'Forecast ({tmp_sc})',
                              line=dict(color=color_scenario[sc], dash='dash')))



# Update layout with title and axis ranges
fig4.update_layout(
     title="Carbon Dioxide Global mean Concentration (ppm) over the Years",  # Set the title here
#     yaxis=dict(
#         range=[tmp['Station'].min(), tmp['Station'].max() + 1]  # Adjust the Y axis minimum
#     ),
#     xaxis=dict(
#         range=[tmp['Year'].min(), tmp['Year'].max() + 1]  # Adjust the X axis minimum
#     )
)

# Display the interactive plot in Streamlit
st.plotly_chart(fig4, use_container_width=True)


fig3 = px.line(wx_df, x=wx_df.index, y=Tmax, title='Maximum Temperature over the Years')

fig3.add_shape(type='line', x0=wx_df.index.min(),
              x1=wx_df.index.max(), y0=30, y1=30,
              line=dict(color='red', width=1, dash='dash'))

fig3.add_shape(type='line', x0=wx_df.index.min(),
              x1=wx_df.index.max(), y0=-20, y1=-20,
              line=dict(color='blue', width=1, dash='dash'))

fig3.add_shape(type='line', x0=wx_df.index.min(),
              x1=wx_df.index.max(), y0=0, y1=0,
              line=dict(color='dodgerblue', width=1, dash='dash'))

# Add markers and lines
fig3.update_traces(
     mode='markers', 
     marker=dict(size=3, color='darkgrey'),
     #line=dict(color='darkgrey')
)

# Only thing I figured is - I could do this 
#fig3.add_scatter(wx_df, x=wx_df.index, y=Tmax, mode='lines')

# Update layout with title and axis ranges
fig3.update_layout(
     title="Maximum Temperature Over The Years",  # Set the title here
#     yaxis=dict(
#         range=[tmp['Station'].min(), tmp['Station'].max() + 1]  # Adjust the Y axis minimum
#     ),
#     xaxis=dict(
#         range=[tmp['Year'].min(), tmp['Year'].max() + 1]  # Adjust the X axis minimum
#     )
)

# Display the interactive plot in Streamlit
st.plotly_chart(fig3, use_container_width=True)

# Display filtered dataset
#st.write("### Filtered Dataset")
#st.write(filtered_df)

tmp = wx_df[wx_df[Tmin] > 0.].groupby('Year').count()
tmp = tmp.reset_index()

# Assuming 'tmp' is your dataframe
fig5 = px.line(tmp, x='Year', y='Station', title='Station Counts Over Years')

# Add markers and lines
fig5.update_traces(
    mode='lines+markers', 
    marker=dict(size=8, color='red')
)

# Update layout with title and axis ranges
fig5.update_layout(
    title="Station Counts Over Time",  # Set the title here
    yaxis=dict(
        range=[tmp['Station'].min(), tmp['Station'].max() + 1]  # Adjust the Y axis minimum
    ),
    xaxis=dict(
        range=[tmp['Year'].min(), tmp['Year'].max() + 1]  # Adjust the X axis minimum
    )
)

# Display the interactive plot in Streamlit
st.plotly_chart(fig5)
# Create an interactive line chart using Plotly
fig2 = px.line(tmp, x='Station', y='Station', title='Station Counts Over Years')

# Customize the Y-axis range (set minimum value and max)
fig2.update_layout(
     yaxis=dict(
         range=[tmp['Station'].min(), tmp['Station'].max() + 1]  # Adjust the Y axis minimum
     ),
     xaxis=dict(
         range=[tmp['Station'].min(), tmp['Station'].max() + 1]  # Adjust the x axis minimum
     ),
     title="Station Counts blablabla Over Time"
)

# Display the interactive plot in Streamlit
st.plotly_chart(fig2)

# chart = alt.Chart(tmp).mark_line().encode(
#     x='Year:O',
#     y=alt.Y('Station:Q', scale=alt.Scale(domain=[ tmp['Station'].min(), tmp['Station'].max() + 1]))  # Adjust min here
# ).properties(
#     width=700,
#     height=400
# )

# st.altair_chart(chart, use_container_width=True)
# Viz 1: Survival countplot
st.subheader("Survival Count")
survival_count = filtered_df['survived'].value_counts()
st.line_chart(tmp['Station'])
#st.bar_chart(survival_count.rename(index={0: 'Did not survive', 1: 'Survived'}))

# Viz 2: Survival by gender
st.subheader("Survival Rate by Gender")

gender_survival = filtered_df.groupby('sex')['survived'].mean().reset_index()

fig = px.pie(
    gender_survival,
    names='sex',
    values='survived',
    title="Survival Rate by Gender",
)

# Display the pie chart
st.plotly_chart(fig)

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



tmp = wx_df[wx_df['Total Precip (mm)'] > 75.].groupby('Year').count()
tmp = tmp.rename(columns={'Station':'Count'}).reset_index()
#tmp['Year'] = pd.to_datetime(tmp['Year'], format='%Y')
#tmp.set_index('Year', inplace=True)
#st.write(tmp)

fig = go.Figure()
fig.add_trace(go.Bar(x=tmp['Year'], 
                     y=tmp['Count'],
                     name='Rain Events',
                     hovertemplate='<b>Year</b>: %{x}<br>' +
                                   '<b># of events</b>: %{y}<extra></extra>'))

fig.update_layout(
     yaxis=dict(range=[0, tmp['Count'].max()],
                tickmode='linear',     
                dtick=1),
     #xaxis=dict(range=[tmp.index.min(), tmp.index.max()],
     #           tickmode='linear',     
     #           dtick=1),
     title="Quantity of daily rain event > 75 mm per year"
)

st.plotly_chart(fig, use_container_width=True)

#st.bar_chart(tmp['Station'])


