import subprocess
import requests
import argparse
import math
from yaspin import yaspin
from collections import namedtuple

url_and_name = namedtuple( 'repoinfo', ['name', 'url'] )
USER_API_URL = 'https://api.github.com/users/'
ORGS_API_URL = 'https://api.github.com/orgs/'

def _fetch_user_info( username ):
    ''' return user details '''
    response = requests.get( 
        ''.join([ 
            USER_API_URL, 
            '{}'.format( username ) 
        ])
    )
    return response.json() if response.status_code == 200 else None

def _get_gitclone_links_with_reponame( username, type_of_acc, page = 1 ):
    ''' returns all the clone links in list '''
    url_prefix = USER_API_URL if type_of_acc == 'User' else ORGS_API_URL
    url = ''.join( [ url_prefix, '{}/repos?per_page=100&page={}'.format( username, page )])
    response = requests.get( url )
    return [ 
        url_and_name( name = repo.get( 'name' ), url = repo.get( 'git_url' ) ) for repo in response.json() 
    ] 

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

    user_info = _fetch_user_info( user )
    if user_info:
        number_of_repos = user_info.get( 'public_repos' )
        type_of_acc = user_info.get( 'type' )
        number_of_pages = math.ceil( number_of_repos / 100 )
        # setting counter value
        count = 1 
        for counter in range( number_of_pages ):
            name_and_links = _get_gitclone_links_with_reponame( user, type_of_acc, counter + 1 )
            if number_of_repos > 0:
                for repo in name_and_links:
                    # print("({}/{})  {} - {}".format( count, number_of_repos, repo.name, repo.url ))
                    with yaspin( text = "({}/{}) cloning {}".format( count, number_of_repos, repo.name ), color = 'blue' ) as spinner:
                        subprocess.run([ 'git', 'clone', repo.url ], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL )
                    incrementing
                    count +=  1 
            else:
                print( 'the user has no repository' )
    else:
        print( 'could not find the user' )


if __name__ == "__main__":
    main()