$(function () {

    $('.connectedSortable').each(function(){
        $('<input name="meals_order" id="m'+$(this).attr('id')+'" value="">').appendTo('#sortlistcontainer')
        $(this).sortable({
            connectWith: ".connectedSortable",
            axis: 'y',
            handle: '.sorthandle',
            create: function( event, ui ) {
                // alert($(this).attr('id'))
                $('#m'+$(this).attr('id')).val($('#'+$(this).attr('id')).sortable('toArray'))
            },
            update: function( event, ui ) {
                $('#m'+$(this).attr('id')).val($('#'+$(this).attr('id')).sortable('toArray'))
            },
        }).disableSelection();
    })

});

function counting() {
    var today = new Date();
    var day = today.getDate();
    var month = today.getMonth() + 1;
    var year = today.getFullYear();
    var hour = today.getHours();
    if (hour < 10) hour = "0" + hour;
    var minute = today.getMinutes();
    if (minute < 10) minute = "0" + minute;
    var second = today.getSeconds();
    if (second < 10) second = "0" + second;
    document.getElementById("clock").innerHTML = day + "/" + month + "/" + year + " | " + hour + ":" + minute + ":" + second;
    setTimeout("counting()", 1000);
}
