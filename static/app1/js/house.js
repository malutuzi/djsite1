$(document).ready(function(){

    $('ul.nav > li').removeClass('active');
    $('ul.nav > li:eq(2)').addClass('active');
    
    document.getElementById("intro").style.display="none";
    
    $("#alter").click(function(){
        $("#intro").toggle();    //jquery里面，切换hide 和 show。
        });
});