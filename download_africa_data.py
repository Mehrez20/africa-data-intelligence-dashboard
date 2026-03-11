import pandas as pd
import numpy as np

countries = [
("Tunisia",34.0,9.0,12000000,45),
("Algeria",28.0,1.6,45000000,180),
("Morocco",31.7,-7.1,37000000,130),
("Egypt",26.8,30.8,110000000,350),
("Libya",26.3,17.2,7000000,40)
]

years = list(range(2000,2024))

rows = []

for country,lat,lon,pop_base,gdp_base in countries:

    for i,year in enumerate(years):

        population = pop_base + i*150000
        gdp = gdp_base + i*2.5
        co2 = np.random.uniform(2,50)

        rows.append({
            "country":country,
            "year":year,
            "gdp":round(gdp,2),
            "population":int(population),
            "co2":round(co2,2),
            "lat":lat,
            "lon":lon
        })

df = pd.DataFrame(rows)

df.to_csv("data/north_africa_data.csv",index=False)

print("Dataset fixed and generated")