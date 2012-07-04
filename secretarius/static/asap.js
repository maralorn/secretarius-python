function reload() {
    $.getJSON("/asaplist/get/"+$NAME, function(data) {
        $.getTemplate("asaplist", function(tmpl) {
            $("#list").jqotesub(tmpl, data);
            reltimes()
            $.getJSON("/asaplist/get/names",function(data){
                for (var listindex in data.names){
                    $("select.asaplist").each(function () {$(this).append(new Option(data.names[listindex],data.names[listindex]))});
                }
            });
            $("#createasap").click(function() {
                $.post("/asap/create/",{ description : $("#description").val(), list: $NAME}, reload)
            });
            $("input:checkbox[name='done']").change(function (){
                $.get($SCRIPT_ROOT+"/task/done/"+$(this).val(), reload);
            });
            $("select").change(function (){
                $.post($SCRIPT_ROOT+"/asap/changelist/"+$(this).attr("id"), { list: $(this).val()}, function(data){
                    reload();
                });
            })
            $("#deletelist").click(function (){
                $.get($SCRIPT_ROOT+"/asaplist/delete/"+$NAME, function (data){window.location = "/"});
            })
        });
    });
}
$(document).ready(function() {
    reload();
});