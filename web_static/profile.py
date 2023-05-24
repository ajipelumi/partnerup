#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import Flask, render_template, session
from models import storage
import requests

app = Flask(__name__)


@app.teardown_appcontext
def close_db(exception):
    """ Remove the current SQLAlchemy Session. """
    storage.close()


@app.route('/profile', strict_slashes=False)
def profile_page():
    """ Create a particular user's page. """
    user = session.get('user')
    url = f'https://api.github.com/users/{user.username}'
    user_response = requests.get(url).json()
    if user_response.status_code != 200:
        error_message = "Error: Failed to retrieve data from the GitHub."
        return render_template('error.html', error_message=error_message)
    
    repo_response = requests.get(user_response.get('repos_url')).json()
    if repo_response.status_code != 200:
        error_message = "Error: Failed to retrieve data from the GitHub."
        return render_template('error.html', error_message=error_message)
    
    return render_template('profile.html',
                           user_response=user_response,
                           repo_response=repo_response)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)