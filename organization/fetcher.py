###################################################################
# This file is licensed under the Affero General Public License   #
#                  Version 3 (AGPLv3)                             #
#                                                                 #
# You should have received a copy of the GNU Affero General       #
# Public License along with this program. If not, see             #
# <https://www.gnu.org/licenses/agpl-3.0.html>.                   #
#                                                                 #
# Author: malvarez@redborder.com                                  #
###################################################################

import requests, os

class OrgToRepos:
    DISALLOW_REPO_LIST = os.getenv('DISALLOW_REPO_LIST').split(',')
    TOPIC = os.getenv('TOPIC')
    
    def __init__(self, api, organization):
        """
        Initializes an OrgToRepos object.

        Args:
        api (GitHubAPI): An instance of GitHubAPI for making API requests.
        organization (str): The name of the GitHub organization.
        """
        self.api = api
        self.organization = organization
        self.repos = []
        self.get_github_organization_repositories()

    def get_github_organization_repositories(self):
        """
        Retrieves the repositories belonging to the specified GitHub organization.

        Populates the 'repos' attribute with the URLs of the organization's repositories.
        """
        url = f"{self.api.BASE_URL}orgs/{self.organization}/repos"
        try:
            page = 1
            while True:
                params = {'per_page': self.api.PER_PAGE, 'page': page}
                repos = self.api.get(url, params=params)
                if not repos:
                    break
                for repo in repos:
                    if self.TOPIC in repo["topics"] and repo['name'] not in self.DISALLOW_REPO_LIST:
                        self.repos.append(repo['html_url'])
                page += 1
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
    
    def get_latest_assets_release(self, repo_name):
        """
        Retrieves the URLs of the latest assets release for a specified repository.

        Args:
        repo_name (str): The name of the repository.

        Returns:
        list or None: A list of URLs of the assets, or None if no assets are found.

        """
        url = f"{self.api.BASE_URL}repos/{self.organization}/{repo_name}/releases/latest"
        try:
            release = self.api.get(url)
            if 'message' in release and release['message'] == 'Not Found':
                return None
            assets = release.get('assets', [])
            asset_urls = [asset['browser_download_url'] for asset in assets]
            return asset_urls
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching latest assets of {repo_name}: {e}")
            return None
