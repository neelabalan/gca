import requests
import math
import subprocess
from collections import namedtuple


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
            username if acctype == 'User' else ORG_API_URL + username

        for counter in range( number_of_pages ):
            url = ''.join(
                [ url_prefix, '/repos?per_page=100&page={}'.format( counter + 1 ) ]
            )
            responses +=  requests.get( url ).json()
    return responses 

def get_clone_urls(username, url_type):
    return  [
        ( repo.get('name'), repo.get('clone_url') ) for repo in responses.get( 'gca.repositories' )
    ]