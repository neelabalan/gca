import subprocess
import requests
import sys
import click

from rich.table import Column
from rich.progress import Progress, BarColumn, TimeElapsedColumn

USER_API_URL = 'https://api.github.com/users/'
ORG_API_URL = 'https://api.github.com/orgs/'
bar_column =  BarColumn(bar_width=None, complete_style='blue')
progress_console = "[progress.percentage]{task.percentage:>3.0f}%"

def construct_url(user, org_type, api='repo'):
    url_prefix = USER_API_URL + user if org_type == 'User' else ORG_API_URL + user 
    if api=='repo': 
        return url_prefix + '/repos?per_page=100&page={page}'
    else:
        return url_prefix + '/gists?per_page=100&page={page}'

def fetch_response(url):
    '''fetch all repo response by iterating the pages'''
    responses = list()
    page = 0
    while True:
        response = requests.get(url.format(page=page))
        page += 1
        if response:
            responses += response
        else:
            break
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
    gh_response['repo'] = fetch_response(url = construct_url(user, usertype, 'repo'))
    if gist:
        gh_response['gist'] = fetch_response(url = construct_url(user, usertype, 'gist'))
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
