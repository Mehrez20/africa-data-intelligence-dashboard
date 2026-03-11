import pandas as pd
import numpy as np
import os

# créer dossier data si inexistant
os.makedirs("data", exist_ok=True)

# pays avec coordonnées + population + GDP de base
countries = [
("Tunisia",34.0,9.0,12e6,48e9),
("Algeria",28.0,1.6,45e6,190e9),
("Morocco",31.7,-7.1,37e6,140e9),
("Egypt",26.8,30.8,110e6,350e9),
("Libya",26.3,17.2,7e6,40e9),
("Nigeria",9.1,8.7,220e6,440e9),
("Kenya",-1.2,36.8,55e6,110e9),
("South Africa",-30.5,22.9,60e6,420e9),
("Ghana",7.9,-1.0,34e6,75e9),
("Ethiopia",9.1,40.5,120e6,160e9)
]

years = list(range(2000,2024))
months = list(range(1,13))

rows = []

for country,lat,lon,base_pop,base_gdp in countries:

    for year in years:
        for month in months:

            # croissance GDP
            gdp = base_gdp * (1 + 0.035*(year-2000)) * np.random.uniform(0.97,1.03)

            # croissance population
            population = base_pop * (1 + 0.015*(year-2000))

            # CO2
            co2 = np.random.uniform(1.5,6)

            # internet
            internet = min(95, np.random.uniform(5,40) + (year-2000)*2)

            # chômage
            unemployment = np.random.uniform(6,20)

            rows.append([
                year,
                country,
                gdp,
                population,
                co2,
                internet,
                unemployment,
                lat,
                lon
            ])

df = pd.DataFrame(rows,columns=[
"year",
"country",
"gdp",
"population",
"co2",
"internet",
"unemployment",
"lat",
"lon"
])

# dataset complet
df.to_csv("data/big_dataset.csv",index=False)

# dataset Tunisie
tunisia = df[df["country"]=="Tunisia"]
tunisia.to_csv("data/tunisia_data.csv",index=False)

# dataset Afrique du Nord
north_africa = df[df["country"].isin(["Tunisia","Algeria","Morocco","Egypt","Libya"])]
north_africa.to_csv("data/north_africa_data.csv",index=False)

print("Dataset created successfully")
print("Total rows :",len(df))