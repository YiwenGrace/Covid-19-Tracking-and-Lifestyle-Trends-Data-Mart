import pandas as pd
import numpy as np
import time
import datetime

df = pd.read_csv("2020_CA_Region_Mobility_Report.csv")
print(df.head())

# create patient dimension
Mobility_dimension = pd.DataFrame(
    columns=['Mobility_key', 'Date', 'Metro_area', 'Subregion',
             'Province', 'Retail_and_recreation', 'Grocery_and_pharmacy', 'Park', 'Transit_stations',
             'Workplaces', 'Residential'])
print('total', len(df))

count = 0
for idx, row in df.iterrows():
    if (row['sub_region_2'] == "Ottawa Division" or
        row['sub_region_2'] == "Toronto Division" or
        row['sub_region_2'] == "Regional Municipality of Durham" or
        row['sub_region_2'] == "Regional Municipality of Halton" or
        row['sub_region_2'] == "Regional Municipality of Peel" or
        row['sub_region_2'] == "Regional Municipality of York") and (
            int(row["date"][0:4]) == 2020 and int(row["date"][5:7]) >= 9):
        if row['sub_region_2'] == "Ottawa Division":
            row['sub_region_2'] = 'Ottawa'
        elif row['sub_region_2'] == "Toronto Division":
            row['sub_region_2'] = 'Toronto'
        elif row['sub_region_2'] == "Regional Municipality of Durham":
            row['sub_region_2'] = 'Durham'
        elif row['sub_region_2'] == "Regional Municipality of Halton":
            row['sub_region_2'] = 'Halton'
        elif row['sub_region_2'] == "Regional Municipality of Peel":
            row['sub_region_2'] = 'Peel'
        elif row['sub_region_2'] == "Regional Municipality of York":
            row['sub_region_2'] = 'York'
        mobility_row = [(row["place_id"] + row["date"]).replace("-", ""), row['date'], row['metro_area'],
                        row['sub_region_2'], row['sub_region_1'],
                        row['retail_and_recreation_percent_change_from_baseline'],
                        row['grocery_and_pharmacy_percent_change_from_baseline'],
                        row['parks_percent_change_from_baseline'],
                        row['transit_stations_percent_change_from_baseline'],
                        row['workplaces_percent_change_from_baseline'],
                        row['residential_percent_change_from_baseline']]

        Mobility_dimension.loc[len(Mobility_dimension)] = mobility_row
        count += 1
        print(count, "added")

Mobility_dimension.insert(0, "Mobility_surrogate_key", np.arange(len(Mobility_dimension)))
Mobility_dimension = Mobility_dimension.fillna({'Retail_and_recreation': '0'})
Mobility_dimension = Mobility_dimension.fillna({'Grocery_and_pharmacy': '0'})
Mobility_dimension = Mobility_dimension.fillna({'Park': '0'})
Mobility_dimension = Mobility_dimension.fillna({'Transit_stations': '0'})
Mobility_dimension = Mobility_dimension.fillna({'Workplaces': '0'})
Mobility_dimension = Mobility_dimension.fillna({'Residential': '0'})
Mobility_dimension.to_csv("Mobility_dimension.csv", index=False)

# Patient_dimension.to_csv("patient_dimension.csv", index=False)
print(Mobility_dimension.head())
