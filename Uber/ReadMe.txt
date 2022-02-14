Uber App:
App deployed on [Heroku](https://uberappdepierre.herokuapp.com/)
This application performs kmean clustering on uber position logs in New York.
The user can choose the month, the week day and the time window.
The app then proceeds to automatically calculate the best elbow and silhouette for the logs in this timeframe.

main_copy.py can be executed with python to deploy an offline dashboard using Dash that does exactly what is described above.
main.py is the online application. 

IMPORTANT NOTE: 
The free version of heroku used here is very slow, and has a timeout of 30s. The automatic elbow calculation performs 11 kmeans in a row, which is amounts to much more than 30s with the free version of heroku.
However, we found a workaround (not very user friendly though), the user has to click on submit, wait for the elbow figure to update with only the first value of kmean. Then the user has to click once more on submit to calculate the second kmean, and so on and so forth until the 11 kmeans are performed. 