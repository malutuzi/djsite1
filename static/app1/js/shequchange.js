$(document).ready(function(){

    // $('ul.nav > li').removeClass('active');
    // $('ul.nav > li:eq(5)').addClass('active');

    document.getElementById("decrease100").style.display="block";
    document.getElementById("increase100").style.display="none";

    $("#decrease").click(function(){
        document.getElementById("decrease100").style.display="block";
        document.getElementById("increase100").style.display="none";
    });

    $("#increase").click(function(){
        document.getElementById("increase100").style.display="block";
        document.getElementById("decrease100").style.display="none";
    });

    
});