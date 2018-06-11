Spyder-Terminal
===============

|license| |pypi status| |pypi version| |conda version|
|circleci status| |appveyor status| |coverage| |backers| |gitter|

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

*Copyright © 2017–2018 Spyder Project Contributors*

|linux-gif|

.. |linux-gif| image:: https://github.com/spyder-ide/spyder-terminal/blob/master/doc/example.gif?raw=true
   :alt: Animated GIF of Spyder-Terminal on Linux

----

Plugin development paused until Spyder 4 release
------------------------------------------------

Currently, work on official Spyder plugins is paused to focus our limited
resources on the development and release of Spyder 4, the next generation
of the Scientific Python Development Environment.  Thanks to your continuing
support, we are on track for the final release of Spyder 4 in early 2019
with many highly anticipated features, including exposing a new public API for
external plugins, to make them easier to develop and more powerful.
Once that happens, active plugin development will resume, to add new features
and fix outstanding bugs. However, organizations or the community are welcome
to offer funding to continue development sooner; if so, please `contact us`_!

Spyder development is made possible by contributions from our global user
community, along with organizations like `NumFOCUS`_ and `Quansight`_.
There are numerous `ways you can help`_, many of which don't require any
programming. If you'd like to make a `donation`_  to help fund further
improvements, we're on `OpenCollective`_.

Thanks for all you do to make the Spyder project thrive! `More details`_

.. _contact us: mailto:ccordoba12@gmail.com
.. _NumFOCUS: https://www.numfocus.org
.. _Quansight: https://www.quansight.com
.. _ways you can help: https://github.com/spyder-ide/spyder/wiki/Contributing-to-Spyder
.. _donation: https://opencollective.com/spyder/donate
.. _OpenCollective: https://opencollective.com/spyder
.. _More details: https://github.com/spyder-ide/spyder/wiki/Current-Funding-and-Development-Status

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
