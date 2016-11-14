// initial setup

function loadTemplate(template) {
  $.ajax({
  url: 'mock/templates/' + template,
  dataType: 'html',
  success: function(html) {
    // find specific elements you want...
    var elem = $(html).find('body');
    $('#qunit-fixture').append(elem);
  }
  });
}

// tests

//
// BEGIN tests for post.html
//

QUnit.module( "post.html", {
  before: function() {
    loadTemplate('post.html');
  }
});

QUnit.test("show progession bar", function(assert) {
  var done = assert.async();
  showProgression();
  setTimeout(function() {
    assert.ok($("#progression-div").is(":visible"), "progression bar is visible");
    done();
  }, 1000 );
});

//
// END post.html tests
//

//
// BEGIN tests for all.html
//

QUnit.module( "all.html", {
  before: function() {
    loadTemplate('all.html');
  }
});

//
// END all.html tests
//
