#!/bin/bash -ex

# Install dependencies
if [ "$OS" = "win" ]; then
    conda install -q -y -c conda-forge --file requirements/windows.txt
else
    conda install -q -y -c conda-forge --file requirements/unix.txt
fi


# Install test dependencies
conda install -q -y -c conda-forge --file requirements/tests.txt

conda install -q codecov
