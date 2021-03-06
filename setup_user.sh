#!/bin/bash
# User-mode setup script.
# Do not call directly.

debug_mode="no" # set to yes to debug

if [[ $EUID -eq 0 ]]; then
    echo "This script must not be run as root"
    exit 1
fi

if [[ "$_SETUP_MAGIC" == "magic123456" ]]; then
    echo "This script must not be run directly"
    exit 1
fi

# Use bash strict mode.
set -eux
set -o pipefail

# Get semester tag
export SEMESTER_TAG=$(./scripts/read_tag.py $HOME/general.yaml)

# Pull in credentials.
source $HOME/credentials.sh
source $HOME/user_credentials.sh

# Remove user_credentials since they are sensitive
if [[ $debug_mode != "yes" ]]; then
    rm $HOME/user_credentials.sh
fi

# Git config
git config --global user.name "ee16b-robot"
git config --global user.email "ee16b-robot@lists.berkeley.edu"

# Import ssh key
mkdir -p ~/.ssh
cp $HOME/id_rsa ~/.ssh/
if [[ $debug_mode != "yes" ]]; then
    rm $HOME/id_rsa
fi
chmod 600 ~/.ssh/id_rsa

# Disable ssh warnings for headless processing
cat <<EOF >> ~/.ssh/config
Host github.com
  StrictHostKeyChecking no
  UserKnownHostsFile=/dev/null
Host cory.eecs.berkeley.edu
  StrictHostKeyChecking no
  UserKnownHostsFile=/dev/null
EOF

# Create source repo (xxxx-www-src.git)
./create_src_repo.py "$GITHUB_USER" "$GITHUB_PASSWORD" "$SEMESTER_TAG-www-src" "Website files for $SEMESTER_TAG"

# Clone source repo locally
git clone git@github.com:ee16b/www-src-template.git "$HOME/$SEMESTER_TAG-www-src"
pushd "$HOME/$SEMESTER_TAG-www-src"
rm -rf .git
cp $HOME/general.yaml .
if [[ $debug_mode != "yes" ]]; then
    rm $HOME/general.yaml
fi
git init
git add -A
git commit -m "Initial commit"
git remote add origin git@github.com:ee16b/$SEMESTER_TAG-www-src.git
git push -u origin master
popd

# Clone directories
git clone git@github.com:ee16b/ee16b-lab.git ~/lab_repo
lab_dir=$(readlink -f ~/lab_repo)
git clone git@github.com:ee16b/ee16b-content.git ~/content_repo
content_dir=$(readlink -f ~/content_repo)

# Set up inst
ssh ee16b@cory.eecs.berkeley.edu "cd ~/public_html/ && git clone git@github.com:ee16b/www-framework.git $SEMESTER_TAG"
ssh ee16b@cory.eecs.berkeley.edu "cd ~/public_html/$SEMESTER_TAG/ && git clone git@github.com:ee16b/$SEMESTER_TAG-www-src.git src"

# Export environment variables
cat <<EOF > $HOME/env_vars.sh
source $HOME/credentials.sh
export RELEASE_LOC=$HOME/$SEMESTER_TAG-www-src
export GENERAL_YAML=$HOME/$SEMESTER_TAG-www-src/general.yaml
export MAKEFILE_LOC=$PWD
export HW_LOC=$content_dir/$SEMESTER_TAG/hws
export DISC_LOC=$content_dir/$SEMESTER_TAG/discussion
export CONTENT_REPOS=$lab_dir:$content_dir

export PATH=$PATH:$PWD/scripts
EOF

# Add to bashrc
echo "source $HOME/env_vars.sh" >> ~/.bashrc
