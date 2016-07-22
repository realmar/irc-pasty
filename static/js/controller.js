$(window).ready(run);

function run() {
  if($("#mode-control").data("initial-view-mode") == "show") {
    $("#edit-area").hide();
    $("#preview-area").show();
    $("#preview").data("mode", "preview");
    $("#preview").html("Edit");
    $("#post-title").attr('readonly', 'true');

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
      $("#post-title").removeAttr('readonly');
      $(this).html("Preview");

    }
  });

  $("#save").click(function() {
    if($("#input-areaa").val() == "") {
      return 0; // IMPLEMENT: error handling
    }
    if($("#post-title").val() == "") {
      return 0; // IMPLEMENT: error handling
    }

    $.ajax({
      url: '/save/None',
      method: 'POST',
      dataType: 'text',
      data: {'input' : $("#input-area").val(), 'title' : $("#post-title").val()}
    })
    .done(function(response) {
      $("#pasty-link").html(window.location.protocol + '//' + window.location.hostname + '/get/' + response);
      $("#pasty-link").parent('div').show();
    })
    .fail(function(jqXHR, text_status) {
      console.log(text_status);
    });
  });
}
