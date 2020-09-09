import argparse
import os

import requests
from requests.exceptions import HTTPError


class GitReposCrawler:
    def __init__(self, search_url, verbose=False):
        if verbose:
            print(f'Requesting search url {search_url} ...')
        self.items = self.get_json(search_url)['items']
        self.verbose = verbose
        if verbose:
            print(f'Got {len(self.items)} items')

    @property
    def names(self):
        return [repo['name'] for repo in self.items]

    @property
    def sizes(self):
        return [repo['size'] for repo in self.items]

    @staticmethod
    def get_json(search_url):
        response = requests.get(search_url)
        if response.status_code != 200:
            raise HTTPError(f'Status code: {response.status_code}')
        return response.json()

    @staticmethod
    def download_repo(repo):
        os.system('git clone ' + repo['html_url'])

    def download_small_repos(self, max_size):
        for repo in self.items:
            if repo['size'] <= max_size:
                self.download_repo(repo)
            elif self.verbose:
                print(f'Skipping {repo["name"]} ({repo["size"]} bytes)')


def main():
    parser = argparse.ArgumentParser(description='Download git repos with size less than 2048b')
    parser.add_argument('search_queries', metavar='search_queries', type=str, nargs='+',
                        help='Git Api search queries to be downloaded')
    parser.add_argument('--max_size', type=int, default=2047,
                        help="Max size of repository in bytes to be downloaded, 2047 be default")
    parser.add_argument('-v', '--verbose', action='store_true', help="Print additional information")
    args = parser.parse_args()
    for url in args.search_queries:
        crawler = GitReposCrawler(search_url=url, verbose=args.verbose)
        crawler.download_small_repos(max_size=args.max_size)


if __name__ == '__main__':
    main()

