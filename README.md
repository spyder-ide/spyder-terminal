# spyder-terminal
Spyder Plugin for displaying a virtual terminal (OS independent) inside the main Spyder window. Currently it only supports Unix and Unix-like operating systems.

This plugin allows you to execute flawlessly any bash command inside spyder, even ncurses applications like ``nano`` or ``vi``.

## Installation
To install this plugin, you can use either ``pip`` or ``conda`` package managers, as it follows:

Using pip:
```
pip install spyder-terminal
```

Using conda:
```
conda install spyder-terminal
```

## Dependencies
This project depends on [Spyder](https://github.com/spyder-ide/spyder), [Tornado](https://github.com/tornadoweb/tornado), [pexpect](pexpect.sourceforge.net/pexpect.html) and [Coloredlogs](https://github.com/xolox/python-coloredlogs). It also depends on [xterm.js](https://github.com/sourcelair/xterm.js/)

## Changelog
Visit our [CHANGELOG](CHANGELOG.md) file to know more about our new features and improvements.

## Development and contribution
To start contributing to this project, you must have installed ``bower`` package manager, then you can execute ``python setup.py install`` to test your changes on Spyder. We follow PEP8 and PEP257 style guidelines.

# Overview
![alt tag](/doc/example.gif)
