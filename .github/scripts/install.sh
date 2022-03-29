#!/bin/bash -ex

# Install dependencies
if [[ "$OS" == "win" ]]
then
    mamba install -q -y -c conda-forge --file requirements/conda_win.txt
else
    mamba install -q -y -c conda-forge --file requirements/conda.txt
fi


# Install test dependencies
mamba install -q -y -c conda-forge --file requirements/tests.txt

mamba install -q codecov
