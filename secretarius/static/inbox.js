function reload() {
    $.getJSON("/inbox/get/first/", function(data) {
        $.getTemplate("info", function(tmpl) {
            $("#info").jqotesub(tmpl, data);
            reltimes()
            $("#deleteinfo").click(function() {
                $.getJSON("/info/delete/" + data.id, reload);
            });
            $("#archiveinfo").click(function() {
                $.get("/info/archive/" + data.id, reload);
            });
            $("#maybeinfo").click(function() {
                $.get("/info/maybe/" + data.id, reload);
            });
            $("#changenote").click(function() {
                $.post("/note/change/" + data.id, {content: $("#notecontent").val() },reload);
            });
            $("#removeattachment").click(function() {
                $.get("/note/delete/attachment/" + data.id, reload);
            });
            $.getJSON("/asaplist/get/names",function(data){
                for (var listindex in data.names){
                    $("#asaplist").append(new Option(data.names[listindex],data.names[listindex]));
                }
            });
            $("#delayinfo").click(function() {
                $.post("/info/delay/"+data.id, { until: $("#date").val()}, reload);
            })
            $("#createasap").click(function() {
                $.post("/asap/create/",{ description : $("#description").val(), list: $("#asaplist").val(), referencing: data.id }, reload)
            });
            $("#createproject").click(function() {
                $.post("/project/create/", { description : $("#description").val(), referencing : data.id }, reload);
            });
            $("#createappointment").click(function() {
                $.post("/appointment/create/",{ description: $("#description").val(), date:$("#date").val(), time:$("#date").val(), referencing: data.id }, function(data) {
                    reload();
                });
            });
            $("#changenote").click(function() {
                $.post("/note/change/" + data.id, {
                    content : $("#notecontent").val() }, function(data) {
                    reload();
                });
            });
            $("#changenote").click(function() {
                $.post("/note/change/" + data.id, {
                    content : $("#notecontent").val() }, function(data) {
                    reload();
                });
            });
        });
    });
}
$(document).ready(function() {
    reload();
});