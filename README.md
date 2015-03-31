# Uber-Challenge
Application to find nearby food trucks and their cuisines in San Francisco.

Problem:
Food Trucks: Create a service that tells the user what types of food trucks might be found near a specific location on a map.

Solution:
- The solution focuses on back-end.

- Technologies:
    * Python (Familiar with the language, mostly used for scripting. Easy to use with mongodb and flask.)
    * MongoDb (No experience. Used for this project as it supports geospatial queries and is easy to setup.)
    * Flask (No experience. Easy to use and learn web development framework.)
    * Memcache (No experience. A popular cache for web frameworks, being used to store results from the Google Places API.)
    * Google Places API (Used to geocode the provided address.)
    * Google Maps (Modified pygmaps to suit the needs for markers, hovering and infowindows.)

- Implementation:
    * dataProcessor.py - Downloads food trucks dataset, processes the raw data and creates a mongodb table. Also, creates indices on "Location" and "Food Items" attributes.
    * app.py - Implements most of the web app. Renders a form on the index page to get address (the only required field), distance (radius for searching food trucks) and food items from the users. Fetches results from the database, marks the location on map and adds info windows. If you hover over the marker, you can see the name of the food truck. If you click on the marker, you can see the food items provided by the food truck. (It assumes that you are using a modern browser like Chrome, Firefox or Safari.)
- Attempted to host it on Heroku, but could not get it working. The app started fine locally but timed out while starting on Heroku.

- Given more time, I would attempt to add support for:
    * handling multiple web requests simultaneously.

How to use:
- pip install -r requirements.txt
- cd webapp/
- python app.py
- In the browser, open http://127.0.0.1:5000/
- Put in an address (For instance: Kings Street, SF), select distance(optional) and food items(optional) and hit submit
- You can hover over the markers on the map to know the food truck name
- You can click on the marker to see the food items at the food truck

