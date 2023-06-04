#!/usr/bin/python3
""" Starts a Flask Web Application """
from flask import Flask, render_template, session, request
from models import storage
from models.partner import Partner
from models.user import User
import random
import uuid
from web_static.helper import *


app = Flask(__name__)
app.secret_key = 'secret_key'


@app.teardown_appcontext
def close_db(exception):
    """ Remove the current SQLAlchemy Session. """
    storage.close()


@app.route('/profile', strict_slashes=False)
def profile_page():
    """ Create a particular user's page. """
    user = session.get('user')
    username = user.get('username')

    user_response = get_user_from_github(username)
    if user_response is None or 'repos_url' not in user_response:
        error_message = "Error: Failed to retrieve data from GitHub."
        return render_template('error.html', error_message=error_message)

    repo_response = get_repos_from_github(username)
    if repo_response is None:
        error_message = "Error: Failed to retrieve data from GitHub."
        return render_template('error.html', error_message=error_message)

    return render_template('profile.html',
                           user_response=user_response,
                           repo_response=repo_response,
                           cache_id=uuid.uuid4())


@app.route('/match', strict_slashes=False)
def match_page():
    """ Match users based on their GitHub repositories. """
    project = request.args.get('project')
    repo = request.args.get('repo')
    time = request.args.get('time')

    matching_partners = []

    user = session.get('user')
    username = user.get('username')
    user_commit_data = get_all_commits(username, repo)
    if user_commit_data is None:
        error_message = "Error: Failed to retrieve data from GitHub."
        return render_template('error.html', error_message=error_message)
    user_commit_count = get_total_commit_count(username, repo)

    all_partners = storage.all(Partner).values()
    random_partners = random.sample(list(all_partners), 3)

    for partner in random_partners:
        partner = partner.to_dict()
        if username == partner.get('username'):
            continue

        partner_commit_data = get_all_commits(partner.get('username'), repo)
        if partner_commit_data is None:
            error_message = "Error: Failed to retrieve data from GitHub."
            return render_template('error.html', error_message=error_message)
        partner_commit_count = get_total_commit_count(partner.get('username'), repo)

        if time == 'night' and commits_during_night(partner_commit_data):
            matching_partners.append({
                'username': partner.get('username'),
                'id': partner.get('id'),
                'email': partner.get('email'),
                'commit_count': partner_commit_count,
            })
        else:
            matching_partners.append({
                'username': partner.get('username'),
                'id': partner.get('id'),
                'email': partner.get('email'),
                'commit_count': partner_commit_count,
            })

    if matching_partners:
        sorted_partners = sorted(matching_partners, key=lambda partner: abs(partner['commit_count'] - user_commit_count))
        selected_partner = sorted_partners[0]

        partner_commit_data = get_all_commits(selected_partner.get('username'), repo)
        if partner_commit_data is None:
            error_message = "Error: Failed to retrieve data from GitHub."
            return render_template('error.html', error_message=error_message)

        partner_response = get_user_from_github(selected_partner.get('username'))
        if partner_response is None:
            error_message = "Error: Failed to retrieve data from GitHub."
            return render_template('error.html', error_message=error_message)

        plot_image_url = plot_image(user, user_commit_data, partner_commit_data, selected_partner)
        email = selected_partner.get('email')

        current_user = storage.get(User, user.get('id'))
        selected_partner = storage.get(Partner, selected_partner.get('id'))
        current_user.partners.append(selected_partner)
        storage.save()

        return render_template('match.html',
                               project=project,
                               partner_response=partner_response,
                               plot_image_url=plot_image_url,
                               email=email,
                               cache_id=uuid.uuid4()
                               )
    else:
        return render_template('match.html',
                               project=project,
                               partner_response=None,
                               plot_image_url=None,
                               email=None,
                               cache_id=uuid.uuid4()
                               )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
