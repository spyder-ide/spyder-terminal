# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
#

"""
Configuration file for Pytest
NOTE: DO NOT add fixtures here. It could generate problems with
      QtAwesome being called before a QApplication is created.
"""

import os

os.environ['SPYDER_DEV'] = 'True'
