// initial setup

function loadTemplate(template, assert) {
  console.log(template);
  $.ajax({
  url: 'mock/templates/' + template,
  dataType: "html",
  async: false    // we want a blocking call, to prevent the tests being executed before the template is loaded
  })
  .done(function(html) {
    $('#qunit-fixture').append(html);
    assert.ok(true, 'Loaded Template');
  })
  .fail(function(jqXHR, text_status) {
    assert.ok(false, 'Failed to load template');
  });
}

// tests

//
// BEGIN tests for post.html
//

QUnit.module( "post.html", {
  before: function(assert) {
    loadTemplate('post.html', assert);
  }
});

QUnit.test("show progession bar", function(assert) {
  showProgression();
  assert.ok($("#progression-div").is(":visible"), "progression bar is visible");
});

//
// END post.html tests
//

//
// BEGIN tests for all.html
//

QUnit.module( "all.html", {
  before: function(assert) {
    loadTemplate('all.html', assert);
  }
});

//
// END all.html tests
//
