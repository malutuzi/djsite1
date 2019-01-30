$(document).ready(function(){

    $('ul.nav > li').removeClass('active');
    $('ul.nav > li:eq(4)').addClass('active');

    document.getElementById("pos1_90").style.display="none";
    // document.getElementById("pos1_365").style.display="none";
    document.getElementById("pos2_30").style.display="none";
    document.getElementById("pos3_30").style.display="none";
    document.getElementById("pos4_30").style.display="none";
    document.getElementById("pos5_30").style.display="none";

    $("#day1_30").click(function(){
        // alert('day15');
        document.getElementById("pos1_30").style.display="block";
        document.getElementById("pos1_90").style.display="none";
        // document.getElementById("pos1_365").style.display="none";
    });   

    $("#day1_90").click(function(){
        // alert('day15');
        document.getElementById("pos1_30").style.display="none";
        document.getElementById("pos1_90").style.display="block";
        // document.getElementById("pos1_365").style.display="none";
    });   

    // $("#day1_365").click(function(){
    //     // alert('day15');
    //     document.getElementById("pos1_30").style.display="none";
    //     document.getElementById("pos1_90").style.display="none";
    //     document.getElementById("pos1_365").style.display="block";
    // });   


    $("#day2_7").click(function(){
        // alert('day7');
        document.getElementById("pos2_7").style.display="block";
        document.getElementById("pos2_30").style.display="none";
    });
    
    $("#day2_30").click(function(){
        // alert('day15');
        document.getElementById("pos2_30").style.display="block";
        document.getElementById("pos2_7").style.display="none";
    });   

    $("#day3_7").click(function(){
        // alert('day7');
        document.getElementById("pos3_7").style.display="block";
        document.getElementById("pos3_30").style.display="none";
    });
    
    $("#day3_30").click(function(){
        // alert('day15');
        document.getElementById("pos3_30").style.display="block";
        document.getElementById("pos3_7").style.display="none";
    });   

    $("#day4_7").click(function(){
        // alert('day7');
        document.getElementById("pos4_7").style.display="block";
        document.getElementById("pos4_30").style.display="none";
    });
    
    $("#day4_30").click(function(){
        // alert('day15');
        document.getElementById("pos4_30").style.display="block";
        document.getElementById("pos4_7").style.display="none";
    });   

    $("#day5_7").click(function(){
        // alert('day7');
        document.getElementById("pos5_7").style.display="block";
        document.getElementById("pos5_30").style.display="none";
    });
    
    $("#day5_30").click(function(){
        // alert('day15');
        document.getElementById("pos5_30").style.display="block";
        document.getElementById("pos5_7").style.display="none";
    });   
    
});  //ready 的配对



