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
  beforeEach: function(assert) {
    loadTemplate('post.html', assert);
    run();    // initalize events
  }
});

QUnit.test("show progession bar", function(assert) {
  showProgression();
  assert.ok($("#progression-div").is(":visible"), "progression bar is visible");
});

QUnit.test("hide progession bar", function(assert) {
  var done = assert.async();
  $("#progression-div").show();
  hideProgression();
  setTimeout(function() {
    assert.notOk($("#progression-div").is(":visible"), "progression bar is invisible");
    done();
  }, 500);
});

QUnit.test("show neutral msg", function(assert) {
  neutralMsgIn('test');
  assert.ok($("#neutral-msg-container").is(":visible"), "neutral msg is visible");
  assert.equal($("#neutral-msg-text-field").html(), "test", "neutral msg show correct text");
});

QUnit.test("hide neutral msg", function(assert) {
  var done = assert.async();
  $("#neutral-msg-container").show();
  neutralMsgOut();
  setTimeout(function() {
    assert.notOk($("#neutral-msg-container").is(":visible"), "neutral msg is invisible");
    done();
  }, 500);
});

function showHideMessage(name, func) {
  QUnit.test("show hide " + name + " msg", function(assert) {
    func('test');
    assert.ok($("#" + name + "-container").is(":visible"), name + " msg is visible");
    assert.equal($("#" + name + "-text-field").html(), 'test', name + " msg show correct text");
  
    var done = assert.async();
    setTimeout(function() {
      assert.notOk($("#" + name + "-container").is(":visible"), name + " msg is invisible");
      done();
    }, 2500);
  });
}

showHideMessage("error", showError);
showHideMessage("warning", showWarning);
showHideMessage("success", showSuccess);

QUnit.test("set link", function(assert) {
  var link = 'localhost';
  setLink(link);
  assert.equal($("#pasty-link").html(), link, "link text set correctly");
  assert.equal($("#pasty-link").attr("href"), link, "link href set correctly");
});

function checkDisplayPost(assert) {
  assert.notOk($("#edit-area").is(":visible"), "edit area is not visible");
  assert.ok($("#preview-area").is(":visible"), "preview area is visible");
  assert.equal($("#preview").html(), "Edit", "preview text is Edit");
  assert.ok($("#post-title").attr('readonly'), "post title is readonly");
}

function checkInversDisplayPost(assert) {
  assert.ok($("#edit-area").is(":visible"), "edit area is visible");
  assert.notOk($("#preview-area").is(":visible"), "preview area is not visible");
  assert.equal($("#preview").html(), "Preview", "preview text is Preview");
  assert.equal($("#post-title").attr('readonly'), undefined, "post title is not readonly");
}

QUnit.test("display Post", function(assert) {
  displayPost('test content');
  checkDisplayPost(assert);
});

//
// user interaction integration tests
//

QUnit.test("on preview clicked", function(assert) {
  // currently in edit mode
  $("#preview").trigger("click");
  checkDisplayPost(assert);
   
  // currently in preview mode
  $("#preview").trigger("click");
  checkInversDisplayPost(assert);
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
