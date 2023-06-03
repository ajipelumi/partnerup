#!/usr/bin/python3
import base64
from github import Github
import io
import matplotlib.pyplot as plt


access_token = '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'
github = Github(access_token)


def get_user_from_github(username):
    """ Get a particular user's data from GitHub. """
    try:
        user = github.get_user(username)
        return user.raw_data
    except Exception as e:
        print(f"Error: Failed to retrieve user data from GitHub. {e}")
        return None


def get_repos_from_github(username):
    """ Get all repositories for a particular user. """
    try:
        user = github.get_user(username)
        repos = user.get_repos()
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
