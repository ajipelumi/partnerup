#!/usr/bin/python3
""" Starts a Flash Web Application """
from flask import Flask, render_template, session, request
from web_static.helpers import *
from models import storage
from models.partner import Partner
from models.user import User
import random
import requests
import uuid


app = Flask(__name__)
app.secret_key = 'secret_key'
access_token = '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'
headers = {
            'User-Agent': 'My Custom User-Agent',
            'Authorization': f'Token {access_token}'
        }


@app.teardown_appcontext
def close_db(exception):
    """ Remove the current SQLAlchemy Session. """
    storage.close()


@app.route('/profile', strict_slashes=False)
def profile_page():
    """ Create a particular user's page. """
    user = session.get('user')
    url = f'https://api.github.com/users/{user.get("username")}'
    user_response = requests.get(url, headers=headers).json()
    if user_response is None or 'repos_url' not in user_response:
        error_message = "Error: Failed to retrieve data from the GitHub."
        return render_template('error.html', error_message=error_message)

    repo_response = requests.get(user_response.get('repos_url'),
                                 headers=headers).json()
    if repo_response is None:
        error_message = "Error: Failed to retrieve data from the GitHub."
        return render_template('error.html', error_message=error_message)

    return render_template('profile.html',
                           user_response=user_response,
                           repo_response=repo_response,
                           cache_id=uuid.uuid4(),
                           get_all_commits=get_all_commits)


@app.route('/match', methods=['GET'])
def match_page():
    """ Match users based on their GitHub repositories. """
    project = request.args.get('project')
    repo = request.args.get('repo')
    time = request.args.get('time')

    matching_partners = []

    user = session.get('user')
    user_commit_data = get_all_commits(user.get('username'), repo)
    if user_commit_data is None:
        error_message = "Error: Failed to retrieve data from the GitHub."
        return render_template('error.html', error_message=error_message)
    user_commit_count = len(user_commit_data)

    all_partners = storage.all(Partner).values()
    random_partners = random.sample(list(all_partners), 2)

    for partner in random_partners:
        partner = partner.to_dict()
        if user.get('username') == partner.get('username'):
            continue

        partner_commit_data = get_all_commits(partner.get('username'), repo)
        if partner_commit_data is None:
            error_message = "Error: Failed to retrieve data from the GitHub."
            return render_template('error.html', error_message=error_message)
        partner_commit_count = len(partner_commit_data)

        if time == 'night':
            if commits_during_night(partner_commit_data):
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

    selected_partner = {}
    if matching_partners:
        sorted_partners = sorted(matching_partners, key=lambda partner:
                                 abs(partner['commit_count'] -
                                     user_commit_count))
        selected_partner = sorted_partners[0]

    partner_commit_data = get_all_commits(selected_partner.get('username'),
                                          repo)
    if partner_commit_data is None:
        error_message = "Error: Failed to retrieve data from the GitHub."
        return render_template('error.html', error_message=error_message)

    url = f'https://api.github.com/users/{selected_partner.get("username")}'
    partner_response = requests.get(url, headers=headers).json()
    if partner_response is None:
        error_message = "Error: Failed to retrieve data from the GitHub."
        return render_template('error.html', error_message=error_message)

    plot_image_url = plot_image(user, user_commit_data, partner_commit_data,
                                selected_partner)

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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
