$(function () {

  var check_notifications = function () {
    $.ajax({
      url: '/notifications/check/',
      cache: false,
      success: function (data) {
        if (data.notifications !== 0) {
          $("#notifications").addClass("new-notifications");
        }
        else {
          $("#notifications").removeClass("new-notifications");
        }
      },
      complete: function () {
        window.setTimeout(check_notifications, REQUEST_INTERVAL);
      }
    });
  };
  check_notifications();

});