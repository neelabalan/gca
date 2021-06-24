import subprocess
import requests
import math
import sys
import click

from rich.table import Column
from rich.progress import Progress, BarColumn, TimeElapsedColumn

USER_API_URL = 'https://api.github.com/users/'
ORG_API_URL = 'https://api.github.com/orgs/'
bar_column =  BarColumn(bar_width=None, complete_style='blue')
progress_console = "[progress.percentage]{task.percentage:>3.0f}%"

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


def get_clone_urls(response, url_type='http') -> dict:
    clone_urls = list()
    if response.get('type') == 'repo':
        clone_urls = {
            response.get('name'): response.get('clone_url')  for repo in response.get('gca.repositories')
        }
    if 'gist' in response.get('type'):
        clone_urls.update({
            gist.get('id'): gist.get('git_pull_url') for gist in response.get('gca.gists')
        }) 
    return clone_urls


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
    finally:
        return response.json()


def execute_cloning(url_list: dict):
    if not url_list:
        raise RuntimeError('No URL provided for cloning')
    with Progress(TimeElapsedColumn(), columns=bar_column, console=progress_console, expand=True) as progress:
        task = progress.add_task("[blue]Cloning...", total=len(url_list))
        for count, repo in enumerate(url_list, start=1):
            progress.update(task, advance=1)
            subprocess.run(
                args=['git', 'clone', repo[1]],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            progress.print('[green]✓[/green] ' + repo[0])


def run(user, ssh, gist):
    response = get_user_response(user)
    total_repo, total_gist, usertype = (
        response.get('public_repos'),
        response.get('public_gists'),
        response.get('type')
    )
    gh_response = dict()
    gh_response['repo'] = fetch_repo_response(user)
    if gist:
        gh_response['gist'] = fetch_gist_response(user)
    clone_urls = get_clone_urls(gh_response)
    execute_cloning(clone_urls)



@click.command
@click.option('--user', required=True, type=str)
@click.option('--ssh', type=str)
@click.option('--gist', type=bool)
def main(user, ssh, gist):
    run(user, ssh, gist) 


if __name__ == "__main__":
    main()
