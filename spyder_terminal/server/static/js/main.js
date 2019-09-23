import { Terminal } from 'xterm';
import { AttachAddon } from 'xterm-addon-attach';
import { FitAddon } from 'xterm-addon-fit';
import { SearchAddon, ISearchOptions } from 'xterm-addon-search';
import { WebLinksAddon } from 'xterm-addon-web-links';
import { WebglAddon } from 'xterm-addon-webgl';

let term;
let searchAddon;
let fitAddon;
let protocol;
let socketURL;
let socket;
let pid;
let curFont;
let alive;

let myHeaders = new Headers();
myHeaders.append("Content-Type", "application/x-www-form-urlencoded");

const terminalContainer = document.getElementById('terminal-container');
const isWindows = ['Windows', 'Win16', 'Win32', 'WinCE'].indexOf(navigator.platform) >= 0;
const lineEnd = isWindows ? '\r\n' : '\n';
const clearCmd = isWindows ? 'cls' : 'clear';

const closeEvent = new Event('terminalClose');
const promptEvent = new Event('promptReady');


function createTerminal(){
  // Clean terminal
  while (terminalContainer.children.length) {
      terminalContainer.removeChild(terminalContainer.children[0]);
  }

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
  
  term.onResize((size) => {
      if (!pid) {
          return;
      }
      fitAddon.fit();
      const cols = size.cols;
      const rows = size.rows;
      const url = '/api/terminals/' + pid + '/size?cols=' + cols + '&rows=' + rows;

      fetch(url, {method: 'POST', headers: myHeaders});
  });

  protocol = (location.protocol === 'https:') ? 'wss://' : 'ws://';
  socketURL = protocol + location.hostname + ((location.port) ? (':' + location.port) : '') + '/terminals/';
  
  term.open(terminalContainer);
  fitAddon.fit();
  term.focus();

  window.term = term

  let cols = term.cols;
  let rows = term.rows;

  fetch('/api/terminals?cols=' + cols + '&rows=' + rows, {
    method: 'POST',
    headers: myHeaders,
    credentials: 'include'
  }).then((res) => {
    let charWidth = Math.ceil(term.element.offsetWidth / cols);
    let charHeight = Math.ceil(term.element.offsetHeight / rows);
    res.text().then((pidf) => {
      pid = pidf;
      fitAddon.fit();
      window.pid = pid;
      socketURL += pid;
      socket = new WebSocket(socketURL);
      socket.onopen = runRealTerminal;
      socket.onclose = closeTerm;
      socket.onerror = closeTerm;
    });
  });
}

window.onresize = (event) => {
  fitAddon.fit();
}

function getFonts() {
  return term.getOption('fontFamily');
}

function setFont(font) {
    let fonts = "monospace";
    fonts = "'"+font+"', "+fonts;
    term.setOption('fontFamily', fonts)
    fitAddon.fit();
}

function fitFont(font) {
  curFont = font;
  setFont(font);
  setFont('Ubuntu Mono');
  setFont(font);
}

function setcwd(cwd) {
  let path = cwd;
}

function getTerminalLines(){
  let text = '';
  for(let row = 0; row < term.rows; row++){
    let actLine = term.buffer.getLine(row);
    let length = actLine._line.length;
    text += actLine.translateToString(false, 0, length) + '';
  }
  return text;
}

function chdir(path) {
  socket.send('cd '+path + lineEnd);
}

function clearTerm(){
  socket.send(clearCmd + lineEnd);
}

function exec(cmd){
  socket.send('' + cmd + lineEnd);
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
  let viewport = document.getElementById('.xterm-viewport');
  let curScrollPos = viewport.scrollTop();
  let maxHeight = viewport.prop('scrollHeight') - viewport.innerHeight();
  curScrollPos = Math.min(maxHeight, Math.max(0, curScrollPos - delta));
  document.getElementById('.xterm-viewport').animate({ scrollTop: curScrollPos }, 0);
}

function isAlive() {
   return alive;
}

function runRealTerminal() {
  term.loadAddon(new AttachAddon(socket));
  term._initialized = true;
  curFont = 'Ubuntu Mono';
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
  alive = true;
}

function addDomListener(element, type, handler){
  element.addEventListener(type, handler);
  term._core.register({dispose: () => element.removeEventListener(type, handler)});
}

$(document).ready( () => {
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

const term_functions = {
  fitFont: fitFont,
  getFonts: getFonts,
  setFont: setFont,
  setcwd: setcwd,
  chdir: chdir,
  clearTerm: clearTerm,
  exec: exec,
  closeTerm: closeTerm,
  consoleReady: consoleReady,
  scrollTerm: scrollTerm,
  isAlive: isAlive,
  getTerminalLines: getTerminalLines,
  // setTerminalSize: setTerminalSize,
};

export default term_functions;