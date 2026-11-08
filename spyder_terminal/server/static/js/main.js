import { Terminal } from '@xterm/xterm';
import { AttachAddon } from '@xterm/addon-attach';
import { FitAddon } from '@xterm/addon-fit';
import { SearchAddon } from '@xterm/addon-search';
import { Unicode11Addon } from '@xterm/addon-unicode11';
import { WebLinksAddon } from '@xterm/addon-web-links';
import { WebglAddon } from '@xterm/addon-webgl';

let term;
let searchAddon;
let fitAddon;
let protocol;
let socketURL;
let socket;
let pid;
let curFont;
let curFontFamily;
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
      // Space between lines, so text is easier to read (Ubuntu Mono has
      // almost none of its own)
      lineHeight: 1.2,
      // Needed by the Unicode 11 addon
      allowProposedApi: true,
      windowsPty: isWindows ? {backend: 'conpty'} : undefined
      });

  // Use the character widths of modern terminals, which full screen
  // programs (e.g. TUIs with emoji or symbols) rely on to lay out text
  term.loadAddon(new Unicode11Addon());
  term.unicode.activeVersion = '11';

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
  });

  protocol = (location.protocol === 'https:') ? 'wss://' : 'ws://';
  socketURL = protocol + location.hostname + ((location.port) ? (':' + location.port) : '') + '/terminals/';

  term.open(terminalContainer);
  loadRenderer();
  fitAddon.fit();
  term.focus();

  window.term = term

  let cols = term.cols;
  let rows = term.rows;

  fontSize = term.options.fontSize;

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

function loadRenderer() {
  // The WebGL renderer draws each character in its cell, so it doesn't
  // depend on the widths of fallback fonts. Use the DOM renderer if it's
  // not available.
  try {
    const webgl = new WebglAddon();
    webgl.onContextLoss(() => {
      webgl.dispose();
      refit();
    });
    term.loadAddon(webgl);
  } catch (e) {
    console.log("WebGL renderer not available, using the DOM renderer");
  }
}

function refit() {
  if(fitAddon){
    fitAddon.fit();
  }
}

window.onresize = (event) => {
  refit();
}

function searchNext(regex, options) {
  if(searchAddon.findNext(regex, options)){
    return term.getSelectionPosition();
  }
  return -1;
}

function searchPrevious(regex, options) {
  if(searchAddon.findPrevious(regex, options)){
    return term.getSelectionPosition();
  }
  return -1;
}

function getFonts() {
  return term.options.fontFamily;
}

function setFont(font) {
  curFontFamily = "'" + font + "', monospace";
  term.options.fontFamily = curFontFamily;
  refit();
}

function fitFont(font) {
  curFont = font;
  setFont(font);

  // Measure the characters again once the font is loaded (e.g. the bundled
  // Ubuntu Mono web font), and fit the terminal to the new size
  if (document.fonts) {
    document.fonts.load("16px '" + font + "'").finally(() => {
      if (curFont === font) {
        term.options.fontFamily = 'monospace';
        setFont(font);
      }
    });
  }
}

function setcwd(cwd) {
  let path = cwd;
}

function getTerminalLines(){
  let text = '';
  let totalLines = term.buffer.active.length;
  for(let row = 0; row < totalLines; row++){
    text += term.buffer.active.getLine(row).translateToString(false);
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

function exec_delayed(cmd, text_trigger, delay){
  setTimeout(() => {
    if(searchNext(text_trigger) !== -1){
      exec(cmd);
    }
  }, delay)
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
  refit();
  return fontSize;
}

function decreaseFontSize(){
  fontSize -= 1;
  setOption('fontSize', fontSize);
  refit();
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
    // Name of the selection color since xterm.js 5
    option['selectionBackground'] = option['selection'];
    setBackground(option['background']);
  }
  term.options[option_name] = option
}

function setBackground(color) {
  // Paint the terminal's padding and the rest of the page like its content
  // (the viewport doesn't cover them since xterm.js 6)
  if (!color) {
    return;
  }
  document.body.style.backgroundColor = color;
  if (term.element) {
    term.element.style.backgroundColor = color;
  }
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

// Colors of the scrollbar, to match Spyder's (see style.css)
function setScrollbarColors(colors) {
  const style = document.documentElement.style;
  style.setProperty('--scrollbar-track', colors.track);
  style.setProperty('--scrollbar-border', colors.border);
  style.setProperty('--scrollbar-handle', colors.handle);
  style.setProperty('--scrollbar-handle-hover', colors.handleHover);
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
  exec_delayed: exec_delayed,
  closeTerm: closeTerm,
  consoleReady: consoleReady,
  scrollTerm: scrollTerm,
  isAlive: isAlive,
  getTerminalLines: getTerminalLines,
  searchNext: searchNext,
  searchPrevious: searchPrevious,
  setOption: setOption,
  setScrollbarColors: setScrollbarColors,
  refit: refit,
  increaseFontSize: increaseFontSize,
  decreaseFontSize: decreaseFontSize,
  addClassStyleToContainer: addClassStyleToContainer,
  hexToRGB: hexToRGB,
  pasteText: pasteText,
};

export default term_functions;
