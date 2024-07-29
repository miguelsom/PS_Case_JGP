# before execute to initiate the server: 
# uvicorn Question_bonus:app --reload


import requests

BASE_URL = "http://127.0.0.1:8000"

def get_welcome_message():
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code}

def get_all_data():
    response = requests.get(f"{BASE_URL}/data")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code}

def get_series_data(series_id):
    response = requests.get(f"{BASE_URL}/data/{series_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code}

def get_series_data_within_date_range(series_id, start_date, end_date):
    response = requests.get(f"{BASE_URL}/data/{series_id}/{start_date}/{end_date}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code}

if __name__ == "__main__":
    print("Welcome Message:")
    print(get_welcome_message())

    print("\nAll Data:")
    print(get_all_data())

    print("\nSeries Data (CUSR0000SA0):")
    print(get_series_data("CUSR0000SA0"))

    print("\nSeries Data (CUSR0000SA0) within date range (2019-01-01 to 2020-01-01):")
    print(get_series_data_within_date_range("CUSR0000SA0", "2019-01-01", "2020-01-01"))
