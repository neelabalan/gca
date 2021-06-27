import subprocess
import requests
import sys
from typing import List, Dict 

import click
from rich import print
from rich.progress import Progress, BarColumn, TimeElapsedColumn

USER_API_URL = 'https://api.github.com/users/'
ORG_API_URL = 'https://api.github.com/orgs/'
DEVNULL = subprocess.DEVNULL

bar_column =  BarColumn(bar_width=None, complete_style='blue')
time_elapsed_column = TimeElapsedColumn()
progress_console = "[progress.percentage]{task.percentage:>3.0f}%"

def construct_url(user: str, usertype: str, api: str='repo') -> str:
    url_prefix = USER_API_URL + user if usertype == 'User' else ORG_API_URL + user 
    if api=='repo': 
        return url_prefix + '/repos?per_page=100&page={page}'
    else:
        return url_prefix + '/gists?per_page=100&page={page}'


def fetch_response(url: str) -> List[Dict]:
    '''fetch all repo response by iterating the pages'''
    responses = list()
    page = 1 # starting with page 1
    while True:
        response = requests.get(url.format(page=page)).json()
        page += 1
        if not response:
            break # break from loop when no response
        responses += response
    return responses


def get_clone_urls(response: Dict, ssh: bool) -> Dict:
    clone_urls = list()
    repo_clone_url = 'ssh_url' if ssh else 'clone_url'
    if response.get('repo'):
        clone_urls = { repo.get('name'): repo.get(repo_clone_url) for repo in response.get('repo') }
    if response.get('gist'):
        clone_urls.update({ gist.get('id'): gist.get('git_pull_url') for gist in response.get('gist') })
    return clone_urls


def get_user_response(username: str) -> Dict:
    '''return user details'''
    try:
        response = requests.get(USER_API_URL + username)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print('Could not get proper response')
        print('[red]{}[/red]'.format(err))
        sys.exit()
    finally:
        return response.json()


def execute_cloning(url_list: dict):
    if not url_list:
        raise RuntimeError('No URL provided')
    with Progress(bar_column, progress_console, time_elapsed_column, expand=True) as progress:
        task = progress.add_task("[blue]Cloning...", total=len(url_list))
        for name, link in url_list.items():
            progress.update(task, advance=1)
            subprocess.run(args=['git', 'clone', link], stdout=DEVNULL, stderr=DEVNULL)
            progress.print('[green]✓[/green] ' + name)


def run(user: str, ssh: bool, gist: bool):
    response = get_user_response(user)
    usertype = response.get('type')
    gh_response = dict()
    gh_response['repo'] = fetch_response(url = construct_url(user, usertype, 'repo'))
    if gist:
        gh_response['gist'] = fetch_response(url = construct_url(user, usertype, 'gist'))
    clone_urls = get_clone_urls(gh_response, ssh)
    execute_cloning(clone_urls)


@click.command()
@click.option('--user', required=True, type=str)
@click.option('--ssh', type=bool)
@click.option('--gist', type=bool)
def main(user, ssh, gist):
    run(user, ssh, gist) 


if __name__ == "__main__":
    main()
