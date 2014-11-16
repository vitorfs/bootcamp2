$(function () {

  var close_compose = function () {
    $(".compose").slideUp(300, function () {
      $(".compose textarea").val("");
    });
  };

  var open_compose = function () {
    $(".compose").slideDown(300, function () {
      $("#post").focus();
    });
  };

  $(".btn-compose").click(open_compose);
  $(".compose .btn-cancel").click(close_compose);

  $(".btn-post").click(function () {
    var post = $("#post").val();
    var csrf = $("[name='csrfmiddlewaretoken']").val();
    var last_feed = $(".stream li:first-child").attr("data-feed-id");
    if (last_feed === undefined) last_feed = "0";
    $.ajax({
      url: '/feed/post/',
      data: {
        'post': post,
        'last_feed': last_feed,
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
      beforeSend: function () {
        $("#compose-form textarea").prop("readonly", true);
        $("#compose-form .btn-post, #compose-form .btn-cancel").prop("disabled", true);
        $(".btn-post > span").hide();
        $(".btn-post .btn-state-posting").show();
      },
      success: function (data) {
        $(".stream").prepend(data);
        close_compose();
        hide_stream_update();
      },
      complete: function () {
        $("#compose-form textarea").prop("readonly", false);
        $("#compose-form .btn-post, #compose-form .btn-cancel").prop("disabled", false);
        $(".btn-post > span").hide();
        $(".btn-post .btn-state-post").show();
      }
    });
  });

  $("body").keydown(function (evt) {
    var keyCode = evt.which?evt.which:evt.keyCode;
    if ((evt.ctrlKey || evt.metaKey) && keyCode == 80) {
      $(".btn-compose").click();
      return false;
    }
  });

  $("#post").keydown(function (evt) {
    var keyCode = evt.which?evt.which:evt.keyCode;
    if ((evt.ctrlKey || evt.metaKey) && (keyCode == 10 || keyCode == 13)) {
      $(".btn-post").click();
    }
  });

});