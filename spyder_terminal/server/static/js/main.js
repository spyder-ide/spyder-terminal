import { Terminal } from 'xterm';
import { AttachAddon } from 'xterm-addon-attach';
import { FitAddon } from 'xterm-addon-fit';
import { SearchAddon } from 'xterm-addon-search';
import { WebLinksAddon } from 'xterm-addon-web-links';

let term;
let searchAddon;
let fitAddon;
let protocol;
let socketURL;
let socket;
let pid;
let curFont;
let curTheme;
let alive;
let fontSize;

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
      const cols = size.cols;
      const rows = size.rows;
      const url = '/api/terminals/' + pid + '/size?cols=' + cols + '&rows=' + rows;

      fetch(url, {method: 'POST', headers: myHeaders});
      term.setOption('theme', curTheme);
      term.setOption('fontFamily', curFont);
  });

  protocol = (location.protocol === 'https:') ? 'wss://' : 'ws://';
  socketURL = protocol + location.hostname + ((location.port) ? (':' + location.port) : '') + '/terminals/';

  term.open(terminalContainer);
  fitAddon.fit();
  term.focus();

  window.term = term

  let cols = term.cols;
  let rows = term.rows;

  fontSize = term.getOption('fontSize');

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

function searchNext(regex) {
  if(searchAddon.findNext(regex)){
    return term.getSelectionPosition();
  }
  return -1;
}

function searchPrevious(regex) {
  if(searchAddon.findPrevious(regex)){
    return term.getSelectionPosition();
  }
  return -1;
}

function getFonts() {
  return term.getOption('fontFamily');
}

function setFont(font) {
    let fonts = "monospace";
    fonts = "'"+font+"', "+fonts;
    term.setOption('fontFamily', fonts);
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
    let actLine = term.buffer.active.getLine(row);
    let length = actLine._line.length;
    text += actLine.translateToString(false, 0, length) + '';
  }
  return text;
}

function chdir(path) {
  socket.send('cd '+ path + lineEnd);
}

function clearTerm(){
  socket.send(clearCmd + lineEnd);
}

function exec(cmd){
  socket.send('' + cmd + lineEnd);
}

function pasteText(cmd){
  socket.send('' + cmd);
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

function increaseFontSize(){
  fontSize += 1;
  setOption('fontSize', fontSize);
  fitAddon.fit();
  return fontSize;
}

function decreaseFontSize(){
  fontSize -= 1;
  setOption('fontSize', fontSize);
  fitAddon.fit();
  return fontSize;
}

function hexToRGB(hex) {
  let r = parseInt(hex.slice(1, 3), 16);
  let g = parseInt(hex.slice(3, 5), 16);
  let b = parseInt(hex.slice(5, 7), 16);
  return "rgba(" + r + ", " + g + ", " + b + ", " + 0.2 + ")";
}

function setOption(option_name, option) {
  if(option_name === 'theme'){
    curTheme = option;
    option['selection'] = hexToRGB(option['selection']);
  }
  term.setOption(option_name, option);
}

function runRealTerminal() {
  term.loadAddon(new AttachAddon(socket));
  term._initialized = true;
  curFont = 'Ubuntu Mono';
  fitFont(curFont);
  alive = true;
  let timer = setInterval( () => {
    if(term !== undefined) {
      fitFont(curFont);
      window.dispatchEvent(promptEvent);
      clearInterval(timer);
    }
  }, 200);
}

function addDomListener(element, type, handler){
  element.addEventListener(type, handler);
  term._core.register({dispose: () => element.removeEventListener(type, handler)});
}

function addClassStyleToContainer(className){
  document.getElementById('terminal-container').classList.add(className);
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
  searchNext: searchNext,
  searchPrevious: searchPrevious,
  setOption: setOption,
  increaseFontSize: increaseFontSize,
  decreaseFontSize: decreaseFontSize,
  addClassStyleToContainer: addClassStyleToContainer,
  hexToRGB: hexToRGB,
  pasteText: pasteText,
};

export default term_functions;