
"""
Setup base functions, taken from Jupyter Notebook project
https://github.com/jupyter/notebook/blob/master/setupbase.py
"""

from __future__ import print_function

import os
import pipes
import sys

from distutils import log
from distutils.cmd import Command
from subprocess import check_call

if sys.platform == 'win32':
    from subprocess import list2cmdline
else:
    def list2cmdline(cmd_list):
        return ' '.join(map(pipes.quote, cmd_list))

# -------------------------------------------------------------------------------
# Useful globals and utility functions
# -------------------------------------------------------------------------------

# A few handy globals
isfile = os.path.isfile
pjoin = os.path.join
repo_root = os.path.dirname(os.path.abspath(__file__))
is_repo = os.path.isdir(pjoin(repo_root, '.git'))
static = os.path.join(repo_root, 'spyder_terminal', 'server', 'static')


def mtime(path):
    """shorthand for mtime"""
    return os.stat(path).st_mtime


def oscmd(s):
    print(">", s)
    os.system(s)

# Py3 compatibility hacks, without assuming IPython itself is installed with
# the full py3compat machinery.


try:
    execfile
except NameError:
    def execfile(fname, globs, locs=None):
        locs = locs or globs
        exec(compile(open(fname).read(), fname, "exec"), globs, locs)


try:
    from shutil import which
except ImportError:
    # which() function copied from Python 3.4.3; PSF license
    def which(cmd, mode=os.F_OK | os.X_OK, path=None):
        """Given a command, mode, and a PATH string, return the path which
        conforms to the given mode on the PATH, or None if there is no such
        file.
        `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result
        of os.environ.get("PATH"), or can be overridden with a custom search
        path.
        """
        # Check that a given file can be accessed with the correct mode.
        # Additionally check that `file` is not a directory, as on Windows
        # directories pass the os.access check.
        def _access_check(fn, mode):
            return (os.path.exists(fn) and os.access(fn, mode) and
                    not os.path.isdir(fn))

        # If we're given a path with a directory part, look it up directly
        # rather than referring to PATH directories. This includes checking
        # relative to the current directory, e.g. ./script
        if os.path.dirname(cmd):
            if _access_check(cmd, mode):
                return cmd
            return None

        if path is None:
            path = os.environ.get("PATH", os.defpath)
        if not path:
            return None
        path = path.split(os.pathsep)

        if sys.platform == "win32":
            # The current directory takes precedence on Windows.
            if os.curdir not in path:
                path.insert(0, os.curdir)

            # PATHEXT is necessary to check on Windows.
            pathext = os.environ.get("PATHEXT", "").split(os.pathsep)
            # See if the given file matches any of the expected path extensions
            # This will allow us to short circuit when given "python.exe".
            # If it does match, only test that one, otherwise we have to try
            # others.
            if any(cmd.lower().endswith(ext.lower()) for ext in pathext):
                files = [cmd]
            else:
                files = [cmd + ext for ext in pathext]
        else:
            # On other platforms you don't have things like PATHEXT to tell you
            # what file suffixes are executable, so just pass on cmd as-is.
            files = [cmd]

        seen = set()
        for dir in path:
            normdir = os.path.normcase(dir)
            if normdir not in seen:
                seen.add(normdir)
                for thefile in files:
                    name = os.path.join(dir, thefile)
                    if _access_check(name, mode):
                        return name
        return None


def run(cmd, *args, **kwargs):
    """Echo a command before running it"""
    log.info('> ' + list2cmdline(cmd))
    kwargs['shell'] = (sys.platform == 'win32')
    return check_call(cmd, *args, **kwargs)


class Bower(Command):
    description = "fetch static client-side components with bower"
    user_options = [
        ('force', 'f', "force fetching of bower dependencies"),
    ]

    def initialize_options(self):
        self.force = False

    def finalize_options(self):
        self.force = bool(self.force)

    bower_dir = pjoin(static, 'components')
    node_modules = pjoin(repo_root, 'node_modules')

    def should_run(self):
        if self.force:
            return True
        if not os.path.exists(self.bower_dir):
            return True
        return mtime(self.bower_dir) < mtime(pjoin(repo_root, 'bower.json'))

    def run(self):
        if not self.should_run():
            print("bower dependencies up to date")
            return

        try:
            run(
                ['bower', 'install',
                 '--allow-root', '--config.interactive=false'],
                cwd=repo_root
            )
        except OSError as e:
            print("Failed to run bower: %s" % e, file=sys.stderr)
            print("You can install js dependencies with `bower install`",
                  file=sys.stderr)
            raise
        # self.patch_codemirror()
        # self.npm_components()
        os.utime(self.bower_dir, None)
        # update package data in case this created new files
        # update_package_data(self.distribution)
