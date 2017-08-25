spyder-terminal
===============

Spyder Plugin for displaying a virtual terminal (OS independent) inside the
main Spyder window. Currently it supports both Unix-like and Windows operating
systems.

This plugin allows you to execute flawlessly any bash command inside Spyder,
even ncurses applications like ``nano`` or ``vi``, or Windows console
applications such as ``powershell``.

Project information
-------------------

|license| |pypi version| |gitter|


Build status
------------

|circleci status| |appveyor status| |coverage|


.. |appveyor status| image:: https://img.shields.io/appveyor/ci/spyder-ide/spyder-terminal/master.svg
   :target: https://ci.appveyor.com/project/spyder-ide/spyder-terminal
   :alt: Appveyor build status
.. |circleci status| image:: https://img.shields.io/circleci/project/github/spyder-ide/spyder-terminal/master.svg
   :target: https://circleci.com/gh/spyder-ide/spyder-terminal/tree/master
   :alt: Circle-CI build status
.. |license| image:: https://img.shields.io/pypi/l/spyder-terminal.svg
   :target: LICENSE.txt
   :alt: License
.. |pypi version| image:: https://img.shields.io/pypi/v/spyder-terminal.svg
   :target: https://pypi.python.org/pypi/spyder-terminal
   :alt: Latest PyPI version
.. |gitter| image:: https://badges.gitter.im/spyder-ide/spyder-terminal.svg
   :target: https://gitter.im/spyder-ide/spyder-terminal
   :alt: Join the chat at https://gitter.im/spyder-ide/spyder-terminal
.. |coverage| image:: https://coveralls.io/repos/github/spyder-ide/spyder-terminal/badge.svg
   :target: https://coveralls.io/github/spyder-ide/spyder-terminal?branch=master
   :alt: Code Coverage


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


Dependencies
------------

This project depends on

1. `Spyder <https://github.com/spyder-ide/spyder>`_
2. `Tornado <https://github.com/tornadoweb/tornado>`_
3. `Pexpect <https://pexpect.sourceforge.net/pexpect.html>`_
4. `Coloredlogs <https://github.com/xolox/python-coloredlogs>`_
5. `xterm.js <https://github.com/sourcelair/xterm.js>`_

We provide Windows support thanks to the
`Pywinpty <https://github.com/spyder-ide/pywinpty>`_ Python bindings for
the awesome `Winpty <https://github.com/rprichard/winpty>`_ library.

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

Development and contribution
----------------------------

To start contributing to this project, you must have installed the ``bower``
package manager, then you can execute ``python setup.py install`` to test
your changes on Spyder. We follow PEP8 and PEP257 style guidelines.

Overview
--------

|linux-gif|

|windows-gif|

.. |linux-gif| image:: https://github.com/spyder-ide/spyder-terminal/blob/master/doc/example.gif?raw=true
   :alt: Linux animated gif

.. |windows-gif| image:: https://github.com/spyder-ide/spyder-terminal/blob/master/doc/windows.gif?raw=true
   :alt: Windows animated gif

