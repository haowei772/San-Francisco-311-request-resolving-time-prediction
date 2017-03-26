Data cleaning procedure:
Read data from SF311.csv (2092917 cases).
1.1. Parse dates of 'Opened', Closed','Updated' to pd.datetime64.
1.2. Sort the data by CaseID in asceding order, which is the same order by case open time.
1.3. Remove 99549 open cases (with no closed time/status==open), these cases are stored in SF311_still_open_raw.csv.
There are 1993368 cases left that are closed.
2.1. Calculate the 'Process_days', a time_delta object, by ('Closed' - 'Opened').
2.2. Creat 'Process_hours' (data type is float) by converting 'Process_days' to hours.
2.3. Remove the cases with process hours <= 0hr(23575 cases). These cases are stored in SF311_wrong_dates_raw.csv. There are The rest valide 1969793 cases left.
2.4. Remove the duplicated cases (34773 cases). These cases are stored in SF311_duplictates_raw.csv.
2.4. The rest valide 1935020 cases were stored in SF311_valid_raw.csv
For the 1935020 valid cases conitue data cleaning process.
3.1. Remove columns: 'Updated','Status', 'Media URL', becuase these columns offer no helpful information. 'Upated' is basically the time for closed or some time between open and closed, which does not offer any useful information. 'Status' is redundent because only closed cases are used in the project. 'Media URL' has too many missing values 1712026 cases.
3.2. Convert 'Process_days' a time-delta object to float. Save these cases to SF311_valid_reduced.csv.
Feature engineering (add new features). (Use a pilot subset of data, 100,000 for feature engineering and modeling)
4.1. Add column Day_Of_Week, indicating the day of the week: 0 to 6 for Monday to Sunday, respectively.
4.2. Add column Month, indicating the which month: 0 to 6 for Monday to Sunday, respectively.
4.3. Add column Year, 2008 to 2016.
4.4. Add column Weekend, indicating if the case is opened on weekend: 1 for True and 0 for False
4.5. Add column Holiday, indicating if the case is opened on federal holiday: 1 for True and 0 for False (41063 cases).
4.6. Add column Before_Holiday, indicating if the case is opened one day before federal holiday: 1 for True and 0 for False (41095 cases). The dataset has 19 columns.
4.7. Add column Opened_Int which casts the Opened datetime object to int
4.8. Save dataset to csv file as SF311_engineered.csv
4.9. Plot the Process days over time and find the linearly decreasing trend of maximum job length over the time span. There are two potential factors contributing to this observation. 1) The maximum job length appearently decreases because long jobs last long and for the later opened cases they may not be closed at the time of inspection. When I exclude the still open cases, some of those possible long jobs are excluded, making the maximum job length shorter for those more recent cases. 2) The city has improved the cival service. To determine if the second factor is a contributor, I need to look at a truncated dataset. The strategy is to investigate the cases with maximum job length of 2 years from 2008 July upto 2015 March (2 years earlier from the current data collecting point) of tatal 1175726 cases. In this way, all cases in this interval will have chance to be finished. Dataset is stored in csv file SF311_chunk.csv.
Still see strong trend of decreasing mean job length in the truncated dataset, suggesting that the reduction of the job length (within the job that length < 2 years) is significant not an artifact created by sampling. The variable year can cetainly explain part of this trend, so it can be used in a random forest model. Another option is to create a continue time variable nth month (0 to from 2008 July to the data collecting point), or include a continue time variable Opend_int, which is basically transfer the datetime object to an int. All these can be included in the random forest model.
Also need to inspect the histogram of cases that are still open.
Did one-way ANOVA on Process_days on year in the full and truncated dataset. Both datasets yielded p-value of 0.0, indicating the difference among years are significantly different.
4.10. Create a pilot dataset of 100000 cases (from begining) for preliminary modeling and feature engineering, save as SF311_pilot.csv
4.11. Add the column Current_Open, which has the number of current open cases (this process is computational intensive, so try it with the pilot dataset first, not done yet).

Data cleaning and modeling procedure:

5. Deal with missing data. Be sure not to us any information gloabally to impute missing value at this stage, because before the test-train split, using gloabal information to impute missing values leads to a data leakage!
********* Number of missing values **********
Status Notes   648795
Request Type   13352
Request Details   70431
Address   11
Supervisor District   8945
Neighborhood   123235
Point   66545
**********************************************
There are 7 features with missing data that may have impact on modeling.
The initial strategy for Request Type is to copy the Request Details to Request Type. But only 7 values can be copied because 13345 out of 13352 cases they are both missing. Decide to add 'Missing' as Request Type.

Strategy for Neighborhood is to use KNN and valid Point to impute the missing values.
Strategy for Supervisor District is to find the Neighborhood or Point, and use KNN to impute missing value; another simpler strategy is to impute -1, which is already used in the dataset.
Strategy for Address is to add 'Missing' as address; there are only 11 records missing; also may not use address in initial modeling.
Have no strategy for Point and Status Notes because will not use Point and Status Notes for modeling.

5.1. Deal with missing Request type and details.
both request type and details are missing:  13345
only request type not details is missing:  7
only request details but not type is missing:  57086

Three steps:
A. Copy Request Details to missing Request Type and fill 7 missing values.

B. Fill missing Request Type with 'Mssing'.

C. Copy Request Types to missing Request Details.

5.2. Save filled df to csv file named SF311_fill.csv

5.3. Plan to use KNN for imputing the neighborhood, but before doing it I need to split the dataset into train-valid and test set, because KNN will use information from the whole dataset, lead to a data leakage.
Right now, for building the initial model, I will simply impute missing Supervisor District as -1.0, and missing Neighborhood as 'MissingNeighborhood'.

5.4. Save dataset with missing values filled to csv file named 'SF311_fill.csv'.

6. Train_test split and save the file.

6.1. Generate a 80-20% train-test split of filled dataframe, save them to csv file. The purpose of this split is not to create the X_train, X_test, y_train, y_test datasets. It just split the dataset to train and test. Will use train for further split into training and valisdation datasets with X and y seperated.

6.2. Save generated dataframes to 'SF311_train.csv' and 'SF311_test.csv'

7. Premodeling process.

7.1. Reduced the dataframe by select the useful columns, including the target column and other useful features: 'Responsible Agency', 'Category', 'Request Type', 'Supervisor District', 'Neighborhood', 'Source', 'Process_days',  'Day_Of_Week', 'Month', 'Year', 'Weekend', 'Holiday', 'Before_Holiday', 'Opened_Int'.

7.2. Scale Opened_Int variable: dividing it by 10^16.

7.3. Convert categorical features to numerical variables, including 'Category','Responsible Agency','Request Type','Neighborhood','Source'.

7.4. Split the training dataframe to training and validation sets (ratio 7:3), yielding dataframes and series of X_train, X_test, y_train, y_test ready for modeling.

8. Modeling and cross-validation.

8.1. Simple model using mean of y_train for predicted value. Get Mean_square_error(MSE) of mean_model: 17439.1.

8.2. Linear regression model. Get r_square: 0.137817479254; MSE: 15035.52; Conclusion: linear regression is not a good model for the dataset.

8.3. RandomForest regressor model. RandomForestRegressor with n_estimators=100 get r_square: 0.5544, oob_score: 0.539 and MSE: 7770.96.

Get the rank of feature importance based on the preliminary random forest model. The top 6 features from high to low: Open_time, Request type, Resposible agency, Neighborhood, District, Category.

8.4. Gradient boosting Regressor model. Runed with three configirations:
GradientBoostingRegressor: n_estimators=100, learning_rate=0.1
r_square:  0.4041, MSE:  10391.96

GradientBoostingRegressor: n_estimators=300, learning_rate=0.1
r_square:  0.4493 MSE:  9604.32

GradientBoostingRegressor: n_estimators=600, learning_rate=0.1
r_square:  0.4785, MSE:  9094.79

Get the rank of feature importance based on the preliminary Gradient boosting model. Get the save results as top 6 features: Open_time, Request type, Resposible agency, Neighborhood, District, Category.

8.5 Survival Model: Aalen Additive Model. Reorganize the data for fitting the the AAF model.
