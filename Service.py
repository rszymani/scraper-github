import requests
from requests.exceptions import Timeout
import random
from bs4 import BeautifulSoup


class Service:
    def __init__(self):
        self.base_url = "https://github.com"

    def scrape_results_urls(self, request_parameters):
        try:
            url = self.prepare_search_url(request_parameters)
            github_response = self.make_request(url, request_parameters["proxies"])
            github_content = self.get_page_content(github_response)
            urls = self.extract_content(github_content, request_parameters["type"])
            full_urls = self.add_base_url(urls)
            return full_urls
        except requests.exceptions.ProxyError as err:
            return err
        except Timeout as err:
            return err

    def prepare_search_url(self, request_parameters):
        formatted_keywords = self.format_keywords(request_parameters["keywords"])
        search_type = request_parameters["type"]
        url = "{}/search?utf8=✓&q={}&type={}".format(self.base_url, formatted_keywords, search_type)
        return url

    def make_request(self, url, proxies):
        proxies_dict = {"http": self.random_proxy(proxies), "https": self.random_proxy(proxies)}
        github_response = requests.get(url, proxies=proxies_dict, timeout=10)
        return github_response

    def get_page_content(self, github_response):
        github_html = github_response.content
        return github_html

    def format_keywords(self, keywords_list):
        return '+'.join(keywords_list)

    def random_proxy(self, proxies):
        return random.choice(proxies)

    def extract_content(self, response_content, search_type):
        soup = BeautifulSoup(response_content, 'html.parser')
        if search_type.lower() == "repositories":
            return self.extract_repositories_path(soup)
        elif search_type.lower() == "issues":
            return self.extract_issues_path(soup)
        elif search_type.lower() == "wikis":
            return self.extract_wikis_path(soup)
        else:
            return None

    def extract_repositories_path(self, soup):
        repos = []
        for repo_el in soup.findAll('ul', {'class': 'repo-list'}):
            for a in repo_el.findAll("a", {'class': 'v-align-middle'}):
                repos.append(a.get("href"))
        return repos

    def extract_wikis_path(self, soup):
        wikis = []
        for wiki_el in soup.findAll('div', {'id': 'wiki_search_results'}):
            for a in wiki_el.findAll("a", class_=False):
                href = a.get("href")
                if "/wiki/" in href:
                    wikis.append(a.get("href"))
        return wikis

    def extract_issues_path(self, soup):
        wikis = []
        for wiki_el in soup.findAll('div', {'id': 'issue_search_results'}):
            for a in wiki_el.findAll("a", class_=False):
                href = a.get("href")
                if "/issues/" in href or "/pull/" in href:
                    wikis.append(href)
        return wikis

    def add_base_url(self, repo_urls):
        full_urls = [self.base_url + url for url in repo_urls]
        return full_urls


