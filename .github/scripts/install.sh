#!/bin/bash -ex

# Install dependencies
if [ "$OS" = "win" ]; then
    mamba install -q -y -c conda-forge --file requirements/windows.txt
else
    mamba install -q -y -c conda-forge --file requirements/unix.txt
fi


# Install test dependencies
mamba install -q -y -c conda-forge --file requirements/tests.txt

mamba install -q codecov
