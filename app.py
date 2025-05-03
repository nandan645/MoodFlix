from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Your Bearer token (keep it secure)
load_dotenv()
TMDB_BEARER_TOKEN = os.getenv("TMDB_BEARER_TOKEN")

headers = {
    "accept": "application/json",
    "Authorization": TMDB_BEARER_TOKEN
}

def get_genres():
    url = f"{TMDB_BASE_URL}/genre/movie/list"
    params = {"language": "en-US"}
    response = requests.get(url, headers=headers, params=params)
    genres = {}
    if response.ok:
        data = response.json()
        for genre in data.get("genres", []):
            genres[genre["id"]] = genre["name"]
    return genres

def get_top_movies():
    movies = []
    url = f"{TMDB_BASE_URL}/trending/all/day"
    params = {"language": "en-US", "page": 1}
    response = requests.get(url, headers=headers, params=params)
    if response.ok:
        data = response.json()
        genres_lookup = get_genres()
        for movie in data.get("results", [])[:10]:
            title = movie.get("title")
            poster_path = movie.get("poster_path")
            poster_url = TMDB_IMAGE_BASE_URL + poster_path if poster_path else ""
            description = movie.get("overview")
            release_date = movie.get("release_date", "")
            year = release_date.split("-")[0] if release_date else "N/A"
            movie_genres = [genres_lookup.get(genre_id, "Unknown") for genre_id in movie.get("genre_ids", [])]
            movies.append({
                "title": title,
                "poster": poster_url,
                "description": description,
                "genres": ", ".join(movie_genres),
                "year": year
            })
    return movies

@app.route("/", methods=["GET", "POST"])
def index():
    search_query = request.form.get("query", "")
    # For now, both search and default display use the top movies list.
    recommended_movies = get_top_movies()
    return render_template("index.html", movies=recommended_movies)

@app.route("/popular-movies", methods=["GET"])
def popular_movies():
    url = f"{TMDB_BASE_URL}/movie/popular"
    params = {"language": "en-US", "page": 1}
    response = requests.get(url, headers=headers, params=params)
    movies = []
    if response.ok:
        data = response.json()
        genres_lookup = get_genres()
        for movie in data.get("results", [])[:10]:
            title = movie.get("title")
            poster_path = movie.get("poster_path")
            poster_url = TMDB_IMAGE_BASE_URL + poster_path if poster_path else ""
            description = movie.get("overview")
            release_date = movie.get("release_date", "")
            year = release_date.split("-")[0] if release_date else "N/A"
            movie_genres = [genres_lookup.get(genre_id, "Unknown") for genre_id in movie.get("genre_ids", [])]
            movies.append({
                "title": title,
                "poster": poster_url,
                "description": description,
                "genres": ", ".join(movie_genres),
                "year": year
            })
    return render_template("index.html", movies=movies)

@app.route("/popular-shows", methods=["GET"])
def popular_shows():
    url = f"{TMDB_BASE_URL}/tv/popular"
    params = {"language": "en-US", "page": 1}
    response = requests.get(url, headers=headers, params=params)
    shows = []
    if response.ok:
        data = response.json()
        genres_lookup = get_genres()
        for show in data.get("results", [])[:10]:
            title = show.get("name")
            poster_path = show.get("poster_path")
            poster_url = TMDB_IMAGE_BASE_URL + poster_path if poster_path else ""
            description = show.get("overview")
            release_date = show.get("first_air_date", "")
            year = release_date.split("-")[0] if release_date else "N/A"
            show_genres = [genres_lookup.get(genre_id, "Unknown") for genre_id in show.get("genre_ids", [])]
            shows.append({
                "title": title,
                "poster": poster_url,
                "description": description,
                "genres": ", ".join(show_genres),
                "year": year
            })
    return render_template("index.html", movies=shows)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Add authentication logic here
        return f"Logged in as {username}"  # Temporary response
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Add authentication logic here
        return f"Logged in as {username}"  # Temporary response
    return render_template("register.html")

@app.route("/temp", methods=["GET", "POST"])
def temp():
    return render_template("temp.html")

if __name__ == "__main__":
    app.run(debug=True)
