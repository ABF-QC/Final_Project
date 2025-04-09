# Climate App Explorer and Climate Forecast for Downtown Montreal

</br>

Explore over a century of maximum/minimum temperature and precipitation data from downtown Montreal (McTavis/McGill). This project combines data analysis, modeling, and interactive visualization to understand historical climate patterns and explore future warming scenarios.


</br></br>


---
## Data

This project integrates a variety of datasets to analyze historical trends and to project our climate trends from our Recurrent Neural Network (RNN) model in downtown Montreal.

</br></br>

**Historic Daily Climate Data**

The historic climate data for downtown Montreal at the weather station McTavish/McGill is available since 1871. Our main focus for the analysis and visualization will be on maximum temperature, minimum temperature and precipitation. While we will focus solely on maximum and minimum temperature in our RNN model.

</br></br>

**Grenhouse Gases (Carbon dioxide and Methane)**

 Carbon dioxide (CO2) and methane (CH4), even though there are more greenhouse gases (GHG) contributing to climate change than these two, were chosen since they have a great impact on climate change.

The forecast of the GHG are based from the Shared Socioeconomic Pathways (SSPs), which are climate change scenarios of projected socioeconomic global changes up to 2100 as defined in the IPCC Sixth Assessment Report on climate change in 2021. They are used to derive GHG emissions scenarios with different climate policies.

</br>

| Scenario  | Description                                                       |
|-----------|-------------------------------------------------------------------|
| **SSP4-34** | Intermediate GHG emissions with a desire to implement climate policies |
| **SSP2-45** | Low to intermediate GHG emissions with large social disparities  |
| **SSP4-60** | Intermediate to high GHG emissions with deep social inequalities |
| **SSP5-80** | Very high GHG emissions (worst case scenario)                    |

</br>

By using the CO2 and CH4 global mean concentration as an input features of my RNN model, I am hoping that it will be able to establish the connection between the GHG curves and the temperature. Thus, in its own way see the GHG impact on climate change.

</br></br>

**Montreal's Population**

Population density significantly impact the land surface of a city. The surface type consequently influence the surface albedo, its capacity to retain moisture, and so much more. When the population is dense enough and has changed the surface type from mainly vegetation to a dense building surface area, the urban heat island effect is created over the urban area. The Urban Heat Island Effect means that the urban area accumulate more heat than its surroundings rural areas and, consequently, the maximum temperature and minimum temperature will generally be warmer in the urban area than in the surroundings rural areas.

By using the Montreal's population as an input feature of my RNN model, I am hoping that it will be able to establish the connection between the population curve and the temperature. Thus, in its own way see the Urban Heat Island Effect.

</br></br>

**Sources**:
- Environment and Climate Change Canada
  - [Historic Climate Data](https://dd.weather.gc.ca/climate/observations/)
- Wikipedia
  - [Population census from Statistic Canada]( https://fr.wikipedia.org/wiki/Montr%C3%A9al) 
- Institut de la statistique du Québec
  - [Population predictions](https://statistique.quebec.ca/en/fichier/perspectives-demographiques-quebec-et-regions-2021-2071-edition-2024.pdf)
- IPCC & CMIP6 (climate projections, SSP scenarios)
  - [Greenhouse Gases Global Mean Concentration Predictions](https://greenhousegases.science.unimelb.edu.au/#!/view)
- Global Monitoring Laboratory (NOAA) for GHG concentrations
  - [CO2 Global Mean Concentration Observations (1959-2024)](https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_mlo.txt)
  - [CH4 Global Mean Concentration Observations (1984-2023)](https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_annmean_gl.txt)
- NASA - GHG concentrations monitoring
  - [CO2 Global Mean Concentration Observations (1850-2011)](https://data.giss.nasa.gov/modelforce/ghgases/Fig1A.ext.txt)
- SeaLevel.info
  - [CH4 Global Mean Concentration Observations (1010-1992)](https://sealevel.info/EthCH498B.txt)

</br></br>
 
**Included Variables for the visualization**:
- Daily maximum temperature (°C)
- Daily minimum temperature (°C)
- Daily precipitation amount (mm)
- Atmospheric carbon dioxide concentrations (ppm)
- Atmospheric methane concentrations (ppb)
- Population for Montreal

</br>

**Included Variables for the RNN model**:
- Daily maximum temperature (°C)
- Daily minimum temperature (°C)
- Atmospheric carbon dioxide concentrations (ppm)
- Atmospheric methane concentrations (ppb)
- Population for Montreal

</br></br>

---
## Data Pre-processing

Data needs to be avaiable on the same period and at the same timesteps without any gap in order to build our RNN model.

</br>

**Historic Daily Climate Data**

In order to fill in gaps of missing data for the weather station of Montreal (McTavish/McGill), we also retrieved the weather station reports from weather stations over Montreal's Island. We replaced any missing daily weather reports from the closest available station on that day. Once that processed was done, we had full years of consecutive daily weather reports for Montreal (McTavish/McGill) from 1892 to 2024. 

Here are the [results](data/ECCC/processed/daily/daily_processed.csv). 

</br></br>

**Grenhouse Gases (Carbon dioxide and Methane)**

The data were interpolated with a polynomal method to get yearly data and to removed the discontinuities between the various dataset. The results were a complete dataset including the observations and the prediction yearly for every SSP scenario from 1850 to 2099.

Here are the [files](data/GreenHouse_Gases/processed/).


An additional interpolation with a linear method was used to bring the dataset at the same time scale as the climate weather reports, which are available daily, to build our RNN model.

</br></br>

**Montreal's Population**

The data were interpolated with a polynomal method to get yearly data and to removed the discontinuities between the various dataset. The results were a complete dataset including the observations and the prediction yearly from 1801 to 2099.

Here are the [files](data/Population/processed/Montreal.csv).

</br></br>

##### Table 1: Population Growth Rates – Montréal  
**Source**: *Institut de la statistique du Québec*

| Period       | 2021–2026 | 2026–2031 | 2031–2036 | 2036–2041 |
|--------------|-----------|-----------|-----------|-----------|
| Montréal     | 5.2%      | -2.1%     | -0.1%     | 0.0%      |

</br></br>

##### Table 2: Projected Population – Montréal  
**Source**: *Institut de la statistique du Québec*

| Year | Population |
|------|------------|
| 2026 | 2,121,100  |
| 2031 | 2,077,000  |
| 2036 | 2,075,600  |
| 2041 | 2,076,700  |
| 2046 | 2,079,700  |
| 2051 | 2,084,400  |

</br></br>

##### Table 2: Scenarios of Projected Population for 2071 – Province
**Prediction for 2071**:

| Scenario          | Formula                           | Population |
|------------------|-----------------------------------|------------|
| Weak             | 2,084,400 × (1 - 0.04)             | 2,001,024  |
| Moderate         | 2,084,400 × (1 + 0.065)            | 2,219,886  |
| High             | 2,084,400 × (1 + 0.15)             | 2,397,060  |

</br></br>

Steps involved:
- Handle missing or inconsistent temperature values
- Convert date formats and extract time-based features (e.g., year, month, season)
- Aggregate data (daily → annual/monthly means or extremes)
- Normalize/scale inputs for model training
- Merge historical data with projection scenarios
- Merge population, CO₂, and CH₄ concentration data for regression modeling or scenario analysis

Key tools: `pandas`, `numpy`, `scikit-learn`

---

## Model

The modeling approach includes:
- **Forecasting Models**: Time-series regressors (e.g., ARIMA, Prophet, or RNN/LSTM for temporal dependencies)
- **Scenario Integration**: SSP pathway projections used to adjust forecasts based on policy or emission assumptions
- **Multivariate Extensions**: Incorporation of additional climate indicators (e.g., CO₂, CH₄) and population data

---

## Validation

Validation strategies:
- **Train/Test Split**: Typically 80/20 based on time (e.g., training: 1910–2000, testing: 2001–2023)
- **Metrics**: MSE
- **Cross-validation**: TimeSeriesSplit where appropriate

---

## Results & Visualization / 🚀 App Deployment

### Visualization
- Interactive line plots and scatter plots (Streamlit + Plotly)
- Forecast overlays with SSP scenarios (e.g., SSP2-4.5, SSP5-8.5)
- Scenario explanation tables embedded in the UI


