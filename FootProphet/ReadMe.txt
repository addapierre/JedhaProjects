FootProphet:
This project's aim is to predict the outcome of a football game (win, loose, or draw) using a neural network trained on a variety of different features describing a game.
The originality of this project is that it aims at using the Fifa scores of the players on the field to describe a game, which has to our knowledge not have been done before.

The Fifa franchise is well known for doing a very thorough and up to date notation of a wide variety of players, over a wide variety of characteristics and skills (visit www.sofifa.com for more details). The objective of this project is to use these informations, alongside the usual features for game prediction (i.e. the n latest results for each teams) to obtain the best possible game predictions.

For the moment, the project has been divided into 2 parts:
	PART 1 is where the data are gathered, transformed, and the model trained. There were some major issues concerning data transformation that were overcame. More details in part 1 readme.
	
	PART 2 is were we gather and transform data for prediction. We want to predict the result of franchise ligue 1 using the latest team composition (i.e. the players that played during the latest game). Therefore in this part we scrape data from lequipe.fr to get not only the team composition, but also the player's position on the field. We also scrape the player's sofifa stats from sofifa.com, and then prepare the data for the game prediction.