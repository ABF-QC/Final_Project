# Climate App Explorer for Downtown Montreal

Explore over a century of maximum/minimum temperature and precipitation data from downtown Montreal (McTavis/McGill). This project combines data analysis, modeling, and interactive visualization to understand historical climate patterns and explore future warming scenarios.

---

## Data

This project integrates a variety of datasets to analyze historical and projected climate trends in downtown Montreal.

**Montreal's Population**
Population density significantly impact the land surface of a city. The surface type consequently influence the surface albedo, its capacity to retain moisture, and so much more. When the population is dense enough and has changed the surface type from mainly vegetation to a dense building surface area, the urban heat island effect is created over the urban area. The Urban Heat Island Effect means that the urban area accumulate more heat than its surroundings rural areas and, consequently, the maximum temperature and minimum temperature will generally be warmer in the urban area than in the surroundings rural areas.

By using the Montreal's population as an input feature of my RNN model, I am hoping that it will be able to establish the connection between the population curve and the temperature. Thus, in its own way see the Urban Heat Island Effect.

Here we can have a look at the past and predicted data for Montreal's population.

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
    
**Included Variables**:
- `Date` – daily timestamps (from 1910 onward)
- `MaxTemp (°C)` – daily maximum temperature
- `CO₂ (ppm)` – atmospheric carbon dioxide concentrations (monthly or yearly averages)
- `CH₄ (ppb)` – atmospheric methane concentrations
- `Population` – projected and historical population values for Montreal or Quebec
- `Scenario` – Shared Socioeconomic Pathway (e.g., SSP2-4.5)

**Format**: Combined CSV and JSON files (tabular format), organized by year or time-series.

---

## Data Pre-processing

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


