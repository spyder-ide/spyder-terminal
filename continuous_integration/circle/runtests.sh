#!/bin/bash -ex
set -ex

source $HOME/miniconda/etc/profile.d/conda.sh
conda activate test

nvm use v13.10.1

python setup.py build_static

# Run tests
python runtests.py

codecov