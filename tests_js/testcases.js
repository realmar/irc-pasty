// initial setup

// do not start automatically, we need first need to fetch the html
QUnit.config.autostart = false;

$.ajax({
  url: '../templates.html',
  dataType: 'html',
  success: function(html) {
      
    // find specific elements you want...
    var elem = $(html).find('body');
    $('#qunit-fixture').append(elem);

    QUnit.start();
  }
});

// tests

QUnit.test( "a basic test example", function(assert) {
    var value = "hello";
    assert.equal( value, "hello", "We expect value to be hello" );
});