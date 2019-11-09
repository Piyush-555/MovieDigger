import json
from flask import Flask, request


import model
import server


app = Flask(__name__)


@app.route("/signup/", methods=['POST'])
def signup():
    """
    Accept json={username:username, password:encrypted}
    Store user in db2

    Return verification
    """

    data = request.get_json()
    uname, enc_pass = data['username'], data['password']

    user_id = server.register_user(uname, enc_pass)
    if user_id == "username_exists":
        return "username_exists"

    server.add_user_movies(user_id, movie_ids=None)
    return "signed_up"


@app.route("/verify/", methods=['POST'])
def verify_login():
    """
    Accept json={username:username, password:encrypted}
    Check from db2

    Return status (verified-1, not-verified-0)
    """

    data = request.get_json()
    uname, enc_pass = data['username'], data['password']

    matched = server.verify_user(uname, enc_pass)
    if matched is True:
        status = "verified"
    elif matched is False:
        status = "password_incorrect"
    else:
        status = "username_do_not_exists"

    data = {'username': uname, 'status': status}
    data = json.dumps(data)
    return data


@app.route("/register_movies/", methods=['POST'])
def register_movies():
    """
    Accept json={username:username, movies:json_array of imdb ids}
    Create user in db1 and add movies
    Return status (ok-1, error-0)
    """

    data = request.get_json()
    uname, tmdb_ids = data['username'], data['tmdb_ids']

    user_id = server.get_user_id(uname)
    if user_id=="username_do_not_exists":
        return "username_do_not_exists"

    server.add_user_movies(user_id, movies=tmdb_ids)
    return "ok"


@app.route("/get_user_movies/", methods=['POST'])
def get_user_movies():
    """
    Accept json={username:username}
    Return num movie ids json_array
    """

    data = request.get_json()
    uname = data['username']

    user_id = server.get_user_id(uname)
    if user_id=="username_do_not_exists":
        return "username_do_not_exists"

    movie_ids = server.get_user_movies(user_id)
    tmdb_ids = server.get_tmdb_ids(movie_ids)
    movie_names = server.get_movie_names(movie_ids)

    data = {'tmdb_ids': tmdb_ids, 'names': movie_names}
    data = json.dumps(data)
    return data


@app.route("/get_popular_movies/", methods=['POST'])
def get_popular_movies():
    """
    Accept json={num_movies:num, genre:null/genre}
    Return num movie ids json_array
    """

    data = request.get_json()
    num_movies, genre = data['num_movies'], data['genre']
    assert genre is None or genre in model.genres

    movie_ids = model.get_popular_movies(num_movies, genre)
    tmdb_ids = server.get_tmdb_ids(movie_ids)
    movie_names = server.get_movie_names(movie_ids)

    data = {'tmdb_ids': tmdb_ids, 'names': movie_names}
    data = json.dumps(data)
    return data


@app.route("/movies_similar_to/", methods=['POST'])
def movies_similar_to():
    """
    Accept json={movie_array:imdb ids json_array, num_result:num}
    Return num movie ids json_array
    """

    data = request.get_json()
    tmdb_ids, num_rec = data['tmdb_ids'], data['num_result']

    movie_ids = server.get_movie_ids(tmdb_ids)
    movie_ids = model.get_recommendations(movie_ids, num_rec)
    tmdb_ids = server.get_tmdb_ids(movie_ids)
    movie_names = server.get_movie_names(movie_ids)

    data = {'tmdb_ids': tmdb_ids, 'names': movie_names}
    data = json.dumps(data)
    return data


@app.route("/recommend_movies_to_user/", methods=['POST'])
def recommend_movies_to_user():
    """
    Accept json={username:username, num_result:num}
    Return num movie ids json_array
    """

    data = request.get_json()
    uname, num_rec = data['username'], data['num_result']

    user_id = server.get_user_id(uname)
    if user_id=="username_do_not_exists":
        return "username_do_not_exists"

    movie_ids = server.get_user_movies(user_id)
    movie_ids = model.get_recommendations(movie_ids, num_rec)
    tmdb_ids = server.get_tmdb_ids(movie_ids)
    movie_names = server.get_movie_names(movie_ids)

    data = {'tmdb_ids': tmdb_ids, 'names': movie_names}
    data = json.dumps(data)
    return data


@app.route("/")
def root():
    return "I'm gROOT"


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
