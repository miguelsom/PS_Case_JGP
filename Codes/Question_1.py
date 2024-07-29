import json
import requests
import pandas as pd

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



# Initialize an empty DataFrame
df_all_series = pd.DataFrame()

for series_id in SERIES_IDS:
    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "seriesid": [series_id],
        "startyear": START_YEAR,
        "endyear": END_YEAR
    })

    response = requests.post(BLS_API_URL, data=payload, headers=headers)
    response_data = response.json()

    if 'Results' in response_data:
        # Extract series data

        series_data = response_data['Results']['series'][0]['data']

        # Create a temporary DataFrame for the current series
        df_temp = pd.DataFrame(series_data)

        # Process the DataFrame
        df_temp['value'] = df_temp['value'].astype(float)
        df_temp['year'] = df_temp['year'].astype(int)
        df_temp['period'] = df_temp['period'].str.replace('M', '').astype(int)
        df_temp['date'] = pd.to_datetime(df_temp['year'].astype(str) + '-' + df_temp['period'].astype(str).str.zfill(2) + '-01')

        # Add the series ID column
        df_temp['series_id'] = series_id

        # Sort the DataFrame by date
        df_temp = df_temp.sort_values('date')

        # Append to the main DataFrame
        df_all_series = pd.concat([df_all_series, df_temp], ignore_index=True)
    else:
        print(f"Error processing request for series ID: {series_id}")
        print("Error message:", response_data.get('message'))

# Drop unnecessary columns
df_all_series.drop(['year', 'period', 'periodName', 'footnotes'], axis=1, inplace=True)

# Pivot the DataFrame to have series IDs as columns
df_pivot = df_all_series.pivot(index='date', columns='series_id', values='value').reset_index()

# Print the pivot DataFrame
print(df_pivot)

# Save the DataFrame to a CSV file
df_pivot.to_csv('cpi_data.csv', index=False)
print("Data saved to 'cpi_data.csv'")
