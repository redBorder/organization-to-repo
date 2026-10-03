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

import logging, os, time
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
    start_time = time.monotonic()

    args = ArgParser.parse_arguments()
    repos = OrgToRepos(args.organization)
    rpm_downloader = RpmDownloader()

    download_rpms(repos, rpm_downloader)

    update_repo(os.getenv('SRC_RPMS_DIR'), "SRC")
    update_repo(os.getenv('x86_64_RPMS_DIR'), "x86")

    elapsed = int(time.monotonic() - start_time)
    logging.info(f"Execution finished in {elapsed // 60}m {elapsed % 60}s")

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
        organization, repo = RepoParser.parse_organization_and_repo(repo)

        if assets:
            for asset in assets:
                file_name = asset.get("name")

                if not file_name:
                    file_name = os.path.basename(asset.get("url", ""))

                if not file_name.lower().endswith(".rpm"):
                    logging.info(f"Skipping {file_name}: not an RPM file.")
                    continue

                asset = {
                    **asset,
                    "name": file_name,
                }

                if rpm_downloader.is_in_repo(asset):
                    logging.info(f"Skipping {file_name}: already in the repo.")
                    continue

                logging.info(f"Downloading RPM from {file_name}...")

                if rpm_downloader.download_and_move_rpm(
                    asset, organization, repo
                ):
                    logging.info(
                        f"RPM {file_name} downloaded and moved successfully."
                    )

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
