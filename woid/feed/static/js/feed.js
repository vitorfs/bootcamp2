$(function () {

  $(".btn-compose").click(function () {
    $(".compose").slideDown();
  });

  $(".compose .btn-cancel").click(function () {
    $(".compose").slideUp(400, function () {
      $(".compose textarea").val("");
    });
  });

});