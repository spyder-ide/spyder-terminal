#!/bin/bash -ex

if [[ $OS == 'win']]; then
    mamba install -q -y -c conda-forge --file requirements/conda_win.txt
else
    # Install dependencies
    mamba install -q -y -c conda-forge --file requirements/conda.txt
fi


# Install test dependencies
mamba install -q -y -c conda-forge --file requirements/tests.txt

pip install -q codecov
