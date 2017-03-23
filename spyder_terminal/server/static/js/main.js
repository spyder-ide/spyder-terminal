var term,
    protocol,
    socketURL,
    socket,
    pid,
    charWidth,
    charHeight;

var terminalContainer = document.getElementById('terminal-container');

function setTerminalSize () {
  var cols = parseInt(colsElement.value, 10),
      rows = parseInt(rowsElement.value, 10),
      width = (cols * charWidth).toString() + 'px',
      height = (rows * charHeight).toString() + 'px';

  terminalContainer.style.width = width;
  terminalContainer.style.height = height;
  term.resize(cols, rows);
}

window.onresize = function(event) {
    term.fit();
}


createTerminal();

function createTerminal() {
  console.log("Creating term...");
  // Clean terminal
  while (terminalContainer.children.length) {
    terminalContainer.removeChild(terminalContainer.children[0]);
  }
  term = new Terminal({
    cursorBlink: true,
    scrollback: 5000,
    tabStopWidth: 8
  });
  // term.fit();
  term.on('resize', function (size) {
    if (!pid) {
      return;
    }
    term.fit();
    var cols = size.cols,
        rows = size.rows,
        url = '/api/terminals/' + pid + '/size?cols=' + cols + '&rows=' + rows;

    fetch(url, {method: 'POST'});
  });
  protocol = (location.protocol === 'https:') ? 'wss://' : 'ws://';
  socketURL = protocol + location.hostname + ((location.port) ? (':' + location.port) : '') + '/terminals/';

  term.open(terminalContainer);
  term.fit();

  var initialGeometry = term.proposeGeometry(),
      cols = initialGeometry.cols,
      rows = initialGeometry.rows;
  console.log(cols);
  console.log(rows);


  fetch('/api/terminals?cols=' + cols + '&rows=' + rows, {method: 'POST'}).then(function (res) {

    charWidth = Math.ceil(term.element.offsetWidth / cols);
    charHeight = Math.ceil(term.element.offsetHeight / rows);

    res.text().then(function (pid) {
      term.fit()
      window.pid = pid;
      socketURL += pid;
      socket = new WebSocket(socketURL);
      socket.onopen = runRealTerminal;
      socket.onclose = closeTerm;
      socket.onerror = closeTerm;
    });
  });
}

function closeTerm() {
  console.log("Closed via server");
  term.writeln("Pipe closed")
}

function runRealTerminal() {
  term.attach(socket);
  console.log("Am I Alive?");
  term._initialized = true;
}
