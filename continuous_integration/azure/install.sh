#!/bin/bash -ex

# Install dependencies
conda install -q -y -c spyder-ide --file requirements/conda.txt

# Install test dependencies
conda install -q -y -c spyder-ide --file requirements/tests.txt

if [ $(uname) == Darwin ]; then
    conda install -q -y qt=5.9.6
fi

# Install nodejs
conda install -q -y -c conda-forge nodejs 

# Install yarn
conda install -q -y -c conda-forge yarn

pip install -q codecov