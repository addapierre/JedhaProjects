# Uber App:
App deployed on [Heroku](https://uber-clustering.herokuapp.com)
This application performs **kmean clustering** on uber position logs in New York.
The user can choose the *month*, the *week day* and the *time window* of the logs.
The app then proceeds to automatically calculate the best elbow and silhouette for the logs in this timeframe.
Since Heroku free tier does not grant enough memory to perform KMeans within its fixed time limit, all the calculus is performed in an **AWS Lambda** function called with an API.
The lambda function is deployed using a docker image built in docker_lambda folder.
The dash app that is actually deployed on heroku (and calls the lambda via API), is main.py

