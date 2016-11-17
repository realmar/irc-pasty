var editor = undefined;
function initializeAce() {
  editor = ace.edit("input-area");
  editor.setTheme("ace/theme/chrome");
  editor.getSession().setMode("ace/mode/javascript");
}

initializeAce();
