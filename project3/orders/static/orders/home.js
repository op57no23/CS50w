$(document).ready(function() {
  $(".list-group-item").click(function() {
    $("#" + $(".list-group-item.active").attr("data-table")).attr("style", "display: none");
    $(".list-group-item.active").removeClass("active");
    $(this).addClass("active");
    $("#" + $(this).attr("data-table")).attr("style", "display: inline");
  });
});
