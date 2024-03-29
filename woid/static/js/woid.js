var OPERATING_SYSTEM = "Unknown OS";
if (navigator.appVersion.indexOf("Win")!=-1) OPERATING_SYSTEM="Windows";
if (navigator.appVersion.indexOf("Mac")!=-1) OPERATING_SYSTEM="MacOS";
if (navigator.appVersion.indexOf("X11")!=-1) OPERATING_SYSTEM="UNIX";
if (navigator.appVersion.indexOf("Linux")!=-1) OPERATING_SYSTEM="Linux";

var PAGE_TITLE = $(document).attr("title");

var REQUEST_INTERVAL = 30000;

$.fn.toggleDropdown = function () {
  if ($(".dropdown-menu", this).is(":visible")) {
    $(".dropdown-menu", this).fadeOut(200);
  }
  else {
    $(".dropdown-menu").hide();
    $(".dropdown-menu", this).fadeIn(200);
  }
};

$(function () {
  $(".help-text").click(function () {
    $(this).toggleDropdown();
  });
});