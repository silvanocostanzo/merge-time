import json
import os
import re
import sys

import requests


def write_prs_to_file(prs: list):
    file_exists = os.path.exists("prs.json")
    if file_exists:
        with open("prs.json", "a", ) as f:
            json.dump(prs, f, default=str)
    else:
        with open("prs.json", "w") as f:
            json.dump(prs, f, default=str)


class Main:

    def __init__(self, repo_owner: str, repo_name: str):
        self.owner = repo_owner
        self.repo = repo_name
        self.token = self.get_token()

    @staticmethod
    def get_token() -> str:
        env_name = 'GH_TOKEN'
        token = os.getenv(env_name)
        return token

    def get_request(self, url: str):
        """
            get_requests handles a GET request
            :param url: the URL to fetch
            :return: return the Response if OK or None
        """
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        if response.ok:
            return response
        return None

    def get_pr(self, number: str):
        """
            get_pr fetches a specific PR number
            :param number:
            :return: it returns a json-encoded PR
        """
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/pulls/{number}"
        response = self.get_request(url)
        try:
            pr_json = response.json()
            return pr_json
        except requests.exceptions.JSONDecodeError:
            print('Decoding JSON has failed')

    def get_prs(self, prs: list) -> list:
        """
            get_prs fetches a list of given PRs
            :param prs: a list of PRs number to fetch
            :return: a list of Pull Requests
        """
        prs_to_write = []
        for pr in prs:
            prs_to_write.append(self.get_pr(pr))
        return prs_to_write

    def search_issues(self, query: str, page: str):
        """
            search_issues search the issues from a given query
            :param query: contains the query string to fetch
            :param page: the query param for page
            :return: a list of PRs number
        """
        per_page = 100
        url = f"https://api.github.com/search/issues?q={query}&per_page={per_page}&page={page}"
        response = self.get_request(url)
        prs_number = []
        try:
            pr_json = response.json()
            for pr in pr_json['items']:
                prs_number.append(pr['number'])
        except requests.exceptions.JSONDecodeError:
            print('Decoding JSON has failed')

        return prs_number, response

    def fetch(self, query: str):
        """
            fetch handles the different steps of the script
            :param query: the query to fetch
        """
        page = 1
        next_page = True
        prs = []
        # handle pagination
        while next_page:
            issues, response = self.search_issues(query, str(page))
            prs = prs + issues
            if 'next' in response.links.keys():
                page += 1
            else:
                next_page = False

        to_write = self.get_prs(prs)
        write_prs_to_file(to_write)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        q = sys.argv[1]
    else:
        sys.exit(1)

    # Example of a query
    # "is:pr is:closed merged:2023-01-25..2023-02-01 repo:silvanocostanzo/gh-fetch"

    # get the Owner and the Repository from the query
    res = re.search('repo:(\w+)/([A-Za-z\-]+)', q)
    owner = res.group(1)
    repo = res.group(2)

    # launch the script
    gh = Main(owner, repo)
    gh.fetch(q)
