Here we gather and transform the data and finally we train a NN.

GAMES dataset
The games data have been downloaded from this dataset:
	https://data.world/dcereijo/player-scores
It contains 40k+ games from European tournaments with 20k+ individual players

FIFA dataset
The Fifa game player scores data have been downloaded from this kaggle dataset:
	https://www.kaggle.com/stefanoleone992/fifa-22-complete-player-dataset
It contains all player scores from FIFA15 to FIFA22.

Data transformation:
	The first and main difficulty for this data transformation is to match players name between several datasets. Players have often different name spelling, different nicknames that are used or not and it is not a trivial task. We used the players birthday to help ourself but even the birthdays are often mistyped, the most recurrent error being the inversion of day and month (confusion between the american and european notation).
We managed to do this using levenshtein scores, which calculate a "distance" between 2 strings. That way we were able to match somewhat similar names. However, some work should still be done by hand and it IS time consuming. At the end, we were able to match more than 16k players between the FIFA dataset and the GAMES dataset. 
	The process described above can be found in the ETL folder. name_matching_DoB.ipynb applied name matching on players having the same date of birth, while name_matching_no_DoB.ipynb did the same thing but each time on the whole dataset.
the results obtained with these two notebooks were used in table_correspondance.ipynb to create a correspondence table to help us match players from the two datasets.

Feature engineering:
	In feature engineering, we prepared the data to be used by the model. We found out that with the obtained correspondance table, we are able to get ~32k games with at least 6 players that we "know" in each teams. 
	The teams are divided into 3 categories (Attack, Midfield and Defense) + the goalkeeper. the score of players from each category is averaged as an imputing strategy for missing players. more details in feature_engineering/feature_engineering_suite.ipynb
	