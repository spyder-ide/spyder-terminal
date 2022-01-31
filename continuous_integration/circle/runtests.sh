#!/bin/bash -ex
set -ex

source $HOME/miniforge/etc/profile.d/conda.sh
conda activate test

export NVM_DIR="/opt/circleci/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm use v13.10.1

python setup.py build_static

# Run tests
python runtests.py

codecov