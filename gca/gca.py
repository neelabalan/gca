import argparse
import subprocess
import requests
import math
import sys

from rich.table import Column
from rich.progress import Progress, BarColumn, TimeElapsedColumn

USER_API_URL = 'https://api.github.com/users/'
ORG_API_URL = 'https://api.github.com/orgs/'


def fetch_repo_responses( response ):
    ''' returns the name of the repo and url '''
    user = response.get( 'repositories' )
    number_of_public_repos = user.get( 'public_repos' )
    acctype      = user.get( 'type' )
    username     = user.get( 'name' )
    responses    = list()

    if number_of_public_repos > 0:
        number_of_pages = math.ceil( number_of_public_repos / 100 )

        url_prefix = USER_API_URL + \
            username if acctype == 'User' else ORG_API_URL + username

        for counter in range( number_of_pages ):
            url = ''.join(
                [ url_prefix, '/repos?per_page=100&page={}'.format( counter + 1 ) ]
            )
            responses +=  requests.get( url ).json()
    return responses 

def get_repo_clone_urls(username, url_type):
    return  [
        ( repo.get('name'), repo.get('clone_url') ) for repo in responses.get( 'gca.repositories' )
    ]


def fetch_gist_responses( response ):
    ''' returns the name and url of user gists '''
    user = response.get( 'gists' )
    public_gists    = user.get( 'public_gists' )
    username        = user.get( 'name' )
    responses       = list()

    if public_gists:
        number_of_pages = math.ceil( public_gists / 100 )
        url_prefix      = USER_API_URL + username

        for counter in range( number_of_pages ):
            url = ''.join(
                [ url_prefix, '/gists?per_page=100&page={}'.format( counter + 1 ) ]
            )
            responses += requests.get( url ).json()
    return responses

def get_gist_clone_urls( responses ):
    return [ 
        ( gist.get( 'id' ), gist.get( 'git_pull_url' ) ) for gist in responses.get( 'gca.gists' )
    ]

def get_user_response( username ):
    ''' return user details '''
    try:
        response = requests.get(
            ''.join([USER_API_URL, username])
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print('Could not get proper response')
        sys.exit( err )
    
    user_response = response.json()
    return {
        'public_repos': user_response.get( 'public_repos' ),
        'user_type'   : user_response.get( 'type' ),
        'name'        : user_response.get( 'login' ),
        'public_gists': user_response.get( 'public_gists' ),
        'name'        : user_response.get( 'name' )
    }


def execute_cloning( url_map ):
    repo_urls = url_map.get( 'gca.repositories' )
    if repo_urls: 
        total_repos = len( repo_urls ) 
        with Progress(
            BarColumn(bar_width=None, complete_style='blue'), 
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeElapsedColumn(), 
            expand=True
        ) as progress:
            task = progress.add_task("[blue]Cloning...", total=total_repos)
            for count, repo in enumerate( repo_urls, start=1 ):
                progress.update(task, advance=1)
                subprocess.run(
                    args=['git', 'clone', repo[1]],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                progress.print('[green]✓[/green] '+repo[0])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u',
        '--user',
        help = 'provide unique github user as arguement',
    )
    parser.add_argument(
        '-i',
        '--ignore-gist',
        action='store_true',
        help = 'ignore the gist, download only the repos',
    )

    args = parser.parse_args()
    user = args.user
    modlist    = [ 'gca.repositories', 'gca.gists' ] if not args.ignore_gist else [ 'gca.repositories' ]
    response   = get_user_response( username = user )
    result     = execute_funcs( modlist, 'fetch_responses', response = response )
    clone_urls = execute_funcs( modlist, 'get_clone_urls', responses = result )
    clone      = execute_funcs( modlist, 'execute_cloning', url_map = clone_urls )


if __name__ == "__main__":
    main()
