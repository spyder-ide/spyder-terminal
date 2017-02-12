# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Setup script for spyder_terminal."""

# Standard library imports
import ast
import os

# Third party imports
from setuptools import find_packages, setup
import versioneer


HERE = os.path.abspath(os.path.dirname(__file__))

def get_description():
    """Get long description."""
    with open(os.path.join(HERE, 'README.rst'), 'r') as f:
        data = f.read()
    return data


REQUIREMENTS = ['spyder', 'pexpect', 'tornado']


setup(
    name='spyder_terminal',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    keywords=['Spyder', 'Plugin'],
    url='https://github.com/spyder-ide/spyder-ide',
    license='MIT',
    author='Spyder Project Contributors',
    author_email='admin@spyder-ide.org',
    description='Spyder Plugin for displaying a virtual terminal (OS independent) inside the main Spyder window',
    long_description=get_description(),
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=REQUIREMENTS,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ])
