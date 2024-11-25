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

import re

class RepoParser:
    
    @staticmethod
    def repo_url_to_repo_name(url):
        """
        Extracts the name of the repository from a GitHub URL.

        Args:
        url (str): The GitHub repository URL.

        Returns:
        str: The name of the repository.

        Raises:
        ValueError: If the provided URL is invalid or doesn't match the expected pattern.
        """
        try:
            match = re.search(r'/([^/]+)$', url)
            if match:
                repo_name = match.group(1)
                return repo_name
            else:
                raise ValueError("Invalid GitHub URL")
        except Exception as e:
            return None
        
    @staticmethod
    def parse_organization_and_repo(url):
        """
        Parses a GitHub URL to extract the organization and repository names.

        Args:
            url (str): The GitHub URL to parse.

        Returns:
            tuple: A tuple containing the organization name and repository name.

        Raises:
            ValueError: If the URL is not in a valid GitHub repository format.
        """
        pattern = r'^https:\/\/github\.com\/([^\/]+)\/([^\/]+)$'
        match = re.match(pattern, url)
        
        if not match:
            raise ValueError(f"Invalid GitHub URL: {url}")
        
        organization, repo = match.groups()
        return organization, repo
