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

import subprocess

class RepoUpdater:

    @staticmethod
    def update_repo(repo_path):
        """
        Update the repository located at the specified path using createrepo command.

        Args:
            repo_path (str): The path to the repository.

        Raises:
            subprocess.CalledProcessError: If the command execution fails.
        """
        try:
            subprocess.run(["createrepo", "--update", repo_path], check=True)
            print(f"Repository at {repo_path} successfully updated.")
        except subprocess.CalledProcessError as e:
            print(f"Error updating repository at {repo_path}: {e}")
