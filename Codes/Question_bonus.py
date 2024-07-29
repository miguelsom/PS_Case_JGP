from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()

# Load the data from the CSV file
df = pd.read_csv('cpi_data.csv')

@app.get("/")
def read_root():
    return {"message": "Welcome to the CPI Data API"}

@app.get("/data")
def read_data():
    return df.to_dict(orient="records")

@app.get("/data/{series_id}")
def read_series(series_id: str):
    if series_id not in df.columns:
        raise HTTPException(status_code=404, detail="Series ID not found")
    return df[["date", series_id]].dropna().to_dict(orient="records")

@app.get("/data/{series_id}/{start_date}/{end_date}")
def read_series_date_range(series_id: str, start_date: str, end_date: str):
    if series_id not in df.columns:
        raise HTTPException(status_code=404, detail="Series ID not found")
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    return df.loc[mask, ["date", series_id]].dropna().to_dict(orient="records")
