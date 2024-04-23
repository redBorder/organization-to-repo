## organization-to-repo

organization-to-repo is a tool designed to retrieve all released software from a specified organization and distribute them to respective repositories for RHEL9 systems. This tool is used in production at redborder for the delivery process.

### Installation

1. Install the required dependencies using pip:

   ```bash
   pip3 install -r requirements.txt
   ```

### Configuration

2. Open the .env file for configuration:
    ```bash
    vim .env
    ```
    
### Example .env file:

```plaintext
DOWNLOAD_DIR=/tmp                # Where to download the RPMs temporarily
SRC_RPMS_DIR=./src_rpms          # Where to store source RPMs
x86_64_RPMS_DIR=./x86_rpms       # Where to store RPMs
GITHUB_OAUTH_TOKEN=abcabcabc     # Your GitHub token
DISALLOW_REPO_LIST=my-cool-repo  # List of repositories to exclude (use commas to exclude more repos)
TOPIC=delivery                   # Topic of the repository to trigger the download
```

### Usage

3 -. You can set-up this to run on your jenkins host like we do in redborder or you can just trigger 

```bash
python3 __main__.py your_organization_here
```

And it will download the rpms and put in your repo

### License
AGLP-3.0

### Author
Miguel Álvarez <malvarez@redborder.com>
