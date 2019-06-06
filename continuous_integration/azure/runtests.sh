#!/bin/bash -ex

python setup.py build_static

# Run tests
python runtests.py

codecov