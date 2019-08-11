import { Terminal } from 'xterm';
import { AttachAddon } from 'xterm-addon-attach';
import { FitAddon } from 'xterm-addon-fit';
import { SearchAddon, ISearchOptions } from 'xterm-addon-search';
import { WebLinksAddon } from 'xterm-addon-web-links';
import { WebglAddon } from 'xterm-addon-webgl';

let term;
let fitAddon;
let searchAddon;
let protocol;
let socketURL;
let socket;
let pid;

const terminalContainer = document.getElementById('terminal-container');

function createTerminal(){
  // Clean terminal
  while (terminalContainer.children.length) {
      terminalContainer.removeChild(terminalContainer.children[0]);
  }

  const isWindows = ['Windows', 'Win16', 'Win32', 'WinCE'].indexOf(navigator.platform) >= 0;

  term = new Terminal({
      cursorBlink: true,
      scrollback: 10000,
      tabStopWidth: 10,
      windowsMode: isWindows
      });

  term.loadAddon(new WebLinksAddon());
  searchAddon = new SearchAddon();
  term.loadAddon(searchAddon);
  fitAddon = new FitAddon();
  term.loadAddon(fitAddon);
  
  term.on('resize', (size) => {
      if (!pid) {
          return;
      }
      term.fit();
      let cols = size.cols;
      let rows = size.rows;
      let url = '/api/terminals/' + pid + '/size?cols=' + cols + '&rows=' + rows;

      fetch(url, {method: 'POST', headers: myHeaders});
  });

  protocol = (location.protocol === 'https:') ? 'wss://' : 'ws://';
  socketURL = protocol + location.hostname + ((location.port) ? (':' + location.port) : '') + '/terminals/';
  
  term.open(terminalContainer);
  fitAddon.fit();
  term.focus();
  term.toggleFullscreen(true);

  let initialGeometry = term.proposeGeometry();
  let cols = initialGeometry.cols;
  let rows = initialGeometry.rows;
  console.log(cols);
  console.log(rows);

  fetch('/api/terminals?cols=' + cols + '&rows=' + rows, {
    method: 'POST',
    headers: myHeaders,
    credentials: 'include'
  }).then(function (res) {
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

function getFonts() {
  return document.getElementById('.terminal').css('font-family');
}

function setFont(font) {
  fonts = "'Ubuntu Mono', monospace";
  fonts = "'"+font+"', "+fonts;
  document.getElementById('.terminal').css('font-family', fonts);

  term.fit();
  let initialGeometry = term.proposeGeometry();
  let cols = initialGeometry.cols;
  let rows = initialGeometry.rows;
}

function fitFont(font) {
  curFont = font;
  setFont(font);
  setFont('Ubuntu Mono');
  setFont(font);
}

function setcwd(cwd) {
  path = cwd;
}

function chdir(path) {
  term.send('cd '+path+lineEnd);
}

function clearTerm()
{
  term.send(clearCmd + lineEnd);
}

function exec(cmd)
{
  term.send('' + cmd + lineEnd);
}

function closeTerm() {
  alive = false;
  window.dispatchEvent(closeEvent);
  console.log("Closed via server");
  term.writeln("Pipe closed");
}

function consoleReady() {
  return term._initialized
}

function scrollTerm(delta) {
  var viewport = document.getElementById('.xterm-viewport');
  var curScrollPos = viewport.scrollTop();
  var maxHeight = viewport.prop('scrollHeight') - viewport.innerHeight();
  curScrollPos = Math.min(maxHeight, Math.max(0, curScrollPos - delta));
  document.getElementById('.xterm-viewport').animate({ scrollTop: curScrollPos }, 0);
}

function isAlive() {
   return alive;
}

function runRealTerminal() {
  term.loadAddon(new AttachAddon(socket));
  term._initialized = true;

  lineEnd = term.browser.isMSWindows ? '\r\n' : '\n';
  clearCmd = term.browser.isMSWindows ? 'cls' : 'clear';
  fitFont(curFont);
  let initialX = term.x;
  let timer = setInterval( () => {
    if(term.x != initialX) {
      fitFont(curFont);
      window.dispatchEvent(promptEvent);
      clearInterval(timer);
    }
  }, 200);
  fitFont(curFont);
}

document.ready( () => {
  createTerminal();
  new QWebChannel(qt.webChannelTransport, function (channel) {
      window.handler = channel.objects.handler;
      window.addEventListener('promptReady', function(e) {
          window.handler.ready();
      }, false);
      window.addEventListener('terminalClose', function(e) {
          window.handler.close();
      }, false);
  });
});
