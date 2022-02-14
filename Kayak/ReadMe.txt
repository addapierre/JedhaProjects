Plan you trip with Kayak:
The application is deployed on [Heroku](http://kayak-app-pierre.herokuapp.com/)
The user can choose the best destination based on several weather feature:
	- the highest maximum temperature
	- the highest minimum temperature
	- the lowest amount of cloud
	- the minimum humidity
The application will send back the top 10 destinations based on one of these features. Next, the user can choose amongst these 10 destination and the application will send the top 5 hotels in this area.

All the scraping process is contained in Kayak_propre.py
The application script is in main.py