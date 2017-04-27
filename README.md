High level description of project:

San Francisco 311-call request resolving time prediction.

Aim of the project:

Development of a predictive model to determine the time of resolving a 311-call request based on various features, such as the description, location, submission time, and corresponding agency of the request.

Data source:

Data is obtained from San Francisco public dataset and the data is heterogenous.
Responsible Agency: 409
 Category: 28 
Neighborhood: 126

Overall mean time of resolving requests is 33.3 days with standard deviation of 128 days
Min: less than 10 minutes (e.g., Noise Report)
Max: over 5 years (e.g., Fix a collapsed_sidewalk)

Brief description of data analysis pipeline:

  1. Data cleaning
     1.1 Remove invalid and duplicated cases
     1.2 Deal with missing data
          a) Fill missing categorical entries with new value - 'Missing value'
          b) Imputation of missing 'neighborhood' using K-nearest neighborhood algorithm (accuracy of 0.89)

  2. Feature engineering
     2.1 Generation of feature 'Request topic' using NLP, K-means clustering
     2.2 Generation of time related features, including 'Year', 'Month', 'Weekend', 'Holiday'

  3. Model development
     3.1 Development of linear regression model as the baseline model
     3.2 Development of Aalen's additive survival models
     3.3 Development of random forest regression model
     3.4 Development of gradient boosting regression model

Description of model evaluation:
                                         R2
linear regression model                 0.11
Aalen's additive model                  0.10
random forest regression model          0.55
gradient boosting regression model      0.51

Feature importance:
'Request topic', 'Response Agency', 'Neighborhood', 'Year'

Analysis of 'Year' feature leads to the discover of a interesting pattern. The mean resolving time of 311 request started to decrease after 2010, coinsidence with the starting time of incorporation of data driven techniques into San Francisco 311 program management. 2010 was also the year that San Francisco 311 program received 'Largan Innovation Award'.

Summary
Random forest model performs well when modeling heterogenous data.

Data driven techniques may contribute to the increase of work efficiency of San Francisco 311 program.
