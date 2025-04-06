import streamlit as st
import pandas as pd
import os

#----------------------------
# Adjust page config
#----------------------------
st.set_page_config(layout="wide")

#----------------------------
# Define paths and filenames
#----------------------------
data_dir = '../../data/'
model_dir = '../model/'

climate_file = 'ECCC/processed/daily/daily_processed.csv'

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


#st.set_page_config(page_title="Climate Dashboard", layout="wide")

st.markdown(f"<h1 style='text-align: center;'>🌍 Welcome to the Climate App for {stn}</h1>",
            unsafe_allow_html=True)

text = f"In this app, you will navigate through past data for {stn} from {start_wx.year} to {end_wx.year}."

st.write(f"<p style='text-align: left;'></br></br>{text}</p>", unsafe_allow_html=True)


text = f"You will be able to see historic data for the maximum temperature, minimum temperature and precipitation. The ultimate goal of this application is to be able to visualize the weather's evolution of the last century for {stn}.</br></br> In addition, you will be able to visualize the frequency of severe events trough time. For example, the yearly occurence of temperature higher than 30 °C or the yearly occurency of daily precpitation amount greater than 75 mm."

st.write(f"<p style='text-align: left;'></br></br>{text}</p>", unsafe_allow_html=True)


text = f"Another important feature of this app is the climate forecast visualizer for different global warming scenarios. You will be able to see the daily maximum and minimum temperatures prediction for four different global warming scenario. The prediction were produced from a Recurrent Neural Network (RNN) model build from the past data of mean global carbone dioxide concentration, mean global methane concentration, Montreal's population and {stn}'s maximum/minimum daily temperatures."

st.write(f"<p style='text-align: left;'></br></br>{text}</p>", unsafe_allow_html=True)


text = f"Use the sidebar to navigate between pages."

st.write(f"<p style='text-align: left;'></br></br>{text}</p>", unsafe_allow_html=True)
