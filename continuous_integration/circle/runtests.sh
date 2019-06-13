#!/bin/bash -ex
set -ex

source $HOME/miniconda/etc/profile.d/conda.sh
conda activate test

python setup.py build_static

# Run tests
python runtests.py

codecov