$(function () {

  var page_title = $(document).attr("title");

  $(".btn-compose").click(function () {
    $(".compose").slideDown(400, function () {
      $(".compose textarea").focus();
    });
  });

  $(".compose .btn-cancel").click(function () {
    $(".compose").slideUp(400, function () {
      $(".compose textarea").val("");
    });
  });

  $(".btn-post").click(function () {
    $.ajax({
      url: '/feed/post/',
      data: $("#compose-form").serialize(),
      type: 'post',
      cache: false,
      beforeSend: function () {
        $("#compose-form textarea").prop("readonly", true);
        $("#compose-form .btn-post, #compose-form .btn-cancel").prop("disabled", true);
        $(".btn-post > span").hide();
        $(".btn-post .btn-state-posting").show();
      },
      success: function (data) {

      },
      complete: function () {
        $("#compose-form textarea").prop("readonly", false);
        $("#compose-form .btn-post, #compose-form .btn-cancel").prop("disabled", false);
        $(".btn-post > span").hide();
        $(".btn-post .btn-state-post").show();
      }
    });
  });

  $.fn.toggleComments = function (callback) {
    callback = callback || function () {};
    var feed = $(this);
    if ($(feed).hasClass("tracking")) {
      $(".comments", feed).slideUp(300, function () {
        $(feed).removeClass("tracking");
      })
    }
    else {
      $(".comments", feed).slideDown(300, function () {
        $(feed).addClass("tracking");
        callback();
      })
    }
  };

  $(".stream").on("click", ".post", function () {
    var feed = $(this).closest(".feed");
    $(feed).toggleComments();
  });

  $(".stream").on("click", ".post p a", function (evt) {
    evt.stopPropagation();
  });

  $(".stream").on("click", ".comment p a", function (evt) {
    evt.stopPropagation();
  });

  $(".stream").on("click", ".feed-settings", function (evt) {
    evt.stopPropagation();
    return false;    
  });

  $(".stream").on("click", ".feed-like", function (evt) {
    evt.stopPropagation();
    return false;
  });

  $(".stream").on("click", ".feed-comment", function (evt) {
    var feed = $(this).closest(".feed");
    $(feed).toggleComments(function () {
      $("[name='comment-description']", feed).focus();
    });
    evt.stopPropagation();
    return false;
  });

});