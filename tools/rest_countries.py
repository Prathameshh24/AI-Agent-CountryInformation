import requests


BASE_URL = "https://restcountries.com/v3.1/name/"


def fetch_country_data(country: str):
    try:
        response = requests.get(f"{BASE_URL}{country}")

        if response.status_code != 200:
            return None

        data = response.json()

        # REST Countries returns a list
        return data[0]

    except Exception:
        return None