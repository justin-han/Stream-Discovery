# Stream-Discovery
A web application that finds small streamers on Twitch made using Python, Flask, and the Twitch API.

For the backend, I used Python and the Twitch API to find streamers based on the game. The streamers are filtered by amount of viewers to be 1000 or less. It is then sorted based on the amount of past broadcasts they had in recent months. Active streamers will have more past broadcasts compared to the less active. The more active streamers are at the top of the list when searched.

For the frontend, I used Flask with HTML and CSS. I created a sleak search bar using CSS. The streamers have a card with their name, stream title, viewer count, and a direct link to their stream.
