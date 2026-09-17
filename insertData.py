import pandas as pd
from connectionDB import engine

def insertData():
    data_final = pd.read_csv("Gold/weather_maroc_final.csv")
    data_silver = pd.read_csv("Silver/weather_maroc_claire.csv")
    data_city = pd.read_csv("extraction/ma.csv")


    data_final.to_sql("meteo_categories", con=engine, if_exists="replace", index=False)
    data_silver.to_sql("meteo", con=engine, if_exists="replace", index=False)
    data_city.to_sql("cities", con=engine, if_exists="replace", index=False)

    print("Données insérées avec succès !")
