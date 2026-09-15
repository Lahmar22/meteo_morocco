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
    df = transformer_data()

    if df is None:
        return

    os.makedirs("bronze", exist_ok=True)
    df.to_csv(
        "bronze/weather_maroc.csv",
        index=False
    )
    print("✅ Weather data saved successfully.")
    print(f"📊 Number of rows: {len(df)}")
    print(df.head())


def nettoyage_data():
    data = pd.read_csv("bronze/weather_maroc.csv")
    data["city"] = data["city"].astype(str).str.strip()

    data["latitude"] = pd.to_numeric(data["latitude"], errors="coerce")
    data["longitude"] = pd.to_numeric(data["longitude"], errors="coerce")

    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data["temp_max"] = pd.to_numeric(data["temp_max"], errors="coerce")
    data["temp_min"] = pd.to_numeric(data["temp_min"], errors="coerce")
    data = data.drop_duplicates()

    data = data[(data["latitude"].between(27, 36)) & (data["longitude"].between(-14, -1))]

    data = data[data["temp_max"] >= data["temp_min"]]

    data = data[data["precipitation"] >= 0]
    data = data[data["wind_speed"] >= 0]

    

    os.makedirs("Silver", exist_ok=True)
    data.to_csv(
        "Silver/weather_maroc_claire.csv",
        index=False
    )

def categorie_temperature(temp):
    if temp < 10:
        return "Froid"
    elif temp < 20:
        return "Frais"
    elif temp < 30:
        return "Modéré"
    elif temp < 40:
        return "Chaud"
    else:
        return "Très chaud"

def categorie_precipitation(value):
    if value == 0:
        return "Aucune"
    elif value < 5:
        return "Faible"
    elif value < 20:
        return "Modérée"
    else:
        return "Forte"

def categorie_vent(speed):
    if speed < 10:
        return "Faible"
    elif speed < 30:
        return "Modéré"
    elif speed < 50:
        return "Fort"
    else:
        return "Très fort"

def categorie_data():
    data = pd.read_csv("Silver/weather_maroc_claire.csv")
    
    data["temperature_category"] = data["temp_max"].apply(
        categorie_temperature
    )
    data["precipitation_category"] = data["precipitation"].apply(
        categorie_precipitation
    )
    data["wind_category"] = data["wind_speed"].apply(
         categorie_vent
    )

    danger_percentage = (
        data["temp_max"] * 0.20
        + data["precipitation"] * 0.40
        + data["wind_speed"] * 0.40
    )

    data["score"] = danger_percentage

    bins = [0, 25, 50, 75, 100]
    labels = ["Faible", "Modéré", "Élevé", "Critique"]
    data["danger"] = pd.cut(
        data["score"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )
    os.makedirs("Gold", exist_ok=True)
    data.to_csv("Gold/weather_maroc_final.csv", index=False)

    
    

    


    

if __name__ == "__main__":

    # get_params()

    # save_data()
    categorie_data()