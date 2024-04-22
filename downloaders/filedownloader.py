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

class FileDownloader:
    DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR")

    def __init__(self):
        """
        Initializes a FileDownloader object.

        This class provides methods to download files from URLs.

        Attributes:
        session (requests.Session): A session object for making HTTP requests.
        """
        self.session = requests.Session()

    def download_file(self, url):
        """
        Downloads a file from the specified URL.

        Args:
        url (str): The URL of the file to download.

        Returns:
        str: The name of the downloaded file.

        Raises:
        requests.HTTPError: If the download fails.
        """
        response = self.session.get(url, stream=True)
        response.raise_for_status()
        file_name = os.path.basename(url)
        download_path = os.path.join(self.DOWNLOAD_DIR, file_name)
        with open(download_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return file_name