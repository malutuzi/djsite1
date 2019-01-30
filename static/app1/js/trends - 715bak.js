$(document).ready(function(){

    $('ul.nav > li').removeClass('active');
    $('ul.nav > li:eq(1)').addClass('active');

    document.getElementById("pos1_7").style.display="none";
    document.getElementById("pos2_7").style.display="none";


    $("#day1_7").click(function(){
        // alert('day7');
        document.getElementById("pos1_7").style.display="block";
        document.getElementById("pos1_15").style.display="none";
    });
    
    $("#day1_15").click(function(){
        // alert('day15');
        document.getElementById("pos1_15").style.display="block";
        document.getElementById("pos1_7").style.display="none";
    });   

    $("#day2_7").click(function(){
        // alert('day7');
        document.getElementById("pos2_7").style.display="block";
        document.getElementById("pos2_15").style.display="none";
    });
    
    $("#day2_15").click(function(){
        // alert('day15');
        document.getElementById("pos2_15").style.display="block";
        document.getElementById("pos2_7").style.display="none";
    });   
    
});  //ready 的配对



