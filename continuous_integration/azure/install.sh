#!/bin/bash -ex

# Install dependencies
conda install -q -y -c conda-forge --file requirements/conda.txt

# Install test dependencies
conda install -q -y -c spyder-ide --file requirements/tests.txt

conda install -q -y -c conda-forge nodejs=13

conda install -q -y -c conda-forge yarn

pip install -q codecov
