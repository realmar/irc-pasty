var editor = undefined;

function initializeAce() {
  editor = ace.edit("input-area");
  editor.setTheme("ace/theme/chrome");
  editor.getSession().setMode("ace/mode/javascript");
}

function adaptFeaturesAce() {
  var syntax = Cookies.get('syntax-checking');
  if(syntax == undefined) {
    editor.getSession().setUseWorker(syntax == '1' ? true : false);
  }

  var vimmode = Cookies.get('vimmode');
  if(vimmode == undefined || vimmode == '0') {
    editor.setKeyboardHandler();
  }else{
    editor.setKeyboardHandler("ace/keyboard/vim");
  }

  var textwrap = Cookies.get('text-wrap');
  if(textwrap != undefined) {
    editor.getSession().setUseWrapMode(textwrap == '1' ? true : false);
  }
}

initializeAce();
adaptFeaturesAce();
