create table weather(
    surrogate_key int,
    Longitude float,
    Latitude float,
    Station_Name varchar,
    Climate_ID varchar,
    Date_Time date,
    Max_Temp float,
    Min_Temp float,
    Mean_Temp float,
    Total_Rain_mm float,
    Total_Snow_cm float,
    Total_Precip_mm float,
    weather_key varchar, 
    primary key (surrogate_key)
);

create table test_date(
    Test_date_surrogate_key int,
    Test_date_key varchar,
    Date date,
    Day int,
    Month varchar,
    Day_of_Week varchar,
    Week_in_Year varchar,
    Weekend varchar,
    Holiday varchar,
    Season varchar, 
    primary key (Test_date_surrogate_key)
);

create table onset_date(
    Onset_date_surrogate_key int,
    Onset_date_key varchar,
    Date date,
    Day int,
    Month varchar,
    Day_of_Week varchar,
    Week_in_Year varchar,
    Weekend varchar,
    Holiday varchar,
    Season varchar, 
    primary key (Onset_date_surrogate_key)
);

create table reported_date(
    Reported_date_surrogate_key int,
    Reported_date_key varchar,
    Date date,
    Day int,
    Month varchar,
    Day_of_Week varchar,
    Week_in_Year varchar,
    Weekend varchar,
    Holiday varchar,
    Season varchar, 
    primary key (Reported_date_surrogate_key)
);

create table specimen_date(
    Specimen_date_surrogate_key int,
    Specimen_date_key varchar,
    Date date,
    Day int,
    Month varchar,
    Day_of_Week varchar,
    Week_in_Year varchar,
    Weekend varchar,
    Holiday varchar,
    Season varchar, 
    primary key (Specimen_date_surrogate_key)
);

create table special_measures(
    surrogate_key int,
    Title varchar,
    City varchar,
    Start_date date,
    End_date date,
    Private_indoor_gathering_limit int,
    Private_out_door_gathering_limit int,
    Public_indoor_gathering_limit int,
    Public_outdoor_gathering_limit int,
    Indoor_religious_services_rites_or_ceremonies_limit varchar,
    Outdoor_religious_services_rites_or_ceremonies_limit int,
    mask_requird varchar,
    Self_isolating varchar,
    Essential_service varchar,
    Entertainment_service varchar,
    School_work varchar,
    Restaurant_patrons_seated_indoors varchar,
    Special_Measures_Key varchar, 
    primary key (surrogate_key)
);

create table PHU_location(
    PHU_surrogate_key int,
    PHU_id int,
    PHU_name varchar,
    Address varchar,
    City varchar,
    Postal_Code varchar,
    Province varchar,
    URL varchar,
    Latitude float,
    Longitude float, 
    primary key (PHU_surrogate_key)
);

create table patient(
    Patient_surrogate_key int,
    Patient_Key int,
    Gender varchar,
    Age_group varchar,
    Acquisition_group varchar,
    Outbreak_related varchar, 
    primary key (Patient_surrogate_key)
);

create table mobility(
    Mobility_surrogate_key int,
    Mobility_key varchar,
    Date date,
    Metro_area varchar,
    Subregion varchar,
    Province varchar,
    Retail_and_recreation float,
    Grocery_and_pharmacy float,
    Park float,
    Transit_stations float,
    Workplaces float,
    Residential float, 
    primary key (Mobility_surrogate_key)
);

create table covid19_tracking_fact_table(
    Onset_date_surrogate int,
    Reported_date_surrogate int,
    Test_date_surrogate int,
    Specimen_date_surrogate int,
    Patient_surrogate int,
    PHU_surrogate int,
    Mobility_surrogate int,
    Weather_surrogate int,
    Special_measures_surrogate int,
    Resolved int,
    Unresolved int,
    Fatal int,
    FOREIGN KEY(Onset_date_surrogate) REFERENCES onset_date(Onset_date_surrogate_key),
    FOREIGN KEY(Reported_date_surrogate) REFERENCES reported_date(Reported_date_surrogate_key),
    FOREIGN KEY(Test_date_surrogate) REFERENCES test_date(Test_date_surrogate_key),
    FOREIGN KEY(Specimen_date_surrogate) REFERENCES specimen_date(Specimen_date_surrogate_key),
    FOREIGN KEY(Patient_surrogate) REFERENCES patient(Patient_surrogate_key),
    FOREIGN KEY(PHU_surrogate) REFERENCES PHU_location(PHU_surrogate_key),
    FOREIGN KEY(Mobility_surrogate) REFERENCES mobility(Mobility_surrogate_key),
    FOREIGN KEY(Weather_surrogate) REFERENCES weather(surrogate_key),
    FOREIGN KEY(Special_measures_surrogate) REFERENCES special_measures(surrogate_key)

);