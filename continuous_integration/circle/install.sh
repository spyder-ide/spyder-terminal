#!/bin/bash -ex

# -- Install Miniforge
MINIFORGE=Miniforge3-Linux-x86_64.sh
wget https://github.com/conda-forge/miniforge/releases/latest/download/$MINIFORGE -O miniforge.sh
bash miniforge.sh -b -p $HOME/miniforge
source $HOME/miniforge/etc/profile.d/conda.sh

# -- Make new conda environment with required Python version
conda create -y -n test python=$PYTHON_VERSION
conda activate test

# Install dependencies
conda install -q -y -c conda-forge --file requirements/conda.txt

# Install test dependencies
conda install -q -y -c conda-forge --file requirements/tests.txt

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm

nvm install v13.10.1

# -- Install Yarn
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt-get update && sudo apt-get -y install yarn
export PATH="$PATH:/opt/yarn-1.17.3/bin"

pip install -q codecov
