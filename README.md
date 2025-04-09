# Climate App Explorer for Downtown Montreal

Explore over a century of maximum/minimum temperature and precipitation data from downtown Montreal (McTavis/McGill). This project combines data analysis, modeling, and interactive visualization to understand historical climate patterns and explore future warming scenarios.

---

## Data

This project integrates a variety of datasets to analyze historical and projected climate trends in downtown Montreal.

**Sources**:
- Environment and Climate Change Canada (historical temperature data)
- Institut de la statistique du Québec (population forecasts)
- IPCC & CMIP6 (climate projections, SSP scenarios)
- Global Monitoring Laboratory (NOAA) for GHG concentrations

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


