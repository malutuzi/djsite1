$(document).ready(function(){

    $('ul.nav > li').removeClass('active');
    $('ul.nav > li:first').addClass('active');

    // $("#detail").style.display="none";
    document.getElementById("detail").style.display="none";
    
    $("#alter").click(function(){
        $("#detail").toggle();    //jquery里面，切换hide 和 show。
        });


});