var hide_stream_update = function () {
  $(".stream-update").hide();
  $(".stream-update .new-posts").text("");
  $(document).attr("title", PAGE_TITLE);
};

$(function () {

  var page = 2;
  var has_next = true;
  var is_loading = false;

  var get_first_feed = function () {
    var from_feed = 'None';
    if ($(".stream li").length > 0) {
      from_feed = $(".stream li:eq(0)").attr("data-feed-id");
    }
    return from_feed;
  };

  var load_feed = function () {
    if (has_next && !is_loading) {
      $.ajax({
        url: '/feed/load/',
        data: {
          'page': page,
          'from_feed': get_first_feed()
        },
        cache: false,
        beforeSend: function () {
          $(".stream-loading").show();
          is_loading = true;
        },
        success: function (data) {
          if (data.trim().length === 0) {
            has_next = false;
          }
          else {
            $(".stream").append(data);
            page = page + 1;
          }
        },
        error: function () {
          has_next = false;
        },
        complete: function () {
          $(".stream-loading").hide();
          is_loading = false;
        }
      });
    }
  };

  $(".stream-trigger").bind("enterviewport", load_feed).bullseye();

  $(".stream-update a").click(function () {
    var last_feed = $(".stream li:first-child").attr("data-feed-id");
    var csrf = $("[name='csrfmiddlewaretoken']").val();
    $.ajax({
      url: '/feed/load_new/',
      data: { 
        'last_feed': last_feed,
        'csrfmiddlewaretoken': csrf
      },
      cache: false,
      type: 'post',
      success: function (data) {
        $(".stream").prepend(data);
      },
      complete: function () {
        hide_stream_update();
      }
    });
    return false;
  });

  function check_new_feed () {
    var last_feed = $(".stream li:first-child").attr("data-feed-id");
    if (last_feed !== undefined) {
      $.ajax({
        url: '/feed/check/',
        data: {
          'last_feed': last_feed
        },
        cache: false,
        success: function (data) {
          if (parseInt(data) > 0) {
            $(".stream-update .new-posts").text(data);
            $(".stream-update").show();
            $(document).attr("title", "(" + data + ") " + PAGE_TITLE);
          }
        },
        complete: function() {
          window.setTimeout(check_new_feed, 3000);
        }
      });
    }
    else {
      window.setTimeout(check_new_feed, 3000);
    }
  };
  check_new_feed();

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