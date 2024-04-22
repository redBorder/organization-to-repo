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
from env.load import load_environment_variables
from parsers.arg import ArgParser
from parsers.repo import RepoParser
from organization.fetcher import OrgToRepos
from organization.gitapi import GitHubAPI
from downloaders.assetdownloader import RpmDownloader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_rpms_for_organization(organization, rpm_downloader):
    repos = OrgToRepos(GitHubAPI(), organization)
    for repo in repos.repos:
        repo_name = RepoParser.repo_url_to_repo_name(repo)
        assets = repos.get_latest_assets_release(repo_name)
        if assets:
            for asset in assets:
                logging.info(f"Downloading RPM from {asset}...")
                rpm_downloader.download_and_move_rpm(asset)
                logging.info(f"RPM downloaded and moved successfully.")

def main():
    try:
        load_environment_variables()
        args = ArgParser.parse_arguments()
        rpm_downloader = RpmDownloader()
        download_rpms_for_organization(args.organization, rpm_downloader)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
