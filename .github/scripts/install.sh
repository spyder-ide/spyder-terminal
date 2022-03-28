#!/bin/bash -ex

# Install dependencies
mamba install -q -y -c conda-forge --file requirements/conda.txt

# Install test dependencies
mamba install -q -y -c conda-forge --file requirements/tests.txt

pip install -q codecov
