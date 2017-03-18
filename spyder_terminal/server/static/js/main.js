var term,
    protocol,
    socketURL,
    socket,
    pid,
    charWidth,
    charHeight;

var terminalContainer = document.getElementById('terminal-container');
    // optionElements = {
    //   cursorBlink: document.querySelector('#option-cursor-blink'),
    //   scrollback: document.querySelector('#option-scrollback'),
    //   tabstopwidth: document.querySelector('#option-tabstopwidth')
    // },
    // colsElement = document.getElementById('cols'),
    // rowsElement = document.getElementById('rows');

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

// colsElement.addEventListener('change', setTerminalSize);
// rowsElement.addEventListener('change', setTerminalSize);

// optionElements.cursorBlink.addEventListener('change', function () {
//   term.setOption('cursorBlink', optionElements.cursorBlink.checked);
// });
// optionElements.scrollback.addEventListener('change', function () {
//   term.setOption('scrollback', parseInt(optionElements.scrollback.value, 10));
// });
// optionElements.tabstopwidth.addEventListener('change', function () {
//   term.setOption('tabStopWidth', parseInt(optionElements.tabstopwidth.value, 10));
// });

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

  // colsElement.value = cols;
  // rowsElement.value = rows;

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
  // socket.send("ssdf");
}

// function runFakeTerminal() {
//   if (term._initialized) {
//     return;
//   }

//   term._initialized = true;

//   var shellprompt = '$ ';

//   term.prompt = function () {
//     term.write('\r\n' + shellprompt);
//   };

//   term.writeln('Welcome to xterm.js');
//   term.writeln('This is a local terminal emulation, without a real terminal in the back-end.');
//   term.writeln('Type some keys and commands to play around.');
//   term.writeln('');
//   term.prompt();

//   term.on('key', function (key, ev) {
//     console.log(key);
//     var printable = (
//       !ev.altKey && !ev.altGraphKey && !ev.ctrlKey && !ev.metaKey
//     );

//     if (ev.keyCode == 13) {
//       term.prompt();
//     } else if (ev.keyCode == 8) {
//      // Do not delete the prompt
//       if (term.x > 2) {
//         term.write('\b \b');
//       }
//     } else if (printable) {
//       term.write(key);
//     }
//   });

//   term.on('paste', function (data, ev) {
//     term.write(data);
//   });
// }
