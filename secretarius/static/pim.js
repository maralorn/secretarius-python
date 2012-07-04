function date(time) {
    return (new Date(time * 1000)).toRelativeTime();
}
function repeat(interval, func) {
    func();
    setTimeout(repeat, interval, interval, func);
}
function reltimes() {
    $("span.reltime").each(function (i) {$(this).html(date($(this).attr("time")))});
}

function loadlinks() {
    $.getJSON("/inbox/count", function(data){
        $.getTemplate("count", function(tmpl) {
            $("#count").jqotesub(tmpl, data);
        });
    });
    $.getJSON("/asaplist/get/names", function(data){
        $.getTemplate("asaplinks", function(tmpl) {
            $("#links").jqotesub(tmpl, data);
        });
    });
}

$(document).ready(function() {
    $('#innerheader').hide();
    $.extend({
        "templates" : {} });
    $.getTemplate = function(name, func) {
        if (name in $.templates) {
            func($.templates[name]);
        } else {
            $.get($SCRIPT_ROOT+"/static/" +name + ".html", function(tmplstr) {
                $.templates[name] = $.jqotec(tmplstr);
                func($.templates[name]);
            });
        }
    };

    $('#createnewlist').click(function (){
        $.get($SCRIPT_ROOT+'/asaplist/create/'+$('#newasaplist').val(), function (i){
            $('newasaplist').val('');
            loadlinks();
        });
    });
    repeat(1000, reltimes);
    loadlinks();
});