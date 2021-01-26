from yaspin import yaspin
from collections import namedtuple
from pytablewriter import MarkdownTableWriter

import subprocess
import requests
import argparse
import math


repo_info = namedtuple('repoinfo', ['name', 'url'])
gist_info = namedtuple('gistinfo', ['id', 'files', 'description', 'url'])
user_info = namedtuple('userinfo', ['username', 'public_repos', 'public_gists', 'type'])

USER_API_URL = 'https://api.github.com/users/'
ORGS_API_URL = 'https://api.github.com/orgs/'


def get_user_info(username):
    ''' return user details '''
    response = requests.get(
        ''.join([
            USER_API_URL,
            '{}'.format(username)
        ])
    )
    return user_info(
        username     = username,
        public_repos = response.json().get('public_repos'),
        public_gists = response.json().get('public_gists'),
        type         = response.json().get('type')
    ) if response.status_code == 200 else None


def write_readme_for_gist(gists):
    ''' write the gist files and description in md format '''
    writer = MarkdownTableWriter()
    writer.table_name = 'gists'
    writer.headers = ['id', 'files', 'description']
    writer.value_matrix = list()
    for gist in gists:
        writer.value_matrix.append([
            gist.id,
            ', '.join(gist.files),
            gist.description
        ])
    writer.dump('GIST-README.md')


def get_repo_info(user_info):
    ''' returns the name of the repo and url '''
    number_of_pages = math.ceil(user_info.public_repos / 100)
    repositories = list()

    url_prefix = USER_API_URL + \
        user_info.username if user_info.type == 'User' else ORGS_API_URL + user_info.username

    for counter in range(number_of_pages):
        url = ''.join(
            [url_prefix, '/repos?per_page=100&page={}'.format(counter + 1)])
        response = requests.get(url)
        repositories += [
            repo_info(
                name = repo.get('name'),
                url  = repo.get('git_url')
            ) for repo in response.json()
        ]
    return repositories 


def get_gist_info(user_info):
    ''' returns the name and url of user gists '''
    number_of_pages = math.ceil(user_info.public_gists / 100)
    gists = list()

    url_prefix = USER_API_URL + user_info.username

    for counter in range(number_of_pages):
        url = ''.join(
            [url_prefix, '/gists?per_page=100&page={}'.format(counter + 1)])
        response = requests.get(url)
        gists += [
            gist_info(
                id          = gist.get('id'),
                files       = list(gist.get('files').keys()),
                description = gist.get('description'),
                url         = gist.get('git_pull_url'),
            ) for gist in response.json()
        ]
    return gists 


def get_gitclone_info(username):
    ''' returns all the clone links in list '''
    user_info = get_user_info(username)
    if type_of_acc:
        if number_of_repos > 0:
            repos = get_repo_info(user_info)
        else:
            print('no repositories found in user\'s github account')
        if number_of_gists > 0:
            gists = get_gist_info(user_info)
        else:
            print('no gists found in user\'s github account')
        return { 'repos': repos, 'gists': gists }
    else:
        print('user not found')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u',
        '--user',
        help='provide unique github user as arguement',
    )
    parser.add_argument(
        '-i',
        '--ignore-gist',
        help='ignore the gist the user has, download only the repos',
    )

    args = parser.parse_args()
    user = args.user

    info = get_gitclone_info(username=user)
    if info:
        total_repos = len(info.get('repos'))
        print('cloning repositories now')
        for count, repo in enumerate(info.get('repos'), start=1):
            # print("({}/{})  {} - {}".format( count, total_repos, repo.name, repo.url ))
            with yaspin(text="({}/{}) cloning {}".format(count, total_repos, repo.name), color='blue') as spinner:
                subprocess.run(
                    args=['git', 'clone', repo.url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

        total_gists = len(info.get('gists'))
        print('cloning gists now')
        if not args.ignore_gist:
            write_readme_for_gist(info.get('gists'))
            for count, gist in enumerate(info.get('gists'), start=1):
                with yaspin(text="({}/{}) cloning {}".format(count, total_gists, gist.id), color='blue') as spinner:
                    subprocess.run(
                        args=['git', 'clone', gist.url],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )


if __name__ == "__main__":
    main()
