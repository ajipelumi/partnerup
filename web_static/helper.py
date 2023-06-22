#!/usr/bin/python3
import base64
from dotenv import dotenv_values
from github import Github
import io
import matplotlib.pyplot as plt


# Load environment variables from .env file
config = dotenv_values(".env")

# Load GitHub access token from .env file
access_token = config.get('ACCESS_TOKEN')

# Create GitHub instance
github = Github(access_token)


def get_user_from_github(username):
    """ Get a particular user's data from GitHub. """
    try:
        # Get user data from GitHub
        user = github.get_user(username)

        # Return user raw data
        return user.raw_data
    except Exception:
        # Return None if user does not exist
        return None


def get_repos_from_github(username):
    """ Get all repositories for a particular user. """
    try:
        # Get user data from GitHub
        user = github.get_user(username)

        # Get all repositories for user
        repos = user.get_repos()

        # Create a list of repository raw data
        repo_data = []

        # Iterate through all repositories
        for repo in repos:

            # Append repository raw data to list
            repo_data.append(repo.raw_data)

        # Return list of repository raw data
        return repo_data
    except Exception:
        # Return None if user does not exist
        return None


def get_all_commits(username, repo, max_commits=30):
    """ Get up to 'max_commits' commits for a particular user and repo. """
    try:
        # Get repository data from GitHub
        repository = github.get_repo(f"{username}/{repo}")

        # Get up to 'max_commits' commits for repository
        commits = repository.get_commits()[:max_commits]

        # Create a list of commit raw data
        commit_data = []

        # Iterate through all commits
        for commit in commits:

            # Append commit raw data to list
            commit_data.append(commit.raw_data)

        # Return list of commit raw data
        return commit_data
    except Exception:
        # Return None if user or repository does not exist
        return None


def get_total_commit_count(username, repo):
    """ Get the total number of commits for a particular user and repo. """
    try:
        # Get repository data from GitHub
        repository = github.get_repo(f"{username}/{repo}")

        # Get all commits for repository
        commits = repository.get_commits()

        # Create a counter for total commits
        total_commit_count = 0

        # Iterate through all commits
        for _ in commits:

            # Increment total commit count
            total_commit_count += 1

        # Return total commit count
        return total_commit_count
    except Exception:
        # Return None if user or repository does not exist
        return None


def commits_during_night(commits):
    """ Check if commits are made at night. """
    # Iterate through all commits
    for commit in commits:

        # Get commit time
        commit_time = commit.get('commit').get('author').get('date')

        # Get commit hour
        commit_hour = int(commit_time[11:13])

        # Check if commit is made at night
        if commit_hour < 6 or commit_hour > 18:

            # Return True if commit is made at night
            return True

    # Return False if no commits are made at night
    return False


def process_commit_by_date(commits):
    """ Process commit counts by date. """
    # Create a dictionary of commit counts by date
    commit_counts = {}

    # Iterate through all commits
    for commit in commits:

        # Get commit date
        date = commit['commit']['author']['date'][:10]

        # Check if date is in dictionary
        if date not in commit_counts:

            # Add date to dictionary if not in dictionary
            commit_counts[date] = 0

        # Increment commit count for date if date is in dictionary
        commit_counts[date] += 1

    # Return dictionary of commit counts by date
    return commit_counts


def plot_image(user, user_commit_data, partner_commit_data, selected_partner):
    """ Visualize commit history with matplotlib. """
    # Create a figure
    plt.figure(figsize=(20, 10))

    # Get user commit counts by date
    user_commit_counts = process_commit_by_date(user_commit_data)

    # Get user commit dates and values
    user_commit_dates = list(user_commit_counts.keys())
    user_commit_values = list(user_commit_counts.values())

    # Plot user commit values
    plt.plot(user_commit_dates, user_commit_values,
             label=f'{user.get("username")}')

    # Get partner commit counts by date
    partner_commit_counts = process_commit_by_date(partner_commit_data)

    # Get partner commit dates and values
    partner_commit_dates = list(partner_commit_counts.keys())
    partner_commit_values = list(partner_commit_counts.values())

    # Plot partner commit values
    plt.plot(partner_commit_dates, partner_commit_values,
             label=f'{selected_partner.get("username")}')

    # Set legend, x-axis label, y-axis label, title, and grid
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Number of Commits')
    plt.title('Commits per day')
    plt.grid(True)

    # Create a buffer
    buffer = io.BytesIO()

    # Save plot to buffer as png
    plt.savefig(buffer, format='png')

    # Seek to beginning of buffer
    buffer.seek(0)

    # Encode buffer as base64
    plot_bytes = base64.b64encode(buffer.read()).decode('utf-8')

    # Return base64 encoded plot
    return plot_bytes
