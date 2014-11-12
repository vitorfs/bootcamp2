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
});