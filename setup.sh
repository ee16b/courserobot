#!/bin/bash
# Run this script as root once upon VM initialization to set up the course manager infrastructure.

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi

if [[ ! -e "$HOME/credentials.sh" ]]; then
    echo "Credentials are required at ~/credentials.sh for the course robot. Please see credentials.sh.template for the format."
fi

if [[ ! -e "$HOME/user_credentials.sh" ]]; then
    echo "Credentials are required at ~/user_credentials.sh to initialize the course. It will be removed after the setup. Please see user_credentials.sh.template for the format."
fi

if [[ ! -e "$HOME/id_rsa" ]]; then
    echo "A private key is required for the course robot to function."
fi

if [[ ! -e "$HOME/general.yaml" ]]; then
    echo "general.yaml is required to configure the semester."
fi

# Use bash strict mode.
set -eux
set -o pipefail

# Change shell to bash to avoid any potential complications with legacy scripts.
echo "dash dash/sh boolean false" | debconf-set-selections
DEBIAN_FRONTEND=noninteractive dpkg-reconfigure dash

# Update package list.
apt-get update

# Shell
apt-get install -y mosh

# Build tools
apt-get install -y make python3-setuptools

# Development tools
apt-get install -y git tig npm nodejs

# Piazza image creation
apt-get install -y imagemagick

# LaTeX
apt-get install -y texlive-full

# Install pygithub
rm -rf pygithub_build
mkdir pygithub_build
pushd pygithub_build
wget https://github.com/PyGithub/PyGithub/archive/c5988c3980753edde628f86c2a5e84e5e4c2cc33.zip -O output.zip
unzip output.zip
cd PyGithub-*
python3 setup.py install
popd
rm -rf pygithub_build

# taft/handlebars
npm install -g taft
PATH=$HOME/.npm-packages/bin:$PATH
npm install --save -g handlebars-helpers
npm i handlebars-helper-moment --save-dev -g
npm install handlebars-fs --save -g

# Continue in user-mode setup.
sudo -H -u ubuntu ./setup_user.sh
