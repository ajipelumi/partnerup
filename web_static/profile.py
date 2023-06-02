#!/usr/bin/python3
""" Starts a Flask Web Application """
import base64
from flask import Flask, render_template, session, request
import io
from models import storage
from models.partner import Partner
from models.user import User
import matplotlib.pyplot as plt
from github import Github
import random
import uuid

app = Flask(__name__)
app.secret_key = 'secret_key'
access_token = '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'
github = Github(access_token)


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

    repo_response = get_repos_from_github(user_response.get('repos_url'))
    if repo_response is None:
        error_message = "Error: Failed to retrieve data from GitHub."
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
    username = user.get('username')
    user_commit_data = get_all_commits(username, repo)
    if user_commit_data is None:
        error_message = "Error: Failed to retrieve data from GitHub."
        return render_template('error.html', error_message=error_message)
    user_commit_count = len(user_commit_data)

    all_partners = storage.all(Partner).values()
    random_partners = random.sample(list(all_partners), 2)

    for partner in random_partners:
        partner = partner.to_dict()
        if username == partner.get('username'):
            continue

        partner_commit_data = get_all_commits(partner.get('username'), repo)
        if partner_commit_data is None:
            error_message = "Error: Failed to retrieve data from GitHub."
            return render_template('error.html', error_message=error_message)
        partner_commit_count = len(partner_commit_data)

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


def get_user_from_github(username):
    """ Get a particular user's data from GitHub. """
    try:
        user = github.get_user(username)
        return user.raw_data
    except Exception as e:
        print(f"Error: Failed to retrieve user data from GitHub. {e}")
        return None


def get_repos_from_github(repos_url):
    """ Get all repositories for a particular user. """
    try:
        repos = github.get_repos(url=repos_url)
        repo_data = []
        for repo in repos:
            repo_data.append(repo.raw_data)
        return repo_data
    except Exception as e:
        print(f"Error: Failed to retrieve repository data from GitHub. {e}")
        return None


def get_all_commits(username, repo):
    """ Get all commits for a particular user and repository. """
    try:
        repository = github.get_repo(f"{username}/{repo}")
        commits = repository.get_commits()
        commit_data = []
        for commit in commits:
            commit_data.append(commit.raw_data)
        return commit_data
    except Exception as e:
        print(f"Error: Failed to retrieve commit data from GitHub. {e}")
        return None


def commits_during_night(commits):
    """ Check if commits are made at night. """
    for commit in commits:
        commit_time = commit.get('commit').get('author').get('date')
        commit_hour = int(commit_time[11:13])
        if commit_hour < 6 or commit_hour > 18:
            return True
    return False


def process_commit_by_date(commits):
    """ Process commit counts by date. """
    commit_counts = {}
    for commit in commits[:10]:
        date = commit['commit']['author']['date'][:10]
        if date not in commit_counts:
            commit_counts[date] = 0
        commit_counts[date] += 1
    return commit_counts


def plot_image(user, user_commit_data, partner_commit_data, selected_partner):
    """ Visualize commit history with matplotlib. """
    plt.figure(figsize=(20, 10))
    user_commit_counts = process_commit_by_date(user_commit_data)
    user_commit_dates = list(user_commit_counts.keys())
    user_commit_values = list(user_commit_counts.values())
    plt.plot(user_commit_dates, user_commit_values,
             label=f'{user.get("username")}')

    partner_commit_counts = process_commit_by_date(partner_commit_data)
    partner_commit_dates = list(partner_commit_counts.keys())
    partner_commit_values = list(partner_commit_counts.values())
    plt.plot(partner_commit_dates, partner_commit_values,
             label=f'{selected_partner.get("username")}')
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Number of Commits')
    plt.title('Commits per day')
    plt.grid(True)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_bytes = base64.b64encode(buffer.read()).decode('utf-8')
    return plot_bytes


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
