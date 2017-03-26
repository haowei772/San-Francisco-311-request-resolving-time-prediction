Data cleaning procedure:

1. Read data from SF311.csv (2092917 cases).

1.1. Parse dates of 'Opened', Closed','Updated' to pd.datetime64.

1.2. Sort the data by CaseID in asceding order, which is the same order by case open time.

1.3. Remove 99549 open cases (with no closed time/status==open), these cases are stored in SF311_still_open_raw.csv.

2. There are 1993368 cases left that are closed.

2.1. Calculate the 'Process_days', a time_delta object, by ('Closed' - 'Opened').

2.2. Creat 'Process_hours' (data type is float) by converting 'Process_days' to hours.

2.3. Remove the cases with process time <= 0hr(23575 cases). These cases are stored in SF311_wrong_dates_raw.csv. There are The rest valide 1969793 cases left.

2.4. Remove the duplicated cases (34773 cases). These cases are stored in SF311_duplictates_raw.csv.

2.4. The rest valide 1935020 cases were stored in SF311_valid_raw.csv

3. For the 1935020 valid cases conitue data cleaning process.

3.1. Remove columns: 'Updated','Status', 'Media URL', becuase these columns offer no helpful information. 'Upated' is basically the time for closed or some time between open and closed, which does not offer any useful information. 'Status' is redundent because only closed cases are used in the project. 'Media URL' has too many missing values 1712026 cases.

3.2. Save these cases to SF311_valid_reduced.csv @.

4. Feature engineering (add new features). (Use a pilot subset of data, 100,000 for feature engineering and modeling)

4.1. Add column Day_Of_Week, indicating the day of the week: 0 to 6 for Monday to Sunday, respectively.

4.2. Add column Month, indicating the which month: 0 to 6 for Monday to Sunday, respectively.

4.3. Add column Weekend, indicating if the case is opened on weekend: 1 for True and 0 for False

4.4. Add column Holiday, indicating if the case is opened on federal holiday: 1 for True and 0 for False (41063 cases).

4.5. Add column Before_Holiday, indicating if the case is opened one day before federal holiday: 1 for True and 0 for False (41095 cases). The dataset has 19 columns.

4.5. Save dataset to csv file as SF311_engineered.csv

4.6. Create a pilot dataset of most recent 100000 cases for preliminary modeling and feature engineering, save as SF311_pilot.csv

4.5. Add the column Current_Open, which has the number of current open cases (this process is computational intensive, so try it with the pilot dataset first.

5. Deal with missing data.

5.1. Impute the missing neighorhood data using KNN.



@ Saving to csv file convert 'Process_days' a time-delta object to string. I will use 'Process_hours' not 'Process_days' for further calculation, the later is just for easy assessment of time.
