# spyder-terminal
Spyder Plugin for displaying a virtual terminal (OS independent) inside the main Spyder window. Currently it supports both Unix-like and Windows operating systems.

This plugin allows you to execute flawlessly any bash command inside spyder, even ncurses applications like ``nano`` or ``vi``, or Windows console applications such as ``powershell``.

## Project info
[![Project License](https://img.shields.io/pypi/l/spyder-terminal.svg)](./LICENSE.txt)
[![pypi version](https://img.shields.io/pypi/v/spyder-terminal.svg)](https://pypi.python.org/pypi/spyder-terminal)

## Build status
[![CircleCI](https://circleci.com/gh/spyder-ide/spyder-terminal.svg?style=svg)](https://circleci.com/gh/spyder-ide/spyder-terminal)
[![Build status](https://ci.appveyor.com/api/projects/status/cowkuaebgeeq45v1?svg=true)](https://ci.appveyor.com/project/spyder-ide/spyder-terminal)
[![Coverage Status](https://coveralls.io/repos/github/spyder-ide/spyder-terminal/badge.svg?branch=master)](https://coveralls.io/github/spyder-ide/spyder-terminal?branch=master)

## Installation
To install this plugin, you can use either ``pip`` or ``conda`` package managers, as it follows:

Using pip:
```
pip install spyder-terminal
```

Using conda:
```
conda install spyder-terminal -c spyder-ide
```

## Dependencies
This project depends on [Spyder](https://github.com/spyder-ide/spyder), [Tornado](https://github.com/tornadoweb/tornado), [pexpect](https://pexpect.sourceforge.net/pexpect.html) and [Coloredlogs](https://github.com/xolox/python-coloredlogs). It also depends on [xterm.js](https://github.com/sourcelair/xterm.js/)

We provide Windows support thanks to the awesome [pywinpty](https://github.com/spyder-ide/pywinpty) pyhton bindings for [winpty](https://github.com/rprichard/winpty).

## Changelog
Visit our [CHANGELOG](CHANGELOG.md) file to know more about our new features and improvements.

## Server implementation
Besides a Qt console, spyder-terminal also provides a web-based terminal interface based on Tornado, which allows you to deploy and serve terminals from a Web/Javascript frontend. To deploy only the server, you can execute:

```bash
cd spyder_terminal/server

# Shell option:

# On Unix systems this can be bash/tcsh/zsh or any Unix shell:
# bash: /usr/bin/env bash

# On Windows systems this might be cmd or powershell:
# cmd: %SystemRoot%\windows\system32\cmd.exe
# powershell: %SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe

python main.py --port <PORT> --shell <Path to the terminal backend to execute>

```

## Development and contribution
To start contributing to this project, you must have installed ``bower`` package manager, then you can execute ``python setup.py install`` to test your changes on Spyder. We follow PEP8 and PEP257 style guidelines.

# Overview
![alt tag](/doc/example.gif)
![alt tag](/doc/windows.gif)
