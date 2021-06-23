import subprocess
import requests
import math
import sys
import click

from rich.table import Column
from rich.progress import Progress, BarColumn, TimeElapsedColumn

USER_API_URL = 'https://api.github.com/users/'
ORG_API_URL = 'https://api.github.com/orgs/'


def fetch_repo_response(response):
    '''returns the name of the repo and url'''
    user = response.get('repositories')
    number_of_public_repos = user.get('public_repos')
    acctype = user.get('type')
    username = user.get('name')
    responses = list()

    if number_of_public_repos > 0:
        number_of_pages = math.ceil(number_of_public_repos / 100)
        url_prefix = (
            USER_API_URL + username if acctype == 'User' else ORG_API_URL + username
        )
        for counter in range(number_of_pages):
            url = ''.join(
                [url_prefix, '/repos?per_page=100&page={}'.format(counter + 1)]
            )
            responses += requests.get(url).json()
    return responses


def get_clone_urls(repo=True, gist=False, url_type='http'):
    clone_urls = list()
    if repo:
        clone_urls = [
            (repo.get('name'), repo.get('clone_url'))
            for repo in responses.get('gca.repositories')
        ]
    if gist:
        clone_urls += [
            (gist.get('id'), gist.get('git_pull_url'))
            for gist in responses.get('gca.gists')
        ]


def fetch_gist_response(user):
    '''returns the name and url of user gists'''
    user = response.get('gists')
    public_gists = user.get('public_gists')
    username = user.get('name')
    responses = list()
    if public_gists:
        number_of_pages = math.ceil(public_gists / 100)
        url_prefix = USER_API_URL + username
        for counter in range(number_of_pages):
            url = ''.join(
                [url_prefix, '/gists?per_page=100&page={}'.format(counter + 1)]
            )
            responses += requests.get(url).json()
    return responses


def get_user_response(username):
    '''return user details'''
    try:
        response = requests.get(''.join([USER_API_URL, username]))
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print('Could not get proper response')
        sys.exit(err)

    user_response = response.json()
    return {
        'total_repo': user_response.get('public_repos'),
        'total_gist': user_response.get('public_gists'),
        'user_type': user_response.get('type'),
    }


def execute_cloning(url_list: dict):
    if not url_list:
        raise RuntimeError('No URL provided for cloning')

    with Progress(
        BarColumn(bar_width=None, complete_style='blue'),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(),
        expand=True,
    ) as progress:
        task = progress.add_task("[blue]Cloning...", total=len(url_list))
        for count, repo in enumerate(url_list, start=1):
            progress.update(task, advance=1)
            subprocess.run(
                args=['git', 'clone', repo[1]],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            progress.print('[green]✓[/green] ' + repo[0])


def run():
    pass


if __name__ == "__main__":
    run()
