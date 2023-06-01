#!/usr/bin/python3
import io
import os
import matplotlib.pyplot as plt
from flask import url_for
import requests


access_token = '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'
headers = {
            'User-Agent': 'My Custom User-Agent',
            'Authorization': f'Token {access_token}'
        }


def get_all_commits(username, repo):
    """ Get all commits in a repository. """
    commits = []
    page = 1
    per_page = 100
    url = f'https://api.github.com/repos/{username}/{repo}/commits'

    while True:
        params = {'page': page, 'per_page': per_page}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        commits += response.json()

        if not response.links:
            break

        if not response.links.get('next'):
            break

        url = response.links['next']['url']
        page += 1

    return commits


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
