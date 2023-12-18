from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
import requests
import sqlite3


app = Flask(__name__)



app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)






db = SQL("sqlite:///StartGame.db")

@app.route("/")
def index():
    """Engine"""
    return render_template("index.html")





@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST
    if request.method == "POST":
        # User sumbit username
        username = request.form.get("username")
        # User sumbit password
        password = request.form.get("password")
        # User sumbit password confirmation
        confirmation = request.form.get("confirmation")
        # Ensure username was sumbitted
        if not username:
            return apology("Must provide username")
        # Ensure password was sumbitted
        if not password:
            return apology("Must provide password")
        # Ensure password confirmation was sumbitted
        if not confirmation:
            return apology("Must provide password confirmation")
        # Ensure password match with confirmation
        if password != confirmation:
            return apology("Password doesn't match with confirmation")
        # Hash password
        hash = generate_password_hash(password)
        # Ensure username does not exist
        username_check = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(username_check) == 1:
            return apology("Username has already used")
        # Add to database username and password
        register = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        # Create session for user
        session["user_id"] = register
        # Flash message
        flash("Registred")
        # Redirect user to home page
        return redirect("/")
    # User reached route via GET
    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/ftpEngine", methods=["GET","POST"])
@login_required
def ftpEngine():
    # User reached route via POST
    if request.method == "POST":
        # User sumbit genres
        genres = request.form.getlist("genres")
        # User sumbit sort of games list
        sort = request.form.get("sort")
        # User sumbit platform
        plat = request.form.get("plat")

        # Ensure genres was sumbitted
        if not genres:
            return apology("Must provide genre")
        
        # joining  genres names together 
        categories = ".".join(genres)

        # search in api for games like sumbitted genres and platform sorted by sumbitted order
        url = url = "https://free-to-play-games-database.p.rapidapi.com/api/filter"
        querystring = {"platform":plat,"tag":categories,"sort-by":sort}

        headers = {
	    "X-RapidAPI-Key": "617f13c16bmsh7a1a7caf483885cp135ae1jsn695604572a12",
	    "X-RapidAPI-Host": "free-to-play-games-database.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        # get api results and make every information in a variable 
        if response.status_code == 200:
            data = response.json()
            title = [game["title"] for game in data]
            image = [game["thumbnail"] for game in data]
            info = [game["short_description"] for game in data]
            game_url = [game["game_url"] for game in data]
            date = [game["release_date"] for game in data]
            return render_template("resultsFTP.html", title=title, image=image, info=info, game_url=game_url, date=date)
        else:
            return apology("Games doesn't exist for your choices")
    # User reached route via GET
    else:
        # List of genres to display in search page
        GENRESFREE = [
            "mmorpg", "shooter", "strategy", "moba", "racing", "sports", "social", "sandbox", "open-world", "survival", "pvp", "pve", "pixel", "voxel", "zombie", "turn-based", "first-person", "third-Person", "top-down", "tank", "space", "sailing", "side-scroller", "superhero", "permadeath", "card", "battle-royale", "mmo", "mmofps", "mmotps", "3d", "2d", "anime", "fantasy", "sci-fi", "fighting", "action-rpg", "action", "military", "martial-arts", "flight", "low-spec", "tower-defense", "horror", "mmorts"
        ]

        genres_dict = {genre: index for index, genre in enumerate(GENRESFREE, start=1)}
        
        return render_template("ftpEngine.html", genres_dict=genres_dict)



@app.route("/Pengine", methods=["GET","POST"])
@login_required
def Pengine():
    # User reached route via POST
    if request.method == "POST":
        # User sumbit genres
        genres = request.form.getlist("genres")
        # User sumbit tags
        tags = request.form.getlist("tags")
        # User sumbit sorting order
        sort = request.form.get("sort")
        # Ensure genres was sumbitted
        if not genres:
            return apology("Must provide genre")
        # get user id to pass it to saerch page and save user likes
        user_id = session["user_id"]
        # search in api for games like sumbitted genres and tags sorted by sumbitted order
        url = 'https://api.rawg.io/api/games'

        params = {
            'key': "4c6277f83647443089966c6bb22ec90b", 
            'genres': genres,
            'tags': tags,
            'ordering': f'-{sort}',
        }
        response = requests.get(url, params=params)
        # get api results 
        if response.status_code == 200:
            data = response.json()
            games = data.get('results', [])
            return render_template("resultsP.html", games = games,  user_id=user_id)
        else:
            return apology("Games doesn't exist for your choices")
    # User reached route via GET
    else:
        GENRESFREE = [
            "shooter", "strategy", "racing", "sports", "card", "fighting", "action"
        ]
        TAGSFREE = [
            "open-world", "singleplayer", "multiplayer", "coop", "pvp", "pve", "online", "story-rich"
        ]

        TAGS_dict = {tags: index for index, tags in enumerate(TAGSFREE, start=1)} 

        genres_dict = {genre: index for index, genre in enumerate(GENRESFREE, start=1)} 

        return render_template("Pengine.html", genres_dict=genres_dict, TAGS_dict=TAGS_dict,)
    
    


@app.route("/like_game", methods=["POST"])
@login_required
def like_game():
    # User reached route via POST
    if request.method == "POST":
        try:
            # Get id of games liked by the user
            game_id = request.json.get("game_id")  
            # get user id 
            user_id = session["user_id"]

            # Check if the user has already liked the game
            if not user_liked_game(user_id, game_id):
                # Insert liked game id into the table of liked games
                db.execute("INSERT INTO liked (user_id, game_id) VALUES (?, ?)", user_id, game_id)
                # Set liked to True
                liked = True  
                message = "Game liked successfully"
            else:
                # Delete unliked game id from the table of liked games
                db.execute("DELETE FROM liked WHERE user_id = ? AND game_id = ?", user_id, game_id)
                # Set liked to False
                liked = False  
                message = "Game unliked successfully"
            # Return a JSON response to indicate success and the updated liked status
            response_data = {
                "message": message,
                "liked": liked
            }
            return jsonify(response_data), 200
        except :
            return jsonify({"error": "Database error"}), 500



def user_liked_game(user_id, game_id):
    # counts the number of liked game id in the liked table
    conn = sqlite3.connect('StartGame.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM liked WHERE user_id = ? AND game_id = ?", (user_id, game_id))
    result = cursor.fetchone()
    conn.close()
    return result[0] > 0


@app.route("/recommendations", methods=["GET"])
@login_required
def recommendations():
    # get user id 
    user_id = session["user_id"]  

    # Fetch liked games from the database
    conn = sqlite3.connect('StartGame.db')
    cursor = conn.cursor()
    like = cursor.execute("SELECT game_id FROM liked WHERE user_id = ?", (user_id,))
    liked_game_ids = [row[0] for row in like.fetchall()]
    cursor.close()
    conn.close()

    # a simple recommendation algorithm that search similar games based on genres
    recommendations  = recommend_games(liked_game_ids)

    if not recommendations:
        return apology("You should like games first")

    return render_template("recommendations.html", recommendations=recommendations) 


def recommend_games(liked_game_ids):
    # Set up your RAWG API key
    api_key = '4c6277f83647443089966c6bb22ec90b'

    # Fetch the genres of liked games
    liked_game_genres = get_game_genres(liked_game_ids, api_key)
    
    # No genres found for liked games
    if not liked_game_genres:
        return None

    # Fetch games from the API based on genres
    recommended_games = []
    
    for genre in liked_game_genres:
        url = f'https://api.rawg.io/api/games?key={api_key}&genres={genre}&page_size=10'
        response = requests.get(url)
        # get api results
        if response.status_code == 200:
            data = response.json()
            games = data.get('results', [])
            
            # Filter out games that are already liked
            games = [game for game in games if game['id'] not in liked_game_ids]
            
            recommended_games.extend(games)

    return recommended_games[:10]

def get_game_genres(game_ids, api_key):
    # initializes an empty set
    game_genres = set()
    # iterate through each game id in game_ids list
    for game_id in game_ids:
        url = f'https://api.rawg.io/api/games/{game_id}?key={api_key}'
        response = requests.get(url)
        # extracts the 'genres' field from the JSON data
        if response.status_code == 200:
            data = response.json()
            genres = data.get('genres', [])
            # extracts the 'slug' field from each genre
            for genre in genres:
                game_genres.add(genre['slug'])
    
    return list(game_genres)



if __name__ == '__main__':
    app.run(debug=True)
