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

    server.add_user_movies(user_id, movies=None)
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
        return "verified"
    elif matched is False:
        return "password_incorrect"
    return "username_do_not_exists"


@app.route("/popular_movies/", methods=['POST'])
def popular_movies():
    """
    Accept json={num_movies:num, genre:null/genre}
    Return num movie ids json_array
    """

    data = request.get_json()
    num_movies, genre = data['num_movies'], data['genre']
    assert genre is None or genre in model.genres

    imdb_ids, movie_names = model.get_popular_movies(num_movies, genre)
    data = {'imdb_ids': imdb_ids, 'names': movie_names}
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
    uname, imdb_ids = data['username'], data['imdb_ids']

    user_id = server.get_user_id(uname)
    if user_id=="username_do_not_exists":
        return "username_do_not_exists"

    server.add_user_movies(user_id, movies=imdb_ids)
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

    imdb_ids = server.get_user_movies(user_id)
    data = {'imdb_ids': imdb_ids}
    data = json.dumps(data)
    return data


@app.route("/movies_similar_to/", methods=['POST'])
def movies_similar_to():
    """
    Accept json={movie_array:imdb ids json_array, num_result:num}
    Return num movie ids json_array
    """

    data = request.get_json()
    imdb_ids, num_recc = data['imdb_ids'], data['num_result']

    movies_recc = model.get_reccomendations(imdb_ids, num_recc)
    data = {'imdb_ids': movies_recc}
    data = json.dumps(data)
    return data


@app.route("/recommend_movies_to_user/", methods=['POST'])
def recommend_movies_to_user():
    """
    Accept json={username:username, num_result:num}
    Return num movie ids json_array
    """

    data = request.get_json()
    uname, num_recc = data['username'], data['num_result']

    user_id = server.get_user_id(uname)
    if user_id=="username_do_not_exists":
        return "username_do_not_exists"

    imdb_ids = server.get_user_movies(user_id)
    movies_recc = model.get_reccomendations(imdb_ids, num_recc)
    data = {'imdb_ids': movies_recc}
    data = json.dumps(data)
    return data


@app.route("/")
def root():
    return "ROOT"


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
