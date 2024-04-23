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

import logging, os
from env.load import *
from parsers.arg import ArgParser
from parsers.repo import RepoParser
from organization.fetcher import OrgToRepos
from downloaders.assetdownloader import RpmDownloader
from repo.repoupdate import RepoUpdater

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main function to execute the program.
    """
    args = ArgParser.parse_arguments()
    repos = OrgToRepos(args.organization)
    rpm_downloader = RpmDownloader()

    download_rpms(repos, rpm_downloader)

    update_repo(os.getenv('SRC_RPMS_DIR'), "SRC")
    update_repo(os.getenv('x86_64_RPMS_DIR'), "x86")

def download_rpms(repos, rpm_downloader):
    """
    Downloads RPMs from repositories.

    param repos An object containing repositories to download from.
    param rpm_downloader An object responsible for downloading RPMs.
    """
    for repo in repos.repos:
        logging.info(f"Downloading assets from {repo}")
        repo_name = RepoParser.repo_url_to_repo_name(repo)
        assets = repos.get_latest_assets_release(repo_name)
        if assets:
            for asset in assets:
                logging.info(f"Downloading RPM from {asset}...")
                rpm_downloader.download_and_move_rpm(asset)
                logging.info("RPM downloaded and moved successfully.")

def update_repo(repo_dir, repo_type):
    """
    Updates a repository.

    param repo_dir The directory path of the repository to update.
    param repo_type The type of the repository (e.g., SRC, x86).
    """
    logging.info(f"Updating {repo_type} repo...")
    RepoUpdater.update_repo(repo_dir)

if __name__ == '__main__':
    main()