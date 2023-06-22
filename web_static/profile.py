#!/usr/bin/python3
""" Starts a Flask Web Application """
from flask import Flask, render_template, session, request
from models import storage
from models.partner import Partner
from models.user import User
import random
import uuid
from web_static.helper import *


# Create Flask app
app = Flask(__name__)

# Set secret key for session
app.secret_key = 'secret_key'


@app.teardown_appcontext
def close_db(exception):
    """ Remove the current SQLAlchemy Session. """
    # Close current SQLAlchemy Session
    storage.close()


@app.route('/profile', strict_slashes=False)
def profile_page():
    """ Create a particular user's page. """
    # Get user data from session
    user = session.get('user')

    # Get username and cohort number from user data
    username = user.get('username')
    cohort_number = user.get('cohort_number')

    # Get user data from GitHub
    user_response = get_user_from_github(username)
    if user_response is None or 'repos_url' not in user_response:
        error_message = "Error: Failed to retrieve data from GitHub."
        return render_template('error.html', error_message=error_message)

    # Get user repositories from GitHub
    repo_response = get_repos_from_github(username)
    if repo_response is None:
        error_message = "Error: Failed to retrieve data from GitHub."
        return render_template('error.html', error_message=error_message)

    # Render profile page
    return render_template('profile.html',
                           cohort_number=cohort_number,
                           user_response=user_response,
                           repo_response=repo_response,
                           cache_id=uuid.uuid4())


@app.route('/match', strict_slashes=False)
def match_page():
    """ Match users based on their GitHub repositories. """
    # Get data from request
    project, repo, time = get_request_data()

    # Set matching partners to empty list
    matching_partners = []

    # Get user data from session
    user, username, cohort_number = get_user_info()

    # Get user commits from GitHub
    user_commit_data = get_all_commits(username, repo)
    if user_commit_data is None:
        error_message = "Error: Failed to retrieve data from GitHub."
        return render_template('error.html', error_message=error_message)
    # Get user commit count
    user_commit_count = get_total_commit_count(username, repo)

    all_partners = storage.all(Partner).values()  # list of partner objects

    # Iterate through all matching partners
    while len(matching_partners) == 0:
        # Get three random partners
        random_partners = random.sample(list(all_partners), 3)

        for partner in random_partners:  # Iterate through all random partners
            partner = partner.to_dict()

            if username == partner.get('username'):  # Skip if partner is user
                continue

            # Skip if partner is not in the same cohort
            if cohort_number != partner.get('cohort_number'):
                continue

            partner_commit_data = get_all_commits(partner.get('username'), repo)
            if partner_commit_data is None:
                err = "Error: Failed to retrieve data from GitHub."
                return render_template('error.html', error_message=err)
            # Get partner commit count
            partner_commit_count = get_total_commit_count(partner.get('username'), repo)

            # Check if partner commits during the day or night
            commit_period(time, matching_partners, partner, partner_commit_data, partner_commit_count)

    # Select best partner
    selected_partner = select_best_partner(matching_partners, user_commit_count)

    partner_commit_data = get_all_commits(selected_partner.get('username'), repo)
    if partner_commit_data is None:
        error_message = "Error: Failed to retrieve data from GitHub."
        return render_template('error.html', error_message=error_message)

    partner_response = get_user_from_github(selected_partner.get('username'))
    if partner_response is None:
        error_message = "Error: Failed to retrieve data from GitHub."
        return render_template('error.html', error_message=error_message)

    # Get plot image URL
    plot_image_url = plot_image(user, user_commit_data, partner_commit_data, selected_partner)
    email = selected_partner.get('email')

    # Save user and partner to database
    save_user_partner(user, selected_partner)

    # Render match page
    return render_template('match.html',
                           project=project,
                           partner_response=partner_response,
                           plot_image_url=plot_image_url,
                           email=email,
                           cache_id=uuid.uuid4()
                           )


def get_request_data():
    """ Get data from request. """
    project = request.args.get('project')
    repo = request.args.get('repo')
    time = request.args.get('time')
    return project, repo, time


def get_user_info():
    """ Get user data from session. """
    user = session.get('user')
    username = user.get('username')
    cohort_number = int(user.get('cohort_number'))
    return user, username, cohort_number


def commit_period(time, matching_partners, partner, partner_commit_data, partner_commit_count):
    """ Check if partner commits during the day or night. """
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


def select_best_partner(matching_partners, user_commit_count):
    """ Select the best partner from a list of matching partners. """
    # Sort matching partners by commit count
    sorted_partners = sorted(matching_partners, key=lambda partner: abs(partner['commit_count'] - user_commit_count))

    # Select partner with the least difference in commit count
    selected_partner = sorted_partners[0]

    # Return selected partner
    return selected_partner


def save_user_partner(user, selected_partner):
    """ Save user and partner to database. """
    current_user = storage.get(User, user.get('id'))
    selected_partner = storage.get(Partner, selected_partner.get('id'))
    current_user.partners.append(selected_partner)
    storage.save()


@app.route('/previous-matches', strict_slashes=False)
def previous_matches_page():
    """ Display a user's previous matches. """
    # Get user data from session
    user = session.get('user')

    # Set up list of partners
    partners = []

    # Get current user and all partners
    current_user = storage.get(User, user.get('id'))
    all_partners = current_user.partners

    # Iterate through all partners and add to list
    for partner in all_partners:
        partner = storage.get(Partner, partner.id)
        partners.append(partner.to_dict())

    # Render previous matches page
    return render_template('previous-matches.html',
                           partners=partners,
                           cache_id=uuid.uuid4())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
