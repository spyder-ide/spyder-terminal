Spyder-Terminal
===============


Project status
--------------

|license| |pypi status| |pypi version| |conda version| |backers| |gitter|

Build status
------------
|circleci status| |Azure status| |coverage| |crowdin|

.. |Azure status| image:: https://dev.azure.com/spyder-ide/spyder-terminal/_apis/build/status/spyder-ide.spyder-terminal?branchName=master
   :target: https://dev.azure.com/spyder-ide/spyder-terminal/_build/latest?definitionId=2&branchName=master
   :alt: Azure build status
.. |circleci status| image:: https://img.shields.io/circleci/project/github/spyder-ide/spyder-terminal/master.svg
   :target: https://circleci.com/gh/spyder-ide/spyder-terminal/tree/master
   :alt: Circle-CI build status
.. |license| image:: https://img.shields.io/pypi/l/spyder-terminal.svg
   :target: LICENSE.txt
   :alt: License (MIT)
.. |pypi status| image:: https://img.shields.io/pypi/status/spyder-terminal.svg
   :target: https://github.com/spyder-ide/spyder-terminal
   :alt: PyPI development status
.. |pypi version| image:: https://img.shields.io/pypi/v/spyder-terminal.svg
   :target: https://pypi.org/project/spyder-terminal
   :alt: Latest PyPI version
.. |conda version| image:: https://img.shields.io/conda/vn/conda-forge/spyder-terminal.svg
   :target: https://anaconda.org/conda-forge/spyder-terminal
   :alt: Latest Conda-Forge version
.. |coverage| image:: https://coveralls.io/repos/github/spyder-ide/spyder-terminal/badge.svg
   :target: https://coveralls.io/github/spyder-ide/spyder-terminal?branch=master
   :alt: Coveralls Code Coverage
.. |gitter| image:: https://badges.gitter.im/spyder-ide/spyder-terminal.svg
   :target: https://gitter.im/spyder-ide/spyder-terminal
   :alt: Join the chat at https://gitter.im/spyder-ide/spyder-terminal
.. |backers| image:: https://opencollective.com/spyder/backers/badge.svg?color=blue
   :target: #backers
   :alt: OpenCollective Backers
.. |sponsors| image:: https://opencollective.com/spyder/sponsors/badge.svg?color=blue
   :target: #sponsors
   :alt: OpenCollective Sponsors
.. |crowdin| image:: https://badges.crowdin.net/spyder-terminal/localized.svg
   :target: https://crowdin.com/project/spyder-terminal
   :alt: Crowdin


*Copyright © 2017–2020 Spyder Project Contributors*

Overview
--------

This is a Spyder plugin for displaying an OS independent virtual terminal inside
the main Spyder window. It currently supports both Unix-like and Windows operating
systems.

Spyder-Terminal allows you to easily execute any ``bash`` command inside
Spyder, even ``ncurses`` programs like ``nano`` or ``vi``:

|linux-gif|

.. |linux-gif| image:: https://github.com/spyder-ide/spyder-terminal/blob/master/doc/example.gif?raw=true
   :alt: Animated GIF of Spyder-Terminal on Linux

On Windows you can run console applications such as ``IPython`` or ``powershell``:

|windows-gif|

.. |windows-gif| image:: https://github.com/spyder-ide/spyder-terminal/blob/master/doc/windows.gif?raw=true
   :alt: Animated GIF of Spyder-Terminal on Windows


Installation
------------

To install this plugin, you can use either the ``conda`` or ``pip`` package
managers, as follows:

Using conda:

::

    conda install spyder-terminal -c spyder-ide

Using pip (only if you don't use conda!):

::

    pip install spyder-terminal

**Note**: At the moment it is not possible to use this plugin with the
`Spyder installers <http://docs.spyder-ide.org/current/installation.html#standalone-installers>`_
for Windows and macOS. We're working to make that a reality in the future.

Dependencies
------------

This project depends on

* `Spyder <https://github.com/spyder-ide/spyder>`_
* `Tornado <https://github.com/tornadoweb/tornado>`_
* `Pexpect <https://github.com/pexpect/pexpect>`_ (Posix Systems)
* `pywinpty <https://github.com/spyder-ide/pywinpty>`_ (Windows Systems)
* `Coloredlogs <https://github.com/xolox/python-coloredlogs>`_
* `xterm.js <https://github.com/sourcelair/xterm.js>`_
* `Terminado <https://github.com/jupyter/terminado>`_

Changelog
---------

Visit our `CHANGELOG <https://github.com/spyder-ide/spyder-terminal/blob/master/CHANGELOG.md>`_
file to know more about our new features and improvements.

Server implementation
---------------------

Besides a Qt terminal, spyder-terminal also provides a web-based terminal
interface based on Tornado, which allows you to deploy and serve terminals
from a Web/Javascript frontend. To deploy only the server, you can execute
the following bash script:

::

    # Shell option:

    # On Unix systems this can be bash/tcsh/zsh or any Unix shell:
    # bash: /usr/bin/env bash

    # On Windows systems this might be cmd or powershell:
    # cmd: %SystemRoot%\windows\system32\cmd.exe
    # powershell: %SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe

    python -m spyder_terminal.server --port <PORT> --shell <Path to the terminal backend to execute>


Development and contribution
----------------------------

To start contributing to this project, you need to install the ``yarn``
and ``npm`` package managers. If you use conda, you can run the following
command to do that:

::

    conda install -c conda-forge nodejs yarn

Then, please install the package's dependencies with:

::

    conda create -n spyder-terminal-dev -c conda-forge --file requirements/{conda,conda_win}.txt

depending on your operating system.

Afterwards, you need to run

::

    python setup.py build_static

to build the Javascript components for this plugin.

Finally, in order to run our test suite, please install its required dependencies with

::

    conda install -c conda-forge --file requirements/tests.txt


and use pytest to run the server and client tests for the terminal like this

::

    pytest .


Sponsors
--------

Spyder is funded thanks to the generous support of

.. image:: https://static.wixstatic.com/media/095d2c_2508c560e87d436ea00357abc404cf1d~mv2.png/v1/crop/x_0,y_9,w_915,h_329/fill/w_380,h_128,al_c,usm_0.66_1.00_0.01/095d2c_2508c560e87d436ea00357abc404cf1d~mv2.png
   :target: https://www.quansight.com
   :alt: Quansight

.. image:: https://i2.wp.com/numfocus.org/wp-content/uploads/2017/07/NumFocus_LRG.png?fit=320%2C148&ssl=1
   :target: https://numfocus.org/
   :alt: Numfocus

And the donations we have received from our users around the world through `Open Collective <https://opencollective.com/spyder>`_:

.. image:: https://opencollective.com/spyder/sponsors.svg
   :target: https://opencollective.com/spyder#support
   :alt: Sponsors


More information
----------------

`Main Website <https://www.spyder-ide.org/>`_

`Download Spyder (with Anaconda) <https://www.anaconda.com/download/>`_

`Spyder Github <https://github.com/spyder-ide/spyder>`_

`Troubleshooting Guide and FAQ <https://github.com/spyder-ide/spyder/wiki/Troubleshooting-Guide-and-FAQ>`_

`Development Wiki <https://github.com/spyder-ide/spyder/wiki/Dev:-Index>`_

`Gitter Chatroom <https://gitter.im/spyder-ide/public>`_

`Google Group <https://groups.google.com/group/spyderlib>`_

`@Spyder_IDE on Twitter <https://twitter.com/spyder_ide>`_

`@SpyderIDE on Facebook <https://www.facebook.com/SpyderIDE/>`_

`Support Spyder on OpenCollective <https://opencollective.com/spyder/>`_
