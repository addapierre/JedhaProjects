Walmart weekly sales predictor.

Data exploration and visualisation:
  There is actually very few data (150 instances) and a lot of missing data (around 10%). 
  Visualisation revealed no visible correlation between explanatory data, except between Fuel price and Year. We decided to keep these features nonetheless (significant dispersion in fuel price).

Pretreatment:
First we divided the Date into Day, Month, Year and DayofWeek

  Because of the very limited amount of data, imputing missing data must be privileged over deleting row (except for missing target which have been deleted). 
- We imputed the temperature according to the average temperature over the same month.
- We imputed the fuel price according to the average fuel price over the same year. When there was no date informed, we imputed according to the average fuel price for the same store.
- We imputed CLI and unemployment according to their average values for the same store, as these values depend mainly on the location.
Then we removed the outliers using (mean ± 3* std). It turns out there were only 5 outliers in the unemployment columns.

Finally we encoded the categorical features using one hot encoding, and standardized the numerical features with StandardScaler.

Model training. 
Our baseline (linear regression) has an R2 score of: train_R2 =  0.975 and test_R2 = 0.944
With ridge regression, after a grid search, we found very minimal improvement with the best alpha = 0.041 and train_R2 =  0.974 and test_R2 = 0.947
With lasso also, best alpha = 613, train_R2 =  0.974 and test_R2 = 0.948


