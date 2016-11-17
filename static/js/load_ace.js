var editor = undefined;

function initializeAce() {
  editor = ace.edit("input-area");
  editor.setTheme("ace/theme/chrome");
  editor.getSession().setMode("ace/mode/javascript");

  var syntax = $.cookie('syntax-checking');
  if(syntax == undefined || syntax == '0') {
    editor.getSession().setUseWorker(false);
  }else{
    editor.getSession().setUseWorker(true);
  }

}

initializeAce();
