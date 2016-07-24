var display_modes = [
  'Markdown',
  'Plain Code',
  'Plain Text'
];

$(window).ready(run);

function neutralMsgIn(message) {
  $("#neutral-msg-text-field").html(message);
  $("#neutral-msg-container").fadeIn('fast')
}

function neutralMsgOut() {
  $("#neutral-msg-container").fadeOut('fast')
}

function showError(message) {
  $("#error-text-field").html(message);
  $("#error-container").fadeIn('fast').delay(2000).fadeOut('fast');
}

function showSuccess(message) {
  $("#success-text-field").html(message);
  $("#success-container").fadeIn('fast').delay(2000).fadeOut('fast');
}

function highlight() {
  $('pre code').each(function(i, block) {
    hljs.highlightBlock(block);
  });
}

function setLink(link) {
  $("#pasty-link").html(link);
  $("#pasty-link").attr("href", link);
}

function sendData(url, autosave) {
  if($("#input-area").length == 0) {
    return 0;
  }

  if($("#input-area").val() == "") {
    if(!autosave) {
      showError("Enter some content to the post");
    }
    return 0;
  }
  if($("#post-title").val() == "") {
    if(!autosave) {
      showError("Specify a title");
    }
    return 0;
  }
  var id = ""
  if($("#post-id").data("post-id") != "") {
    id = $("#post-id").data("post-id");
  }
  neutralMsgIn('Loading ...')
  $.ajax({
    url: url + id,
    method: 'POST',
    dataType: 'text',
    data: {
      'content' : $("#input-area").val(),
      'title' : $("#post-title").val(),
      'display_mode' : $("#display-mode").data("display-mode")
    }
  })
  .done(function(response) {
    if(autosave) {
      window.history.replaceState({}, "Pasty", window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/getautosave/' + response);
    }else{
      setLink(window.location.protocol + '//' + window.location.hostname + '/get/' + response);
      $("#link-container").show();
    }
    $("#post-id").data("post-id", response);
    neutralMsgOut()
    if(!autosave) {
      showSuccess('Post saved!');
    }else{
      showSuccess('Autosaved!');
    }
  })
  .fail(function(jqXHR, text_status) {
    neutralMsgOut()
    showError("There was a communication problem with the server");
  });
}

function generateHTML(content) {
  if($("#display-mode").data("display-mode") == 0) {
    var converter = new showdown.Converter();
    return converter.makeHtml(content);
  }else if($("#display-mode").data("display-mode") == 1) {
    return '<pre><code>' + content + '</code></pre>';
  }else if($("#display-mode").data("display-mode") == 2) {
    return content;
  }
}

function displayPost(content) {
  $("#edit-area").hide();
  $("#preview-area").empty();
  $("#preview-area").append(generateHTML(content));
  highlight();
  $("#preview-area").show();
  $("#preview").data("mode", "preview");
  $("#preview").html("Edit");
  $("#post-title").attr('readonly', 'true');
}

function run() {
  setInterval(function() {
    sendData('/autosave/', true)
  }, 1000 * 60); // every minute

  if($("#mode-control").data("initial-view-mode") == "show") {
    displayPost($("#input-area").html());
    setLink(window.location.href);
    $("#link-container").show();
  }

  $("#display-mode-text").html(display_modes[parseInt($("#display-mode").data("display-mode"))]);

  $("#preview").click(function() {
    if($(this).data("mode") == "edit") {
      displayPost($("#input-area").val());
      $(this).data("mode", "preview");
      $(this).html("Edit");
    }else{
      $(this).data("mode", "edit");
      $("#preview-area").hide();
      $("#edit-area").show();
      $("#post-title").removeAttr('readonly');
      $(this).html("Preview");

    }
  });

  $("#save").click(function() {
    sendData('/save/', false);
  });

  $("#display-mode-selector > li > a").click(function () {
    $("#display-mode-text").html($(this).html());
    $("#display-mode").data("display-mode", $(this).data("display-mode"));
    if($("#preview").data("mode") == "preview") {
      displayPost($("#input-area").val());
    }
  });
}
