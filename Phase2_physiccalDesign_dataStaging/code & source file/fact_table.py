import pandas as pd
import numpy as np

Onset_Date_dimension = pd.read_csv("Onset_Date_dimension.csv")
Reported_Date_dimension = pd.read_csv("Reported_Date_dimension.csv")
Test_Date_dimension = pd.read_csv("Test_Date_dimension.csv")
Specimen_Date_dimension = pd.read_csv("Specimen_Date_dimension.csv")
patient_dimension = pd.read_csv("patient_dimension.csv")
Mobility_dimension = pd.read_csv("Mobility_dimension.csv")
weather_dimension = pd.read_csv("weather_dimension.csv")
PHU_Location_dimension = pd.read_csv("PHU_Location_dimension.csv")
Special_Measures_dimension = pd.read_csv('special_measures_dimension.csv')
covid = pd.read_csv("Confirmed_Positive_Cases_ON.csv")

# print(Onset_Date_dimension.head())
# print(Reported_Date_dimension.head())
# print(Test_Date_dimension.head())
# print(Specimen_Date_dimension.head())
# print(special_measures_dimension.head())
# print(patient_dimension.head())
# print(Mobility_dimension.head())
# print(weather_dimension.head())
# print(PHU_Location_dimension.head())

fact_table = pd.DataFrame(
    columns=['Onset_date_key', 'Reported_date_key', 'Test_date_key', 'Specimen_date_key',
             'Patient_Key', 'PHU_id', 'Mobility_key', 'Weather_Key', 'Special_Measures_Key',
             'Resolved', 'Unresolved', 'Fatal'])

count = 0
for idx, row in covid.iterrows():
    if int(row['Accurate_Episode_Date'][0:4]) == 2020 \
            and int(row['Accurate_Episode_Date'][5:7]) >= 9 \
            and int(row['Case_Reported_Date'][0:4]) == 2020 \
            and str(row['Test_Reported_Date']) != "nan" \
            and str(row['Specimen_Date']) != "nan" \
            and (row['Reporting_PHU'] == "Ottawa Public Health" or
                 row['Reporting_PHU'] == "Toronto Public Health" or
                 row['Reporting_PHU'] == "Durham Region Health Department" or
                 row['Reporting_PHU'] == "Halton Region Health Department" or
                 row['Reporting_PHU'] == "Peel Public Health" or
                 row['Reporting_PHU'] == "York Region Public Health Services"):

        if row['Reporting_PHU'] == "Ottawa Public Health":
            row['Reporting_PHU'] = "Ottawa"
        elif row['Reporting_PHU'] == "Toronto Public Health":
            row['Reporting_PHU'] = "Toronto"
        elif row['Reporting_PHU'] == "Durham Region Health Department":
            row['Reporting_PHU'] = "Durham"
        elif row['Reporting_PHU'] == "Halton Region Health Department":
            row['Reporting_PHU'] = "Halton"
        elif row['Reporting_PHU'] == "Peel Public Health":
            row['Reporting_PHU'] = "Halton"
        elif row['Reporting_PHU'] == "York Region Public Health Services":
            row['Reporting_PHU'] = "York"

        fact_row = [Onset_Date_dimension[Onset_Date_dimension['Date'] ==
                                         row['Accurate_Episode_Date'][:10]]['Onset_date_key'].to_string(index=False),
                    Reported_Date_dimension[Reported_Date_dimension['Date'] ==
                                            row['Case_Reported_Date'][:10]]['Reported_date_key'].to_string(index=False),
                    Test_Date_dimension[Test_Date_dimension['Date'] ==
                                        row['Test_Reported_Date'][:10]]['Test_date_key'].to_string(index=False),
                    Specimen_Date_dimension[Specimen_Date_dimension['Date'] ==
                                            row['Specimen_Date'][:10]]['Specimen_date_key'].to_string(index=False),
                    row['Row_ID'],
                    row['Reporting_PHU_ID'],
                    Mobility_dimension[(Mobility_dimension['Subregion'] == row['Reporting_PHU']) &
                                       (Mobility_dimension['Date'] == row['Case_Reported_Date'][:10])]
                    ['Mobility_key'].to_string(index=False),
                    weather_dimension[(weather_dimension["Date_Time"] == row['Case_Reported_Date'][:10]) &
                                      (weather_dimension["Station_Name"] == row['Reporting_PHU_City'])]
                    ["Weather_Key"].to_string(index=False),
                    Special_Measures_dimension[(Special_Measures_dimension["City"] == row['Reporting_PHU']) &
                                               (Special_Measures_dimension['Start_date'] < row['Case_Reported_Date'][
                                                                                           :10]) &
                                               (Special_Measures_dimension['End_date'] > row['Case_Reported_Date'][
                                                                                         :10])]
                    ["Special_Measures_Key"].to_string(index=False)
                    ]
        if row['Outcome1'] == "Resolved":
            fact_row += [1, 0, 0]
        elif row['Outcome1'] == "Not Resolved":
            fact_row += [0, 1, 0]
        elif row['Outcome1'] == "Fatal":
            fact_row += [0, 0, 1]
        else:
            fact_row += [None, None, None]

        count += 1
        print("current at", idx)
        print(count, 'added')
        fact_table.loc[len(fact_table)] = fact_row

fact_table = fact_table.replace('Series([], )', "")
fact_table.to_csv("fact_table.csv", index=False)

final_fact_table = pd.DataFrame(
    columns=['Onset_date_surrogate', 'Reported_date_surrogate', 'Test_date_surrogate', 'Specimen_date_surrogate',
             'Patient_surrogate', 'PHU_surrogate', 'Mobility_surrogate', 'Weather_surrogate',
             'Special_measures_surrogate', 'Resolved', 'Unresolved', 'Fatal'])

countt = 0
for idx, row in fact_table.iterrows():
    fact_row = [
        Onset_Date_dimension[Onset_Date_dimension["Onset_date_key"] ==
                             row["Onset_date_key"]]["Onset_date_surrogate_key"].to_string(index=False),
        Reported_Date_dimension[Reported_Date_dimension["Reported_date_key"] ==
                                row["Reported_date_key"]]["Reported_date_surrogate_key"].to_string(index=False),
        Test_Date_dimension[Test_Date_dimension["Test_date_key"] ==
                            row["Test_date_key"]]["Test_date_surrogate_key"].to_string(index=False),
        Specimen_Date_dimension[Specimen_Date_dimension["Specimen_date_key"] ==
                                row["Specimen_date_key"]]["Specimen_date_surrogate_key"].to_string(index=False),
        patient_dimension[patient_dimension["Patient_Key"] ==
                          row["Patient_Key"]]["Patient_surrogate_key"].to_string(index=False),
        PHU_Location_dimension[PHU_Location_dimension["PHU_id"] ==
                               row["PHU_id"]]["PHU_surrogate_key"].to_string(index=False),
        Mobility_dimension[Mobility_dimension["Mobility_key"] ==
                           row["Mobility_key"]]["Mobility_surrogate_key"].to_string(index=False),
        weather_dimension[weather_dimension["Weather_Key"] ==
                          row["Weather_Key"]]["surrogate_key"].to_string(index=False),
        Special_Measures_dimension[Special_Measures_dimension["Special_Measures_Key"] ==
                                   row["Special_Measures_Key"]]["surrogate_key"].to_string(index=False),
        row["Resolved"],
        row["Unresolved"],
        row["Fatal"]

    ]
    countt += 1
    print("second current at", idx)
    print(countt, 'checked')

    final_fact_table.loc[len(final_fact_table)] = fact_row

final_fact_table = final_fact_table.replace('Series([], )', "")
final_fact_table.to_csv("final_fact_table.csv", index=False)
