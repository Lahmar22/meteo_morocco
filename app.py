import os
import requests
import pandas as pd


def get_params():
    url = "https://simplemaps.com/static/data/country-cities/ma/ma.csv"

    data = pd.read_csv(url)

    ma = data[["city", "lat", "lng"]]

    os.makedirs("extraction", exist_ok=True)

    ma.to_csv("extraction/ma.csv", index=False)

    print("✅ Cities extracted successfully.")


def get_weather(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ",".join([
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "precipitation_probability_max",
            "wind_speed_10m_max",
            "wind_gusts_10m_max",
            "weather_code"
        ]),
        "timezone": "Africa/Casablanca",
        "forecast_days": 7
    }

    response = requests.get(url, params=params)

    response.raise_for_status()

    return response.json()


def conserve_data():

    data = pd.read_csv("extraction/ma.csv")

    latitudes = ",".join(data["lat"].astype(str))
    longitudes = ",".join(data["lng"].astype(str))

    weather = get_weather(latitudes, longitudes)

    if weather is None:
        return None

    resultats = []

    for city, result in zip(data["city"], weather):

        resultats.append({
            "city": city,
            "latitude": result["latitude"],
            "longitude": result["longitude"],
            "daily": result["daily"]
        })

    return resultats


def transformer_data():
    """Transform nested weather data into a flat table."""

    data = conserve_data()

    if data is None:
        return None

    rows = []

    for item in data:

        city = item["city"]
        daily = item["daily"]

        for i in range(len(daily["time"])):

            rows.append({
                "city": city,
                "latitude": item["latitude"],
                "longitude": item["longitude"],
                "date": daily["time"][i],
                "temp_max": daily["temperature_2m_max"][i],
                "temp_min": daily["temperature_2m_min"][i],
                "precipitation": daily["precipitation_sum"][i],
                "precip_probability": daily["precipitation_probability_max"][i],
                "wind_speed": daily["wind_speed_10m_max"][i],
                "wind_gusts": daily["wind_gusts_10m_max"][i],
                "weather_code": daily["weather_code"][i]
            })

    df = pd.DataFrame(rows)

    return df


def save_data():
    """Save transformed weather data."""

    df = transformer_data()

    if df is None:
        return

    os.makedirs("data", exist_ok=True)

    df.to_csv(
        "data/weather_maroc.csv",
        index=False
    )

    print("✅ Weather data saved successfully.")
    print(f"📊 Number of rows: {len(df)}")
    print(df.head())


if __name__ == "__main__":


    get_params()

    save_data()