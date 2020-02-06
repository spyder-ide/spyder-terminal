#!/bin/bash -ex

# Install nomkl to avoid installing Intel MKL libraries 
if [ "$RUNNER_OS" = "linux" ]; then
    conda install -q -y nomkl
fi

if [ "$USE_CONDA" = "yes" ]; then

    # Install dependencies
    if [ "$RUNNER_OS" = "windows" ]; then
        conda install --file requirements/conda_win.txt -c conda-forge -q -y
    else
        conda install --file requirements/conda.txt -c conda-forge -q -y
    fi

    # Install test dependencies
    conda install --file requirements/tests.txt -c conda-forge -q -y

    # Install qt
    if [ "$RUNNER_OS" = "macos" ]; then
        conda install qt=5.9.6 -c conda-forge -q -y
    fi
else
    pip install pyqt5

    # Install dependencies
    if [ "$RUNNER_OS" = "windows" ]; then
        pip install -r requirements/conda_win.txt
    else
        pip install -r requirements/conda.txt
    fi

    # Install test dependencies
    pip install -r requirements/tests.txt

    if [ "$PYTHON_VERSION" = "3.7" ]; then
        pip install -U pywinpty
        pip install --pre -U spyder
    fi

fi

# Install nodejs
conda install nodejs -c conda-forge -q -y

# Install Yarn
conda install yarn -c conda-forge -q -y
