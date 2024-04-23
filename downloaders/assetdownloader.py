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

from downloaders.filedownloader import FileDownloader
import shutil, os, re

class RpmDownloader:
    def __init__(self):
        """
        Initializes an RpmDownloader object.

        This class provides methods to download and move RPM files.

        Attributes:
        file_downloader (FileDownloader): An instance of FileDownloader for downloading files.
        """
        self.file_downloader = FileDownloader()

    def download_and_move_rpm(self, url):
        """
        Downloads an RPM file from the specified URL and moves it to the appropriate destination folder.

        Args:
        url (str): The URL of the RPM file to download and move.
        """
        file_name = self.file_downloader.download_file(url)
        file_type, file_name = self.parse_asset(file_name)
        destination_folder = self.get_destination_folder(file_type)
        if file_type != "UNKNOWN":
            self.move_to_folder(file_name, destination_folder)

    @staticmethod
    def parse_asset(file_name):
        """
        Parses the type of RPM file from its name.

        Args:
        file_name (str): The name of the RPM file.

        Returns:
        tuple: A tuple containing the file type and the updated file name.
        """
        match = re.search(r'\.(\w+)\.rpm$', file_name)
        if match:
            file_type = match.group(1).upper()
        else:
            file_type = "UNKNOWN"
        return file_type, file_name

    @staticmethod
    def get_destination_folder(file_type):
        """
        Gets the destination folder for moving the RPM file based on its type.

        Args:
        file_type (str): The type of the RPM file.

        Returns:
        str: The destination folder path.
        """
        if file_type == "SRC":
            return os.getenv("SRC_RPMS_DIR")
        return os.getenv("x86_64_RPMS_DIR")

    @staticmethod
    def move_to_folder(file_name, destination_folder):
        """
        Moves the RPM file to the specified destination folder.

        Args:
        file_name (str): The name of the RPM file.
        destination_folder (str): The destination folder path.
        """
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        shutil.move(os.path.join(FileDownloader.DOWNLOAD_DIR, file_name), os.path.join(destination_folder, file_name))

