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

import argparse

class ArgParser:
    @staticmethod
    def parse_arguments():
        """
        Parses command-line arguments.

        Returns:
        argparse.Namespace: An object containing parsed arguments.
        """
        parser = argparse.ArgumentParser(description="Fetch GitHub organization repositories and assets.")
        parser.add_argument("organization", help="Name of the GitHub organization")
        return parser.parse_args()
