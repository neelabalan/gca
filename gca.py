import subprocess
import requests
import argparse
import math
from yaspin import yaspin
from collections import namedtuple

url_and_name = namedtuple( 'repoinfo', ['name', 'url'] )
USER_API_URL = 'https://api.github.com/users/'
ORGS_API_URL = 'https://api.github.com/orgs/'

def _get_numberofrepos_and_type( username ):
    ''' return user details '''
    response = requests.get( 
        ''.join([ 
            USER_API_URL, 
            '{}'.format( username ) 
        ])
    )
    return ( 
        response.json().get( 'public_repos' ), response.json().get( 'type' ) 
    ) if response.status_code == 200 else ( None, None )

def get_gitclone_links_with_reponame( username ):
    ''' returns all the clone links in list '''
    number_of_repos, type_of_acc = _get_numberofrepos_and_type( username )
    if type_of_acc:
        name_and_links  = list()
        if number_of_repos > 0:
            number_of_pages = math.ceil( number_of_repos / 100 )
            url_prefix      = USER_API_URL + username if type_of_acc == 'User' else ORGS_API_URL + username

            for counter in range( number_of_pages ):
                url      = ''.join( [ url_prefix, '/repos?per_page=100&page={}'.format( counter + 1 )])
                response = requests.get( url )
                name_and_links += [ 
                    url_and_name( name = repo.get( 'name' ), url = repo.get( 'git_url' ) ) for repo in response.json() 
                ] 
            return name_and_links
        else:
            print( 'no repository found for the given user' )
    else:
        print( 'user not found' )

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
        help = 'ignore the gist the user has, download only the repos',
    )
    args = parser.parse_args()
    user = args.user

    name_and_links = get_gitclone_links_with_reponame( username = user )
    if name_and_links: 
        total_repos = len( name_and_links )
        for count, repo in enumerate( name_and_links, start = 1 ):
            # print("({}/{})  {} - {}".format( count, total_repos, repo.name, repo.url ))
                with yaspin( text = "({}/{}) cloning {}".format( count, total_repos, repo.name ), color = 'blue' ) as spinner:
                    subprocess.run([ 'git', 'clone', repo.url ], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL )

if __name__ == "__main__":
    main()