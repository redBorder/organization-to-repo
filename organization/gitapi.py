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

import os
import requests

class GitHubAPI:
    
    BASE_URL = "https://api.github.com/"
    PER_PAGE = 100
    OAUTH_TOKEN = os.getenv("GITHUB_OAUTH_TOKEN")
    
    def __init__(self):
        """
        Initializes a GitHubAPI object.

        This class provides methods to interact with the GitHub API.

        Attributes:
        session (requests.Session): A session object for making HTTP requests.
        """
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/vnd.github.v3+json'})

    def get(self, url, params=None):
        """
        Sends a GET request to the specified URL.

        Args:
        url (str): The URL to send the request to.
        params (dict, optional): Parameters to include in the request.

        Returns:
        dict: The JSON response from the API.

        Raises:
        requests.HTTPError: If the request fails.
        """
        headers = {'Authorization': f'token {self.OAUTH_TOKEN}'}
        response = self.session.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()