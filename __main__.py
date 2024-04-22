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


import logging
from env.load import *
from parsers.arg import ArgParser
from parsers.repo import RepoParser
from organization.fetcher import OrgToRepos
from organization.gitapi import GitHubAPI
from downloaders.assetdownloader import RpmDownloader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    args = ArgParser.parse_arguments()
    repos = OrgToRepos(GitHubAPI(), args.organization)
    rpm_downloader = RpmDownloader()
    for repo in repos.repos:
        repo_name = RepoParser.repo_url_to_repo_name(repo)
        assets = repos.get_latest_assets_release(repo_name)
        if assets:
            for asset in assets:
                logging.info(f"Downloading RPM from {asset}...")
                rpm_downloader.download_and_move_rpm(asset)
                logging.info(f"RPM downloaded and moved successfully.")