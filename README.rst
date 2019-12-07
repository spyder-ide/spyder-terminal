Spyder-Terminal
===============

Project status
--------------

|license| |pypi status| |pypi version| |conda version| |backers| |gitter|

Build status
------------
|circleci status| |appveyor status| |coverage| |crowdin|

.. |appveyor status| image:: https://ci.appveyor.com/api/projects/status/github/spyder-ide/spyder-terminal?branch=master&svg=true
   :target: https://ci.appveyor.com/project/spyder-ide/spyder-terminal
   :alt: Appveyor build status
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


*Copyright © 2017–2018 Spyder Project Contributors*

|linux-gif|

.. |linux-gif| image:: https://github.com/spyder-ide/spyder-terminal/blob/master/doc/example.gif?raw=true
   :alt: Animated GIF of Spyder-Terminal on Linux

----

Overview
--------

Spyder plugin for displaying an OS independent virtual terminal inside the main
Spyder window. Currently supports both Unix-like and Windows operating systems.

Spyder-Terminal allows you to easily execute any ``bash`` command inside
Spyder, even ``ncurses`` programs like ``nano`` or ``vi``;
or, on Windows, console applications such as ``powershell``.

|windows-gif|

.. |windows-gif| image:: https://github.com/spyder-ide/spyder-terminal/blob/master/doc/windows.gif?raw=true
   :alt: Animated GIF of Spyder-Terminal on Windows


Installation
------------
To install this plugin, you can use either ``pip`` or ``conda`` package
managers, as it follows:

Using pip:

::

 pip install spyder-terminal


Using conda:

::

    conda install spyder-terminal -c spyder-ide

Please be sure of installing a node and yarn version:

::
    conda install -c conda-forge nodejs yarn

Dependencies
------------

This project depends on

* `Spyder <https://github.com/spyder-ide/spyder>`_
* `Tornado <https://github.com/tornadoweb/tornado>`_
* `Pexpect <https://github.com/pexpect/pexpect>`_ (*nix Systems)
* `pywinpty <https://github.com/spyder-ide/pywinpty>`_ (Windows Systems)
* `Coloredlogs <https://github.com/xolox/python-coloredlogs>`_
* `xterm.js <https://github.com/sourcelair/xterm.js>`_


Changelog
---------

Visit our `CHANGELOG <https://github.com/spyder-ide/spyder-terminal/blob/master/CHANGELOG.md>`_
file to know more about our new features and improvements.

Server implementation
---------------------

Besides a Qt console, spyder-terminal also provides a web-based terminal
interface based on Tornado, which allows you to deploy and serve terminals
from a Web/Javascript frontend. To deploy only the server, you can execute
the following bash script:

::

    cd spyder_terminal/server

    # Shell option:

    # On Unix systems this can be bash/tcsh/zsh or any Unix shell:
    # bash: /usr/bin/env bash

    # On Windows systems this might be cmd or powershell:
    # cmd: %SystemRoot%\windows\system32\cmd.exe
    # powershell: %SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe

    python main.py --port <PORT> --shell <Path to the terminal backend to execute>

Build from source code
-------------------------

Install all the dependencies given in our `requirements file <https://github.com/spyder-ide/spyder-terminal/tree/master/requirements>`_
depending on your OS, a distribution of `node <https://nodejs.org/>`_ and
`yarn <https://yarnpkg.com/lang/en/>`_. Then, use the following bash script 
to build the plugin from source code.

::
    python setup.py build_static


Run tests
---------

In order to run our test suite, install the `dependencies <https://github.com/spyder-ide/spyder-terminal/blob/master/requirements/tests.txt>`_ for
tests and make sure spyder-terminal is already installed. Then, use pytest
to run the server and client tests for the terminal.

::
    pytest .


Development and contribution
----------------------------

To start contributing to this project, you must have installed the ``yarn``
package manager, then you can execute ``python setup.py install`` to test
your changes on Spyder. We follow PEP8 and PEP257 style guidelines.


~~~~~~~

Support us with a monthly donation and help us continue our activities.

.. image:: https://opencollective.com/spyder/backers.svg
   :target: https://opencollective.com/spyder#support
   :alt: Backers

Sponsors
~~~~~~~~

Become a sponsor to get your logo on our README on Github.

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
