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
            $(".stream-update").slideDown();
            $(document).attr("title", "(" + data + ") " + PAGE_TITLE);
          }
        },
        complete: function() {
          window.setTimeout(check_new_feed, REQUEST_INTERVAL);
        }
      });
    }
    else {
      window.setTimeout(check_new_feed, REQUEST_INTERVAL);
    }
  };
  check_new_feed();

  $.fn.toggleComments = function (callback) {
    callback = callback || function () {};
    var feed = $(this);
    if ($(feed).hasClass("tracking")) {
      $(feed).removeClass("tracking");
      $(".comments", feed).slideUp(300);
    }
    else {
      $(feed).addClass("tracking");
      var feed_id = $(feed).attr("data-feed-id");
      $.ajax({
        url: '/feed/comments/',
        data: {
          'feed_id': feed_id
        },
        cache: false,
        beforeSend: function () {
          $(".loading-comment", feed).css("display", "block");
        },
        success: function (data) {
          $(".comments ol", feed).html(data);
          $(".comment-count", feed).text($(".comments ol li", feed).not(".comment-help").length);
        },
        error: function () {

        },
        complete: function () {
          $(".loading-comment", feed).css("display", "none");
        }
      });
      $(".comments", feed).slideDown(300, callback);
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
    $(this).toggleDropdown();
    return false;
  });

  $(".stream").on("click", ".feed-like", function (evt) {
    evt.stopPropagation();
    var feed_id = $(this).closest("li.feed").attr("data-feed-id");
    var csrf = $("[name='csrfmiddlewaretoken']").val();
    var like_button = $(this);
    $.ajax({
      url: '/feed/like/',
      data: {
        'feed_id': feed_id,
        'csrfmiddlewaretoken': csrf
      },
      dataType: 'json',
      type: 'post',
      cache: false,
      success: function (data) {
        if ($(".text-like", like_button).is(":visible")) {
          $(".text-like", like_button).hide();
          $(".text-unlike", like_button).show();
        }
        else {
          $(".text-like", like_button).show();
          $(".text-unlike", like_button).hide();
        }
        $(".like-count", like_button).text(data.feed_likes);
      }
    });
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

  $(".stream").on("keydown", ".comments input[name='comment-description']", function (evt) {
    var keyCode = evt.which?evt.which:evt.keyCode;
    if (keyCode == 13) {
      var feed = $(this).closest(".feed");
      var comments = $(this).closest(".comments");
      var input = $(this);
      var comment = $(this).val();
      var feed_id = $(this).closest("li.feed").attr("data-feed-id");
      var csrf = $("[name='csrfmiddlewaretoken']").val();

      $.ajax({
        url: '/feed/comment/',
        data: {
          'feed_id': feed_id,
          'comment': comment,
          'csrfmiddlewaretoken': csrf,
        },
        type: 'post',
        cache: false,
        beforeSend: function () {
          $(input).val("");
        },
        success: function (data) {
          $("ol", comments).html(data);
          $(".comment-count", feed).text($(".comments ol li", feed).not(".comment-help").length);
        }
      });
      return false;
    }
  });

  function update_feeds () {
    var first_feed = $(".stream li:first-child").attr("data-feed-id");
    var last_feed = $(".stream li:last-child").attr("data-feed-id");

    if (first_feed != undefined && last_feed != undefined) {
      $.ajax({
        url: '/feed/update/',
        data: {
          'first_feed': first_feed,
          'last_feed': last_feed
        },
        cache: false,
        success: function (data) {
          $.each(data, function(id, feed) {
              var li = $("li[data-feed-id='" + id + "']");
              $(".like-count", li).text(feed.likes);
              $(".comment-count", li).text(feed.comments);
          });
        },
        complete: function () {
          window.setTimeout(update_feeds, REQUEST_INTERVAL);
        }
      });
    }
    else {
      window.setTimeout(update_feeds, REQUEST_INTERVAL);
    }
  };
  update_feeds();

  function track_comments () {
    $(".tracking").each(function () {
      var feed = $(this);
      var feed_id = $(this).closest("li").attr("data-feed-id");
      $.ajax({
        url: '/feed/track_comments/',
        data: {
          'feed_id': feed_id
        },
        cache: false,
        success: function (data) {
          $(".comments ol", feed).html(data);
          $(".comment-count", feed).text($(".comments ol li", feed).not(".comment-help").length);
        }
      });
    });
    window.setTimeout(track_comments, REQUEST_INTERVAL);
  };
  track_comments();

});