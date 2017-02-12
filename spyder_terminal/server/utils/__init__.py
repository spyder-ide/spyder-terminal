# -*- coding: utf-8 -*-

"""
utils module
=========

Provides:
    1. Windows compatibility layer

How to use the documentation
----------------------------
Documentation is available in one form: docstrings provided
with the code

Copyright (c) 2016, Edgar A. Margffoy.
MIT, see LICENSE for more details.
"""

import os
if os.name == 'nt':
    import utils.winpexpect
