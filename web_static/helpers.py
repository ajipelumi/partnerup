#!/usr/bin/python3
import os
import requests
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode


access_token = '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'

def get_commit_count(commits_url):
    """ Get the number of commits from a GitHub repository. """
    headers = {
            'User-Agent': 'My Custom User-Agent',
            'Authorization': f'Token {access_token}'
            }
    commits_url = commits_url[:commits_url.index("{/sha}")]
    parsed_url = urlparse(commits_url)
    query_params = parse_qs(parsed_url.query)
    query_params['per_page'] = ['100']
    encoded_query_params = urlencode(query_params, doseq=True)
    updated_url = urlunparse(parsed_url._replace(query=encoded_query_params))
    response = requests.get(updated_url, headers=headers)
    if response:
        commits = response.json()
        return len(commits)
    else:
        return 0
