$(window).ready(run);

function setLink(link) {
  $("#pasty-link").html(link);
  $("#pasty-link").attr("href", link);
}

function sendData(url, autosave) {
  if($("#input-area").val() == "" || $("#input-area").val() == undefined) {
    return 0; // IMPLEMENT: error handling
  }
  if($("#post-title").val() == "" || $("#input-title").val() == undefined) {
    return 0; // IMPLEMENT: error handling
  }
  var id = "None"
  if($("#post-id").data("post-id") != "") {
    id = $("#post-id").data("post-id");
  }
  $.ajax({
    url: url + id,
    method: 'POST',
    dataType: 'text',
    data: {'input' : $("#input-area").val(), 'title' : $("#post-title").val()}
  })
  .done(function(response) {
    if(autosave) {
      window.history.replaceState({}, "Pasty", window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/getautosave/' + response);
    }else{
      setLink(window.location.protocol + '//' + window.location.hostname + '/get/' + response);
      $("#pasty-link").parent('div').show();
    }
    $("#post-id").data("post-id", response);
  })
  .fail(function(jqXHR, text_status) {
    console.log(text_status);
  });
}

function run() {
  setInterval(function() {
    sendData('/autosave/', true)
  }, 1000 * 60); // every minute

  if($("#mode-control").data("initial-view-mode") == "show") {
    $("#edit-area").hide();
    var content = $("#preview-area").html()
    $("#preview-area").empty();
    $("#preview-area").append(markdown.toHTML(content));
    $("#preview-area").show();
    $("#preview").data("mode", "preview");
    $("#preview").html("Edit");
    $("#post-title").attr('readonly', 'true');
    setLink(window.location.href)
    $("#pasty-link").parent('div').show();

  }

  $("#preview").click(function() {
    if($(this).data("mode") == "edit") {
      $("#edit-area").hide();
      $("#preview-area").show();
      $("#preview-area").empty();
      $("#preview-area").append(markdown.toHTML($("#input-area").val()));
      $("#post-title").attr('readonly', 'true')
      $(this).data("mode", "preview");
      $(this).html("Edit");
    }else{
      $(this).data("mode", "edit");
      $("#preview-area").hide();
      $("#edit-area").show();
      if($("#mode-control").data("initial-view-mode") != "show") {
        $("#post-title").removeAttr('readonly');
      }
      $(this).html("Preview");

    }
  });

  $("#save").click(function() {
    sendData('/save/', false);
  });
}
