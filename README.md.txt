# Game Lab
#### Video Demo: https://youtu.be/9HBa3cqksZw
#### Description:

-Game Lab is a web application that allow you to search Free to Play and paid games ,also it recommended to you Games based on your preference.

-To access the site you need to make an account first: you can sign up and login.

-The homepage displays the 3 diffrent functions you find in the website.

1-Search Free to play Games: -by genres: more than 40 genres and you can choose multible.
			     -by platform: All, pc or browser.
			     -by sort: release date, popularity or alphabetical.
			     -

2-Search All Games: -by genres: 7 genres and you can choose multible.
		    -by tags: 8 tags and you can choose multible.

3-Game recommendation engine: -You get recommended games based on the games you have liked.
			      -You can like games when you search all games.
			      -The engine recommend by taking the top genres from the games you liked.


Langages used: -Html
	       -Css
	       -Javascript
	       -Python
	       -Flask 
	       -Ajax
	       -Sqlite3

>>app.py: 

-def index(): redirect to index.html.
-def login(): login session.
-def register(): register in the database.
-def logout(): logout from the session.
-def ftpEngine(): free to play search engine works with an api.
-def Pengine(): all games searcch engine works with an api.
-def like_game(): let you like games throug ajax.
-def user_liked_game(user_id, game_id): check if the game is already liked.
-def recommendations(): get the liked games and recommend using recommend_games function.
-def recommend_games(liked_game_ids): recommend games by taking the top genre and take the top 10 and filter out the games that is already liked.
-def get_game_genres(game_ids, api_key): return the list of the genres that the user liked.


>>helpers.py: 

-def apology(message, code=400): error message using the cat meme.
-def login_required(f): a function that checks if the user is loged in ( in session ).  


>>StartGame.db:

A data base of two tables:

1-table 1 liked: a table to store liked games with two columns user id and game id.
2-table 2 liked: a table to store users information with three columns id, username, hash ( witch is the columns to store the hash passwords ).

>>static:

<<>>photos: All photos that are used in the website.
	
-index.css: the css file that style all the templates ( html pages ).
-layout.js: all the javascript for the templates the first function is for the home page to make a transetion to all the elements to come from the left, second function find the current used page to make the navbar active page standout ( highlited white ).



>>templates:

-apology.html: apology template that display errors with the cat meme.
-ftpEngine.html: free to play template that display 5 divs including name, genres, platform, sort and search button.
-index.html: the home page that show three elements of the three engines free to play, all games, recommendation engine with three images and three descriptions and three buttons that connect you to the engines.
-layout.html: the layout for all the templates to fill in the header that include the responsive nav bar and dinamic with animations and highlited active pages and a hover effect that shows a blue line at the bottom the logo and the name game lab, the sign in sign up buttons or logout button.
-login.html: login template it is the login page.
-Pengine.html: all games template that display 4 divs including name, genres, tags and search button.
-recommendations.html: recommandation template that shows a page of divs 3 columns every div is a game and you can go back to the all games page through the games button.
-register.html: register template that displays a forum that allow you to create an account to the data base.
-resultsFTP.html: a results page for the free to play engine consist of divs 3 columns every div is a game it has the game image, the game title, the game discription, the game release date and a link to the game website or where you can buy or find the game.
-resultsP.html: a results page for the all game engine consist of divs 3 columns every div is a game it has the game image, the game title, the game rating and a like button of the game that allow you to like the game and memorise it to use it later in the recommendation engine.


