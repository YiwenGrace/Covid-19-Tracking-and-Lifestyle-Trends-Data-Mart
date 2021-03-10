import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# read csv

df = pd.read_csv("Confirmed_Positive_Cases_ON.csv")
date = pd.read_csv("date.csv")

# print(date.head())

# create Onset Date dimension

Onset_date_dimension = pd.DataFrame(
    columns=['Onset_date_key', 'Date', 'Day', 'Month', 'Day_of_Week',
             'Week_in_Year', 'Weekend', 'Holiday', 'Season'])

for idx, row in date.iterrows():
    date_row = ["On" + row["id"].replace("-", ""), row["id"], row['Day'], row['Month'], row['Day_of_Week'],
                row['Week_in_Year'], row['Weekend'], row['Holiday'], row['Season']]
    Onset_date_dimension.loc[len(Onset_date_dimension)] = date_row

Onset_date_dimension.insert(0, "Onset_date_surrogate_key", np.arange(len(Onset_date_dimension)))
Onset_date_dimension.to_csv("Onset_Date_dimension.csv", index=False)

# create Reported Date dimension

Reported_date_dimension = pd.DataFrame(
    columns=['Reported_date_key', 'Date', 'Day', 'Month', 'Day_of_Week',
             'Week_in_Year', 'Weekend', 'Holiday', 'Season'])

for idx, row in date.iterrows():
    date_row = ["Re" + row["id"].replace("-", ""), row["id"], row['Day'], row['Month'], row['Day_of_Week'],
                row['Week_in_Year'], row['Weekend'], row['Holiday'], row['Season']]
    Reported_date_dimension.loc[len(Reported_date_dimension)] = date_row

Reported_date_dimension.insert(0, "Reported_date_surrogate_key", np.arange(len(Reported_date_dimension)))
Reported_date_dimension.to_csv("Reported_Date_dimension.csv", index=False)

# create Test Date dimension

Test_date_dimension = pd.DataFrame(
    columns=['Test_date_key', 'Date', 'Day', 'Month', 'Day_of_Week',
             'Week_in_Year', 'Weekend', 'Holiday', 'Season'])

for idx, row in date.iterrows():
    date_row = ["Te" + row["id"].replace("-", ""), row["id"], row['Day'], row['Month'], row['Day_of_Week'],
                row['Week_in_Year'], row['Weekend'], row['Holiday'], row['Season']]
    Test_date_dimension.loc[len(Test_date_dimension)] = date_row

Test_date_dimension.insert(0, "Test_date_surrogate_key", np.arange(len(Test_date_dimension)))
Test_date_dimension.to_csv("Test_Date_dimension.csv", index=False)

# create Specimen Date dimension

Specimen_date_dimension = pd.DataFrame(
    columns=['Specimen_date_key', 'Date', 'Day', 'Month', 'Day_of_Week',
             'Week_in_Year', 'Weekend', 'Holiday', 'Season'])

for idx, row in date.iterrows():
    date_row = ["Sp" + row["id"].replace("-", ""), row["id"], row['Day'], row['Month'], row['Day_of_Week'],
                row['Week_in_Year'], row['Weekend'], row['Holiday'], row['Season']]
    Specimen_date_dimension.loc[len(Specimen_date_dimension)] = date_row

Specimen_date_dimension.insert(0, "Specimen_date_surrogate_key", np.arange(len(Specimen_date_dimension)))
Specimen_date_dimension.to_csv("Specimen_Date_dimension.csv", index=False)

# create patient dimension

Patient_dimension = pd.DataFrame(columns=['Patient_Key', 'Gender', 'Age_group',
                                          'Acquisition_group', 'Outbreak_related'])
count = 0
for idx, row in df.iterrows():
    if int(row['Accurate_Episode_Date'][0:4]) == 2020 \
            and int(row['Accurate_Episode_Date'][5:7]) >= 9 \
            and int(row['Case_Reported_Date'][0:4]) == 2020 \
            and (row['Reporting_PHU'] == "Ottawa Public Health" or
                 row['Reporting_PHU'] == "Toronto Public Health" or
                 row['Reporting_PHU'] == "Durham Region Health Department" or
                 row['Reporting_PHU'] == "Halton Region Health Department" or
                 row['Reporting_PHU'] == "Peel Public Health" or
                 row['Reporting_PHU'] == "York Region Public Health Services"):

        if row['Outbreak_Related'] != "Yes":
            row['Outbreak_Related'] = "No"

        patient_row = [row["Row_ID"], row['Client_Gender'], row['Age_Group'],
                       row['Case_AcquisitionInfo'], row['Outbreak_Related']]
        Patient_dimension.loc[len(Patient_dimension)] = patient_row

        count += 1
        print("current at ", idx)
        print(count, "added")

Patient_dimension.insert(0, "Patient_surrogate_key", np.arange(len(Patient_dimension)))
Patient_dimension.to_csv("patient_dimension.csv", index=False)
# print(Patient_dimension.head())

# create PHU dimension

PHU_Location_dimension = pd.DataFrame(columns=['PHU_id', 'PHU_name', 'Address', 'City',
                                               'Postal_Code', 'Province', 'URL', 'Latitude', 'Longitude'])
pid = []

for idx, row in df.iterrows():
    if row['Outbreak_Related'] != "Yes":
        row['Outbreak_Related'] = "No"

    if row["Reporting_PHU_ID"] not in pid:
        pid.append(row["Reporting_PHU_ID"])

        PHU_Location_row = [row["Reporting_PHU_ID"], row['Reporting_PHU'], row['Reporting_PHU_Address'],
                            row['Reporting_PHU_City'], row['Reporting_PHU_Postal_Code'], "ON",
                            row['Reporting_PHU_Website'], row['Reporting_PHU_Latitude'], row['Reporting_PHU_Longitude']]
        PHU_Location_dimension.loc[len(PHU_Location_dimension)] = PHU_Location_row

PHU_Location_dimension.insert(0, "PHU_surrogate_key", np.arange(len(PHU_Location_dimension)))
PHU_Location_dimension.to_csv("PHU_Location_dimension.csv", index=False)
