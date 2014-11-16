var OPERATING_SYSTEM = "Unknown OS";
if (navigator.appVersion.indexOf("Win")!=-1) OPERATING_SYSTEM="Windows";
if (navigator.appVersion.indexOf("Mac")!=-1) OPERATING_SYSTEM="MacOS";
if (navigator.appVersion.indexOf("X11")!=-1) OPERATING_SYSTEM="UNIX";
if (navigator.appVersion.indexOf("Linux")!=-1) OPERATING_SYSTEM="Linux";

var PAGE_TITLE = $(document).attr("title");