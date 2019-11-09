import json
from flask import Flask, request


app = Flask(__name__)


@app.route("/signup/", methods=['GET', 'POST'])
def signup():
    """
    Accept json={username:username, password:encrypted}
    Store user in db2

    Return verification
    """
    return 

@app.route("/verify/")
def verify_login():
    """
    Accept json={username:username, password:encrypted}
    Check from db2

    Return status (verified-1, not-verified-0)
    """
    return

def popular_movies():
    """
    Accept json={num_movies:num, genre:null/genre}
    Return num movie ids json_array
    """
    return

def register_movies():
    """
    Accept json={username:username, movies:json_array of imdb ids}
    Create user in db1 and add movies
    Return status (ok-1, error-0)
    """
    return

def recommend_movies():
    """
    Accept json={movie_array:imdb ids json_array, num_result:num}
    Return num movie ids json_array
    """
    return

@app.route("/")
def root():
    return "ROOT"


if __name__ == "__main__":
    app.run(host='192.168.100.102', port=5000)