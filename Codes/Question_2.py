import pandas as pd
import plotly.graph_objects as go

SERIES_ID_CPI_ALL_ITEMS_SEASONALLY_ADJUSTED = "CUSR0000SA0"
SERIES_ID_CPI_ALL_ITEMS_LESS_FOOD_ENERGY_SEASONALLY_ADJUSTED = "CUSR0000SA0L1E"
SERIES_ID_CPI_GASOLINE_ALL_TYPES_SEASONALLY_ADJUSTED = "CUSR0000SEGA"
SERIES_IDS = [
    SERIES_ID_CPI_ALL_ITEMS_SEASONALLY_ADJUSTED,
    SERIES_ID_CPI_ALL_ITEMS_LESS_FOOD_ENERGY_SEASONALLY_ADJUSTED,
    SERIES_ID_CPI_GASOLINE_ALL_TYPES_SEASONALLY_ADJUSTED
]
START_YEAR = "2014"
END_YEAR = "2024"
BLS_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"


# Load the DataFrame from the CSV file
df_pivot = pd.read_csv('cpi_data.csv')

# Filter data for the series "All items, less food and energy, seasonally adjusted" since 2018
series_id_less_food_energy = SERIES_ID_CPI_ALL_ITEMS_LESS_FOOD_ENERGY_SEASONALLY_ADJUSTED
df_filtered = df_pivot[['date', series_id_less_food_energy]].copy()
df_filtered['date'] = pd.to_datetime(df_filtered['date'])

# Calculate year-over-year percentage change
df_filtered.loc[:, 'yoy_pct_change'] = df_filtered[series_id_less_food_energy].diff(12) / df_filtered[series_id_less_food_energy].shift(12) * 100

# Filter the data again to start from 2019
df_filtered = df_filtered[df_filtered['date'] >= '2019-01-01']

# Create the plot
fig = go.Figure()

# Add the price series line
fig.add_trace(go.Scatter(
    x=df_filtered['date'],
    y=df_filtered[series_id_less_food_energy],
    mode='lines',
    name='All items, less food and energy (SA)',
    line=dict(color='blue')
))

# Add the year-over-year percentage change line
fig.add_trace(go.Scatter(
    x=df_filtered['date'],
    y=df_filtered['yoy_pct_change'],
    mode='lines',
    name='Year-over-Year % Change',
    line=dict(color='red'),
    yaxis='y2'
))

# Configure the axes
fig.update_layout(
    title='CPI All items, less food and energy (SA) - Monthly Data from 2019',
    xaxis_title='Date',
    yaxis_title='CPI Value',
    yaxis2=dict(
        title='Year-over-Year % Change',
        overlaying='y',
        side='right'
    ),
    legend=dict(x=0.1, y=1.1)
)

# Display the plot
fig.show()
