$(window).ready(run);

function run() {
  $("#preview").click(function() {
    if($(this).data("mode") == "edit") {
      $("#edit-area").hide();
      $("#preview-area").show();
      $("#preview-area").empty();
      $("#preview-area").append(markdown.toHTML($("#edit-area > textarea").val()));
      $(this).data("mode", "preview");
      $(this).html("Edit");
    }else{
      $(this).data("mode", "edit");
      $("#preview-area").hide();
      $("#edit-area").show();
      $(this).html("Preview");
    }
  });

  $("#save").click(function() {
    if($("#edit-area > textarea").val() == "") {
      return 0;
    }

    $.ajax({
      url: '/save/None',
      method: 'GET',
      dataType: 'text',
      data: {'input' : $("#edit-area > textarea").val()}
    })
    .done(function(response) {
    })
    .fail(function(jqXHR, text_status) {
    });
  });
}
