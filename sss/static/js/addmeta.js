$(document).ready(function() {
    json = $.parseJSON($("#filelist").val());
    filetable = $("#filetable");
    $.each(json, function(index, file) {
      filetable.append("<tr><td>" + file + "</tr></tr>");
    });
});
