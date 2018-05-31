# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) Spyder Project Contributors
# Copyright (c) 2015-, Jupyter Development Team.
# Copyright (c) 2008-2015, IPython Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# -----------------------------------------------------------------------------

"""
General setup rules to download external JS dependencies
via Bower

Some functions were taken from the Jupyter Notebook
setupbase definition
See: https://github.com/jupyter/notebook/blob/master/setupbase.py
"""

import os
import os.path as osp
import pipes
import shutil
import sys

from distutils import log
from distutils.core import Command
from setuptools.command.develop import develop
from setuptools.command.sdist import sdist
from subprocess import check_call

if sys.platform == 'win32':
    from subprocess import list2cmdline
else:
    def list2cmdline(cmd_list):
        return ' '.join(map(pipes.quote, cmd_list))


HERE = os.path.abspath(os.path.dirname(__file__))
COMPONENTS = osp.join(HERE, 'spyder_terminal', 'server', 'static',
                      'components')


repo_root = os.path.dirname(os.path.abspath(__file__))


def run(cmd, *args, **kwargs):
    """Echo a command before running it"""
    log.info('> ' + list2cmdline(cmd))
    kwargs['shell'] = (sys.platform == 'win32')
    return check_call(cmd, *args, **kwargs)


class BuildStatic(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if not osp.isdir(COMPONENTS):
            log.info("running [yarn install]")
            run(['yarn', 'install'], cwd=repo_root)


class DevelopWithBuildStatic(develop):
    def install_for_development(self):
        self.run_command('build_static')
        return develop.install_for_development(self)


class SdistWithBuildStatic(sdist):
    def run(self):
        self.run_command('build_static')
        sdist.run(self)

    def make_distribution(self):
        if not osp.isdir(COMPONENTS):
            print("\nWARNING: Server components are missing!! We can't "
                  "proceed further!\n")
            sys.exit(1)
        return sdist.make_distribution(self)


class CleanComponents(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        log.info("Removing server components")
        shutil.rmtree(COMPONENTS, ignore_errors=True)
