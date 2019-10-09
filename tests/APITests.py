import unittest
from unittest.mock import patch
from unittest.mock import Mock
from requests.exceptions import Timeout
from bs4 import BeautifulSoup
from flask import json

import sys
sys.path.insert(1, '.')
from Service import Service
import API

class ServiceTest(unittest.TestCase):

    def setUp(self) -> None:
        self.service = Service()
        self.request_parameters = {"keywords": ["openstack", "nova", "css"],
                                   "proxies": ["93.152.176.225:54136", "185.189.211.70:8080"],
                                   "type": "Repositories"
                                   }
        self.test_url = "https://github.com/search?utf8=✓&q=openstack+nova+css&type=Repositories"

    def test_prepare_search_url(self):
        actual = self.service.prepare_search_url(self.request_parameters)
        self.assertEqual(actual, self.test_url)

    @patch('Service.requests')
    def test_timeout_make_request(self, mock_requests):
        mock_requests.get.side_effect = Timeout
        with self.assertRaises(Timeout):
            self.service.make_request(self.test_url, self.request_parameters["proxies"])
            mock_requests.get.assert_called_once()

    @patch('random.choice')
    def test_random_proxy(self, mock_choice):
        mock_choice.return_value = "93.152.176.225:54136"
        random_proxy = self.service.random_proxy(self.request_parameters["proxies"])
        self.assertEqual("93.152.176.225:54136", random_proxy)

    @patch('Service.requests')
    def test_make_request(self, mock_requests):
        simple_html = "<!DOCTYPE html><html><body><h1>My First Heading</h1><p>My first paragraph.</p></body></html>"
        mock_requests.get.return_value = Mock(status_code=200, content=simple_html)
        response = self.service.make_request(self.test_url, self.request_parameters["proxies"])
        self.assertEqual(200, response.status_code)

    def test_get_page_content(self):
        simple_html = "<!DOCTYPE html><html><body><h1>My First Heading</h1><p>My first paragraph.</p></body></html>"
        mock_response = Mock(status_code=200, content=simple_html)
        page_content = self.service.get_page_content(mock_response)
        self.assertEqual(simple_html, page_content)

    def test_format_keywords(self):
        actual = self.service.format_keywords(self.request_parameters["keywords"])
        self.assertEqual('openstack+nova+css', actual)

    def test_extract_repositories_path(self):
        soup = BeautifulSoup('<!DOCTYPE html><html><body><ul class="repo-list"><li class="repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source" ><div class="flex-shrink-0 mr-2"><svg height="16" style="color: #6a737d" class="octicon octicon-repo" viewBox="0 0 12 16" version="1.1" width="12" aria-hidden="true"><path fill-rule="evenodd" d="M4 9H3V8h1v1zm0-3H3v1h1V6zm0-2H3v1h1V4zm0-2H3v1h1V2zm8-1v12c0 .55-.45 1-1 1H6v2l-1.5-1.5L3 16v-2H1c-.55 0-1-.45-1-1V1c0-.55.45-1 1-1h10c.55 0 1 .45 1 1zm-1 10H1v2h2v-1h3v1h5v-2zm0-10H2v9h9V1z"/></svg></div><div class="mt-n1"><div class="f4 text-normal"><a class="v-align-middle" data-hydro-click="{&quot;event_type&quot;:&quot;search_result.click&quot;,&quot;payload&quot;:{&quot;page_number&quot;:1,&quot;per_page&quot;:10,&quot;query&quot;:&quot;openstack nova css&quot;,&quot;result_position&quot;:1,&quot;click_id&quot;:55005225,&quot;result&quot;:{&quot;id&quot;:55005225,&quot;global_relay_id&quot;:&quot;MDEwOlJlcG9zaXRvcnk1NTAwNTIyNQ==&quot;,&quot;model_name&quot;:&quot;Repository&quot;,&quot;url&quot;:&quot;https://github.com/atuldjadhav/DropBox-Cloud-Storage&quot;},&quot;client_id&quot;:&quot;2140021149.1565620401&quot;,&quot;originating_request_id&quot;:&quot;8156:1EA09:2823E:4DC65:5D9DC481&quot;,&quot;originating_url&quot;:&quot;https://github.com/search?utf8=%E2%9C%93&amp;q=openstack+nova+css&amp;type=Repositori&quot;,&quot;referrer&quot;:null,&quot;user_id&quot;:47145676}}" data-hydro-click-hmac="35819dc837436e68a7588e75c44fc593a22a734169abeb84e63000890ff0d51a" href="/atuldjadhav/DropBox-Cloud-Storage">atuldjadhav/DropBox-Cloud-Storage</a></div><p class="mb-1">Technologies:- <em>Openstack</em> <em>NOVA</em>, NEUTRON, SWIFT, CINDER API\'s, JAVA, JAX-RS, MAVEN, JSON, HTML5, <em>CSS</em>, JAVASCRIPT, ANGUL…</p><div><div class="d-flex flex-wrap text-small text-gray"><div class="mr-3"><span><span class="repo-language-color" style="background-color: #563d7c"></span><span itemprop="programmingLanguage">CSS</span></span></div><div class="mr-3">Updated <relative-time datetime="2016-03-29T19:40:33Z" class="no-wrap">Mar 29, 2016</relative-time></div></div></div></div></li></ul></body>',"html.parser")
        repositories_path = self.service.extract_repositories_path(soup)
        self.assertEqual(["/atuldjadhav/DropBox-Cloud-Storage"], repositories_path)

    def test_extract_wikis_path(self):
        soup = BeautifulSoup(
            '<!DOCTYPE html><html><body><div id="wiki_search_results"><div ><div class="hx_hit-wiki py-4 border-top" ><a class="muted-link text-small text-bold" href="/vault-team/vault-website">vault-team/vault-website</a><div class="f4 text-normal"><a title="Quick installation guide" data-hydro-click="{&quot;event_type&quot;:&quot;search_result.click&quot;,&quot;payload&quot;:{&quot;page_number&quot;:1,&quot;per_page&quot;:10,&quot;query&quot;:&quot;openstack nova css&quot;,&quot;result_position&quot;:1,&quot;click_id&quot;:73172868,&quot;result&quot;:{&quot;id&quot;:73172868,&quot;global_relay_id&quot;:&quot;MDEwOlJlcG9zaXRvcnk3MzE3Mjg2OA==&quot;,&quot;model_name&quot;:&quot;Repository&quot;,&quot;url&quot;:&quot;https://github.com//vault-team/vault-website/wiki/Quick-installation-guide&quot;},&quot;client_id&quot;:&quot;2140021149.1565620401&quot;,&quot;originating_request_id&quot;:&quot;80FA:22EDE:3873058:557BC1F:5D9C8198&quot;,&quot;originating_url&quot;:&quot;https://github.com/search?q=openstack+nova+css&amp;type=Wikis&quot;,&quot;referrer&quot;:&quot;https://github.com/search?q=kaggle&amp;type=Wikis&quot;,&quot;user_id&quot;:47145676}}" data-hydro-click-hmac="c00168b320c13764dfad7a4f5d93c6d1d303859f4c2ebbce43223a7dea040ef6" href="/vault-team/vault-website/wiki/Quick-installation-guide">Quick installation guide</a></div><p class="mb-1 width-full">...  providers to access Vault API <em>Nova</em>: supports the deployment and management of virtual machines in the <em>OpenStack</em> cloud. A <em>Nova</em> instance is a virtual machine that runs inside <em>OpenStack</em> cloud Glance: manages ...</p><div class="f6 text-gray updated-at">Last updated<relative-time datetime="2017-05-03T04:35:32Z" class="no-wrap">May 3, 2017</relative-time></div></div></div></div></body></html>',
            "html.parser")
        repositories_path = self.service.extract_wikis_path(soup)
        self.assertEqual(['/vault-team/vault-website/wiki/Quick-installation-guide'], repositories_path )

    def test_extract_issues_path(self):
        soup = BeautifulSoup(
            '<!DOCTYPE html><html><body><div id="issue_search_results"><div class="issue-list"><div ><div class="issue-list-item d-flex py-4 hx_hit-issuepublic" data-repository-hovercards-enabled><svg height="16" class="octicon octicon-issue-opened open flex-shrink-0" viewBox="0 0 14 16" version="1.1" width="14" aria-hidden="true"><path fill-rule="evenodd" d="M7 2.3c3.14 0 5.7 2.56 5.7 5.7s-2.56 5.7-5.7 5.7A5.71 5.71 0 0 1 1.3 8c0-3.14 2.56-5.7 5.7-5.7zM7 1C3.14 1 0 4.14 0 8s3.14 7 7 7 7-3.14 7-7-3.14-7-7-7zm1 3H6v5h2V4zm0 6H6v2h2v-2z"/></svg><div class="ml-1 flex-auto "><div class="text-small"><a class="muted-link text-bold" data-hovercard-type="repository" data-hovercard-url="/novnc/websockify/hovercard" href="/novnc/websockify/issues">novnc/websockify</a><a class="muted-link text-gray-light" data-hovercard-type="repository" data-hovercard-url="/novnc/websockify/hovercard" href="/novnc/websockify/issues">#180</a></div><div class="f4 text-normal"><a title="str() cannot handle the message which contain non-ascii characters." data-hydro-click="{&quot;event_type&quot;:&quot;search_result.click&quot;,&quot;payload&quot;:{&quot;page_number&quot;:1,&quot;per_page&quot;:10,&quot;query&quot;:&quot;openstack nova css&quot;,&quot;result_position&quot;:1,&quot;click_id&quot;:91199482,&quot;result&quot;:{&quot;id&quot;:91199482,&quot;global_relay_id&quot;:&quot;MDU6SXNzdWU5MTE5OTQ4Mg==&quot;,&quot;model_name&quot;:&quot;Issue&quot;,&quot;url&quot;:&quot;https://github.com/novnc/websockify/issues/180&quot;},&quot;client_id&quot;:&quot;2140021149.1565620401&quot;,&quot;originating_request_id&quot;:&quot;8176:25B3:52984F4:7D3AA7C:5D9CFE97&quot;,&quot;originating_url&quot;:&quot;https://github.com/search?q=openstack+nova+css&amp;type=Issues&quot;,&quot;referrer&quot;:null,&quot;user_id&quot;:47145676}}" data-hydro-click-hmac="bc3d5e99ac3090ae32f3c357ebfe3c160632199dbfca601d74b025288819b409" href="/novnc/websockify/issues/180">str() cannot handle the message which contain non-ascii characters.</a></div><div class="text-gray mt-0"><span class="d-inline-block IssueLabel bg-gray v-align-text-top">bug</span></div><div class="d-flex text-small text-gray flex-wrap position-relative"><div class="d-inline mr-3"><a title="iamhappg" class="text-bold muted-link" href="/iamhappg">iamhappg</a>opened<relative-time datetime="2015-06-26T09:15:12Z" class="no-wrap">Jun 26, 2015</relative-time></div><span class="mr-3">5comments</span></div></div></div></div></div></div></body></html>',
            "html.parser")
        repositories_path = self.service.extract_issues_path(soup)
        self.assertEqual(['/novnc/websockify/issues/180'], repositories_path)

    @patch.object(Service, 'extract_wikis_path')
    @patch.object(Service, 'extract_issues_path')
    @patch.object(Service, 'extract_repositories_path')
    def test_extract_content(self, mock_extract_repositories_path, mock_extract_issues_path, mock_extract_wikis_path):
        mock_extract_repositories_path.return_value = ["/atuldjadhav/DropBox-Cloud-Storage"]
        mock_extract_wikis_path.return_value = ['/vault-team/vault-website/wiki/Quick-installation-guide']
        mock_extract_issues_path.return_value = ['/novnc/websockify/issues/180']

        repos = self.service.extract_content("", "repositories")
        issues = self.service.extract_content("", "issues")
        wikis = self.service.extract_content("", "wikis")
        wrong_type = self.service.extract_content("", "other")

        self.assertEqual(["/atuldjadhav/DropBox-Cloud-Storage"], repos)
        self.assertEqual(['/novnc/websockify/issues/180'], issues)
        self.assertEqual(['/vault-team/vault-website/wiki/Quick-installation-guide'], wikis)
        self.assertEqual(None, wrong_type)

    @patch("Service.requests.get")
    def test_scrape_results_urls(self, mock_request_get):
        mock_request_get.side_effect = Timeout
        error = self.service.scrape_results_urls(self.request_parameters)
        with self.assertRaises(Timeout):
            self.service.make_request(self.test_url, self.request_parameters["proxies"])
            mock_request_get.get.assert_called_once()

    def test_add_base_url(self):
        repo_urls = ["/atuldjadhav/DropBox-Cloud-Storage"]
        actual_urls = self.service.add_base_url(repo_urls)
        self.assertEqual(["https://github.com/atuldjadhav/DropBox-Cloud-Storage"], actual_urls)

class APITests(unittest.TestCase):
    def setUp(self):
        self.app = API.app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.request_parameters = {"keywords": ["openstack", "nova", "css"],
                                   "proxies": ["93.152.176.225:54136", "185.189.211.70:8080"],
                                   "type": "Repositories"
                                   }

    @patch.object(Service, 'scrape_results_urls')
    def test_prepare_response(self, mock_scrape_results_urls):
        headers = {'content-type': 'application/json'}
        mock_scrape_results_urls.return_value = ["https://github.com/atuldjadhav/DropBox-Cloud-Storage"]

        response = self.client.post(
            '/find_resource',
            data=json.dumps(self.request_parameters),
            headers=headers
        )

        self.assertTrue(response.status_code == 200)
        self.assertEqual([{'url': 'https://github.com/atuldjadhav/DropBox-Cloud-Storage'}], response.get_json())

        headers = {}
        response = self.client.post(
            '/find_resource',
            data=json.dumps(self.request_parameters),
            headers=headers
        )
        self.assertTrue(response.status_code == 400)
        self.assertEqual({'message': 'Request is not json'}, response.get_json())

        headers = {'content-type': 'application/json'}
        mock_scrape_results_urls.return_value = None
        response = self.client.post(
            '/find_resource',
            data=json.dumps(self.request_parameters),
            headers=headers
        )
        self.assertTrue(response.status_code == 400)
        self.assertEqual({"message": "Bad request"}, response.get_json())

if __name__ =="__main__":
    unittest.main()
