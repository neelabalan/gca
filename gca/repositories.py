import requests
import math
import subprocess
from collections import namedtuple

from gca.urls import USER_API_URL, ORG_API_URL
from yaspin import yaspin

def fetch_responses( response ):
    ''' returns the name of the repo and url '''
    user = response.get( 'repositories' )
    number_of_public_repos = user.get( 'public_repos' )
    acctype      = user.get( 'type' )
    username     = user.get( 'name' )
    responses    = list()

    if number_of_public_repos > 0:
        number_of_pages = math.ceil( number_of_public_repos / 100 )

        url_prefix = USER_API_URL + \
            username if acctype == 'User' else ORGS_API_URL + username

        for counter in range( number_of_pages ):
            url = ''.join(
                [ url_prefix, '/repos?per_page=100&page={}'.format( counter + 1 ) ]
            )
            responses +=  requests.get( url ).json()
    return responses 

def get_clone_urls( responses ):
    return  [
        ( repo.get('name'), repo.get('ssh_url') ) for repo in responses.get( 'repositories' )
    ]

def dump_summary( filename = 'repositories.md' ):
    pass

def execute_cloning( url_map ):
    repo_urls = url_map.get( 'repositories' )
    if repo_urls: 
        total_repos = len( repo_urls ) 
        print('cloning repositories...')
        for count, repo in enumerate( repo_urls, start=1 ):
            # print("({}/{})  {} - {}".format( count, total_repos, repo[0], repo[1]))
            with yaspin(text="({}/{}) cloning {}".format( count, total_repos, repo[ 0 ] ), color = 'blue' ) as spinner:
                subprocess.run(
                    args=[ 'git', 'clone', repo[ 1 ] ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )