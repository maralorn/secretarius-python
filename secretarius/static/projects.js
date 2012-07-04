function toggle(id){
    if ($('#projecttoggle'+id).html() == '+'){
        $('#project'+id).hide(200);
        $('#projecttoggle'+id).html('-')
    } else{
        $('#project'+id).show(200);
        $('#projecttoggle'+id).html('+')
    }
}

function reload() {
    $.getJSON("/project/get/tree/", function(data) {
        $.getTemplate("projecttree", function(tmpl) {
            $("#projects").jqotesub(tmpl, data.root);
            $(".children").hide();
            $("input:checkbox[name='done']").change(function (){
                $.get($SCRIPT_ROOT+"/task/done/"+$(this).val(), function(data){
                    reload();
                });
            });
            function handleDropEvent( event, ui ) {
                    var draggable = ui.draggable;
                    if (draggable.hasClass("project")){
                        $.post("/project/set/parent/"+draggable.attr("id"), { parent: $(this).attr("id")}, reload);
                    }
                    if (draggable.hasClass("asap")){
                        $.post("/asap/set/project/"+draggable.attr("id"), { project: $(this).attr("id")}, reload);
                    }
                }
            function handleDropEvent2( event, ui ) {
                var draggable = ui.draggable;
                if (draggable.hasClass("project")){
                    $.post("/project/set/parent/"+draggable.attr("id"), { }, reload);
                }
                if (draggable.hasClass("asap")){
                    $.post("/asap/set/project/"+draggable.attr("id"), { }, reload);
                }
            }
            function handleDropEvent3( event, ui ) {
                var draggable = ui.draggable;
                $.get("/info/delete/"+draggable.attr("id"), reload);
            }
            $(".project").draggable({ revert: "invalid"});
            $(".asap").draggable({ revert: "invalid"});
            $(".project p").droppable( {drop: handleDropEvent} );
            $("#root").droppable( {drop: handleDropEvent2, activate: function(event, ui) {$(this).fadeTo(200,1);}, deactivate: function(event, ui) {$(this).fadeTo(200,0);}} );
            $("#garbage").droppable( {drop: handleDropEvent3, activate: function(event, ui) {$(this).fadeTo(200,1);}, deactivate: function(event, ui) {$(this).fadeTo(200,0);}} );
        });
    });
}

$(document).ready(function() {
    $("#createproject").click(function() {
        $.post("/project/create/", { description : $("#description").val() }, function() {$("#description").val(''); reload();});
    });
    $("#createasap").click(function() {
        $.post("/asap/create/",{ description : $("#description").val(), list: $("#asaplist").val() }, function() {$("#description").val(''); reload();})
    });
    $.getJSON("/asaplist/get/names",function(data){
        for (var listindex in data.names){
            $("#asaplist").append(new Option(data.names[listindex],data.names[listindex]));
        }
    });
    reload();
});