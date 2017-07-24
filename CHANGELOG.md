## Version 0.2 (2017/07/24)

### Issues Closed

* [Issue 90](https://github.com/spyder-ide/spyder-terminal/issues/90) - Windows: Close websocket when a console is closed manually
* [Issue 85](https://github.com/spyder-ide/spyder-terminal/issues/85) - Update package dependencies on Windows
* [Issue 84](https://github.com/spyder-ide/spyder-terminal/issues/84) - Release 0.2
* [Issue 83](https://github.com/spyder-ide/spyder-terminal/issues/83) - Enable AppVeyor CI for Windows testing
* [Issue 79](https://github.com/spyder-ide/spyder-terminal/issues/79) - Bold font may not be activated on new terminals
* [Issue 77](https://github.com/spyder-ide/spyder-terminal/issues/77) - Execute initial commands only if prompt is available
* [Issue 76](https://github.com/spyder-ide/spyder-terminal/issues/76) - Copy and Paste shortcuts are disabled
* [Issue 72](https://github.com/spyder-ide/spyder-terminal/issues/72) - clear command does not work
* [Issue 71](https://github.com/spyder-ide/spyder-terminal/issues/71) - Tabify terminal next to the IPython console
* [Issue 70](https://github.com/spyder-ide/spyder-terminal/issues/70) - Use check_compatibility for PyQt4
* [Issue 69](https://github.com/spyder-ide/spyder-terminal/issues/69) - Make 0.2 to depend on Spyder 3.2
* [Issue 64](https://github.com/spyder-ide/spyder-terminal/issues/64) - Add server tests
* [Issue 22](https://github.com/spyder-ide/spyder-terminal/issues/22) - Incorporate Windows version using pywinpty

In this release 13 issues were closed.

### Pull Requests Merged

* [PR 94](https://github.com/spyder-ide/spyder-terminal/pull/94) - PR: Restore previous font rescaling behaviour
* [PR 93](https://github.com/spyder-ide/spyder-terminal/pull/93) - PR: Simplify initialization routine
* [PR 91](https://github.com/spyder-ide/spyder-terminal/pull/91) - PR: Close websocket if process was stopped on Windows
* [PR 89](https://github.com/spyder-ide/spyder-terminal/pull/89) - PR: Don't raise plugin when a new terminal is created
* [PR 88](https://github.com/spyder-ide/spyder-terminal/pull/88) - PR: Add server tests
* [PR 87](https://github.com/spyder-ide/spyder-terminal/pull/87) - PR: Simplify new terminal actions
* [PR 86](https://github.com/spyder-ide/spyder-terminal/pull/86) - PR: Several installation fixes
* [PR 82](https://github.com/spyder-ide/spyder-terminal/pull/82) - PR: Copy and Paste shortcuts update
* [PR 80](https://github.com/spyder-ide/spyder-terminal/pull/80) - PR: Bold fonts are enabled by default
* [PR 78](https://github.com/spyder-ide/spyder-terminal/pull/78) - Emit initialization commands only if prompt is ready
* [PR 75](https://github.com/spyder-ide/spyder-terminal/pull/75) - PR: Version 0.2 depends on Spyder 3.2
* [PR 74](https://github.com/spyder-ide/spyder-terminal/pull/74) - PR: Tabify terminal next to the IPython Console
* [PR 73](https://github.com/spyder-ide/spyder-terminal/pull/73) - PR: Add plugin check_compatibility
* [PR 58](https://github.com/spyder-ide/spyder-terminal/pull/58) - PR: Extend spyder-terminal to Windows

In this release 14 pull requests were closed.

## Version 0.1.2 (2017/06/27)

### Issues Closed

* [Issue 61](https://github.com/spyder-ide/spyder-terminal/issues/61) - Capture all keyboard events when a console is on focus
* [Issue 60](https://github.com/spyder-ide/spyder-terminal/issues/60) - Redirect server output and errors to a file
* [Issue 59](https://github.com/spyder-ide/spyder-terminal/issues/59) - Don't start to create consoles until the server is up and running

In this release 3 issues were closed.

### Pull Requests Merged

* [PR 66](https://github.com/spyder-ide/spyder-terminal/pull/66) - Add Release notes
* [PR 65](https://github.com/spyder-ide/spyder-terminal/pull/65) - PR: Launch first console instance only if server is up
* [PR 63](https://github.com/spyder-ide/spyder-terminal/pull/63) - PR: Make the terminal to capture all keyboard events
* [PR 62](https://github.com/spyder-ide/spyder-terminal/pull/62) - PR: Redirecting server stderr and stdout to files

In this release 4 pull requests were closed.

## Version 0.1.1 (2017/05/12)

### Issues Closed

* [Issue 48](https://github.com/spyder-ide/spyder-terminal/issues/48) - Terminal content not re-scaling to plugin size
* [Issue 47](https://github.com/spyder-ide/spyder-terminal/issues/47) - Move terminal webview to be inside a QFrame so that dock panes in Spyder are uniform
* [Issue 46](https://github.com/spyder-ide/spyder-terminal/issues/46) - Rename plugin to "Terminal"
* [Issue 45](https://github.com/spyder-ide/spyder-terminal/issues/45) - Plugin "Options menu" is empty
* [Issue 44](https://github.com/spyder-ide/spyder-terminal/issues/44) - Make mouse wheel to work
* [Issue 43](https://github.com/spyder-ide/spyder-terminal/issues/43) - Getting annoying Qt warnings

In this release 6 issues were closed.

### Pull Requests Merged

* [PR 54](https://github.com/spyder-ide/spyder-terminal/pull/54) - PR: Added more options for opening terminals at different locations
* [PR 53](https://github.com/spyder-ide/spyder-terminal/pull/53) - PR: Fixed scroller issues
* [PR 52](https://github.com/spyder-ide/spyder-terminal/pull/52) - PR: Update font size and geometry after terminal has finished loading
* [PR 51](https://github.com/spyder-ide/spyder-terminal/pull/51) - PR: Update plugin name to Terminal
* [PR 50](https://github.com/spyder-ide/spyder-terminal/pull/50) - PR: Added Content-Type header to all HTTP requests
* [PR 49](https://github.com/spyder-ide/spyder-terminal/pull/49) - PR: Removed reference to contentsChanged signal
* [PR 42](https://github.com/spyder-ide/spyder-terminal/pull/42) - PR: Use sys.executable to start the server

In this release 7 pull requests were closed.


## Version 0.1 (2017/04/11)

### Issues Closed

* [Issue 37](https://github.com/spyder-ide/spyder-terminal/issues/37) - Each terminal should be numbered sequentially
* [Issue 34](https://github.com/spyder-ide/spyder-terminal/issues/34) - Terminals should use user-defined fonts
* [Issue 32](https://github.com/spyder-ide/spyder-terminal/issues/32) - Fix text overflow when commands fill all the terminal space
* [Issue 31](https://github.com/spyder-ide/spyder-terminal/issues/31) - Prevent running this plugin if Spyder is using PyQt4
* [Issue 27](https://github.com/spyder-ide/spyder-terminal/issues/27) - Don't hard code port number
* [Issue 24](https://github.com/spyder-ide/spyder-terminal/issues/24) - Add CI Engines and Minor Tests
* [Issue 21](https://github.com/spyder-ide/spyder-terminal/issues/21) - Each terminal instance should be launched on currently opened path
* [Issue 20](https://github.com/spyder-ide/spyder-terminal/issues/20) - Create basic terminal shortcuts
* [Issue 15](https://github.com/spyder-ide/spyder-terminal/issues/15) - Server should start and end with Spyder process
* [Issue 14](https://github.com/spyder-ide/spyder-terminal/issues/14) - Extract Javascript dependencies to a bower.json file
* [Issue 12](https://github.com/spyder-ide/spyder-terminal/issues/12) - Solve security access problem
* [Issue 10](https://github.com/spyder-ide/spyder-terminal/issues/10) - Display xterm terminal inside a QWebView widget
* [Issue 6](https://github.com/spyder-ide/spyder-terminal/issues/6) - Implement basic web bash console using tornado and xterm.js
* [Issue 4](https://github.com/spyder-ide/spyder-terminal/issues/4) - Add project skeleton
* [Issue 3](https://github.com/spyder-ide/spyder-terminal/issues/3) - Write package documentation and description

In this release 15 issues were closed.

### Pull Requests Merged

* [PR 40](https://github.com/spyder-ide/spyder-terminal/pull/40) - New terminals inherit Spyder current working directory
* [PR 39](https://github.com/spyder-ide/spyder-terminal/pull/39) - Server port is now variable
* [PR 38](https://github.com/spyder-ide/spyder-terminal/pull/38) - Terminal tabs naming convention is sequential
* [PR 36](https://github.com/spyder-ide/spyder-terminal/pull/36) - Plugin import is restricted to PyQt5
* [PR 35](https://github.com/spyder-ide/spyder-terminal/pull/35) - PR: Custom font loading
* [PR 33](https://github.com/spyder-ide/spyder-terminal/pull/33) - Overflow resolution
* [PR 30](https://github.com/spyder-ide/spyder-terminal/pull/30) - PR: Fix tests
* [PR 28](https://github.com/spyder-ide/spyder-terminal/pull/28) - PR: Basic test added
* [PR 26](https://github.com/spyder-ide/spyder-terminal/pull/26) - PR: Documentation and Changelog update
* [PR 25](https://github.com/spyder-ide/spyder-terminal/pull/25) - PR: Server deploys on port 8070 by default
* [PR 23](https://github.com/spyder-ide/spyder-terminal/pull/23) - PR: Added basic shortcuts and menu entries
* [PR 19](https://github.com/spyder-ide/spyder-terminal/pull/19) - Code cleanup: Removed useless font HTML examples
* [PR 18](https://github.com/spyder-ide/spyder-terminal/pull/18) - PR: setup.py now downloads bower components before installing the plugin
* [PR 17](https://github.com/spyder-ide/spyder-terminal/pull/17) - Added README screenshot
* [PR 16](https://github.com/spyder-ide/spyder-terminal/pull/16) - Server now starts and stops with Spyder process
* [PR 13](https://github.com/spyder-ide/spyder-terminal/pull/13) - Spyder IDE integration
* [PR 11](https://github.com/spyder-ide/spyder-terminal/pull/11) - PR: Terminal is now shown inside a Qt Widget
* [PR 9](https://github.com/spyder-ide/spyder-terminal/pull/9) - PR: Modified pexpect constructor orden between OSes
* [PR 8](https://github.com/spyder-ide/spyder-terminal/pull/8) - PR: Added Py3 Compatibility
* [PR 7](https://github.com/spyder-ide/spyder-terminal/pull/7) - PR: Web terminal proof-of-concept
* [PR 5](https://github.com/spyder-ide/spyder-terminal/pull/5) - Add plugin template skeleton

In this release 21 pull requests were closed.
