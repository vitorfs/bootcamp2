$(function () {

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

});