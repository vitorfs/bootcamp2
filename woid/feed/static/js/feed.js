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
    //$("#compose-form textarea").prop("readonly", true);
    //$(".btn-post").prop("disabled", true);
    $(".btn-post .text").text("Posting…");
    $(".btn-post .fa").removeClass("fa-check").addClass("fa-spinner fa-spin");
  });

});