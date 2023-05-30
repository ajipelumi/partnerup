#!/usr/bin/python3
import requests


def get_commit_count(commits_url):
    """ Get the number of commits from a GitHub repository. """
    response = requests.get(commits_url)
    if response:
        commits = response.json()
        return len(commits)
    else:
        return 0
