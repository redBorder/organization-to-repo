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
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        Downloads an RPM file from a GitHub release.

        Non-RPM assets are skipped without downloading them.

        Args:
            asset (dict): GitHub release asset.
            organization (str): GitHub organization.
            repo (str): GitHub repository.

        Returns:
            str | None: The name of the downloaded file, or None if the
            asset is not an RPM.
        """
        file_name = asset.get("name")

        logging.info(
            "GitHub asset: name=%r, id=%r, browser_download_url=%r",
            file_name,
            asset.get("id"),
            asset.get("browser_download_url"),
        )

        # Skip assets without a name
        if not file_name:
            logging.warning(
                "Skipping GitHub asset because it has no name: %r",
                asset,
            )
            return None

        # Skip non-RPM assets
        if not file_name.lower().endswith(".rpm"):
            logging.warning(
                "Skipping non-RPM asset: %r",
                file_name,
            )
            return None

        self.session.headers.update({
            "Authorization": f"token {self.GITHUB_TOKEN}",
            "Accept": "application/octet-stream",
        })

        url = (
            f"https://api.github.com/repos/{organization}/{repo}"
            f"/releases/assets/{asset['id']}"
        )

        logging.info(
            "Downloading RPM from GitHub API: %s",
            url,
        )

        response = self.session.get(url, stream=True)

        logging.info(
            "GitHub response for %s: status=%s, content-type=%s",
            file_name,
            response.status_code,
            response.headers.get("Content-Type"),
        )

        response.raise_for_status()

        download_path = os.path.join(self.DOWNLOAD_DIR, file_name)

        logging.info(
            "Saving RPM to: %s",
            download_path,
        )

        with open(download_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        if not os.path.exists(download_path):
            logging.error(
                "RPM download completed but file does not exist: %s",
                download_path,
            )
            return None

        logging.info(
            "RPM downloaded successfully: %s",
            download_path,
        )

        return file_name



