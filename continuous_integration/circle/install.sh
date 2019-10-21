#!/bin/bash -ex

# -- Install Miniconda
MINICONDA=Miniconda3-latest-Linux-x86_64.sh
wget https://repo.continuum.io/miniconda/$MINICONDA -O miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda
source $HOME/miniconda/etc/profile.d/conda.sh

# -- Make new conda environment with required Python version
conda create -y -n test python=$PYTHON_VERSION
conda activate test

# Install nomkl to avoid installing Intel MKL libraries 
conda install -q -y nomkl

# Install dependencies
conda install -q -y -c spyder-ide --file requirements/conda.txt

# Install test dependencies
conda install -q -y -c spyder-ide --file requirements/tests.txt

# Install nodejs
conda install -q -y -c conda-forge nodejs 

# -- Install Yarn
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt-get update && sudo apt-get install yarn
export PATH="$PATH:/opt/yarn-1.17.3/bin"

pip install -q codecov