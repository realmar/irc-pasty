var editor = undefined;

function initializeAce() {
  editor = ace.edit("input-area");
  editor.setTheme("ace/theme/chrome");
  editor.getSession().setMode("ace/mode/javascript");
}

function adaptFeaturesAce() {
  var syntax = $.cookie('syntax-checking');
  if(syntax == undefined || syntax == '0') {
    editor.getSession().setUseWorker(false);
  }else{
    editor.getSession().setUseWorker(true);
  }

  var vimmode = $.cookie('vimmode');
  console.log(vimmode);
  if(vimmode == undefined || vimmode == '0') {
    editor.setKeyboardHandler();
  }else{
    editor.setKeyboardHandler("ace/keyboard/vim");
  }
}

initializeAce();
adaptFeaturesAce();
