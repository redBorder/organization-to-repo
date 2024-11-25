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
import re
import requests

class FileDownloader:
    
    DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR")
    GITHUB_TOKEN = os.getenv("GITHUB_OAUTH_TOKEN")

    def __init__(self):
        """
        Initializes a FileDownloader object.

        This class provides methods to download files from URLs.

        Attributes:
        session (requests.Session): A session object for making HTTP requests.
        """
        self.session = requests.Session()

    def download_file(self, asset, organization, repo):
        """
        Downloads a file from the specified URL.

        Args:
        url (str): The URL of the file to download.

        Returns:
        str: The name of the downloaded file.

        Raises:
        requests.HTTPError: If the download fails.
        """
        self.session.headers.update({"Authorization": f"token {self.GITHUB_TOKEN}"})
        self.session.headers.update({"Accept": "application/octet-stream"})

        url = f"https://api.github.com/repos/{organization}/{repo}/releases/assets/{asset['id']}"
        pattern = r"https:\/\/github.com\/.+\/download\/.+\/((.+).rpm)"

        match = re.search(pattern, asset["url"])

        if match:
            file_name = match.group(1)

        response = self.session.get(url, stream=True)
        response.raise_for_status()
        download_path = os.path.join(self.DOWNLOAD_DIR, file_name)
        
        with open(download_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return file_name