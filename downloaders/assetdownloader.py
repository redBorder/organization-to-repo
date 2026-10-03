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
import logging
import os
import shutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RpmDownloader(FileDownloader):
    
    def __init__(self):
        """
        Initializes an RpmDownloader object.

        This class provides methods to download and move RPM files.
        """
        super().__init__()

    def download_and_move_rpm(self, asset, organization, repo):
        file_name = self.download_file(asset, organization, repo)
    
        if not file_name:
            logging.warning("RPM download returned no file name")
            return False
    
        file_type, file_name = self.parse_asset(file_name)
    
        logging.info(
            "Parsed RPM: file_name=%s, file_type=%s",
            file_name,
            file_type,
        )
    
        if file_type == "UNKNOWN":
            logging.warning("Unknown RPM type for file: %s", file_name)
            return False
    
        destination_folder = self.get_destination_folder(file_type)
    
        return self.move_to_folder(file_name, destination_folder)

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
        """
        if file_type == "SRC":
            destination_folder = os.getenv("SRC_RPMS_DIR")
        else:
            destination_folder = os.getenv("x86_64_RPMS_DIR")
    
        logging.info(
            "Destination folder for file_type=%s: %s",
            file_type,
            destination_folder,
        )
    
        return destination_folder
   
    @staticmethod
    def move_to_folder(file_name, destination_folder):
        source = os.path.join(FileDownloader.DOWNLOAD_DIR, file_name)
        destination = os.path.join(destination_folder, file_name)
    
        logging.info("Moving RPM from %s to %s", source, destination)
    
        if not destination_folder:
            logging.error("Destination folder is empty or not configured")
            return False
    
        if not os.path.exists(source):
            logging.error("Source RPM does not exist: %s", source)
            return False
    
        if not os.path.exists(destination_folder):
            logging.info("Creating destination folder: %s", destination_folder)
            os.makedirs(destination_folder)
    
        try:
            shutil.move(source, destination)
            logging.info("RPM moved successfully: %s", destination)
            return True
        except Exception:
            logging.exception("Error moving RPM")
            return False
   
