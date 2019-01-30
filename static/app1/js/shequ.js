$(document).ready(function(){

    $('ul.nav > li').removeClass('active');
    $('ul.nav > li:eq(1)').addClass('active');
    
    $("#alter1").click(function(){
        $("#pricetrend").toggle();    //jquery里面，切换hide 和 show。
        });

    document.getElementById("brokers").style.display="block";
    document.getElementById("houses").style.display="none";

    $("#s_brokers").click(function(){
        document.getElementById("brokers").style.display="block";
        document.getElementById("houses").style.display="none";
    });


    $("#s_houses").click(function(){
        document.getElementById("brokers").style.display="none";
        document.getElementById("houses").style.display="block";
    });


    // var inputname = $("#shequid").value
    // // var namelen = inputname.length
    // console.log(inputname)


    // $("#query").click(function(){
    //     // alert('day7');
    //     // var inputname = $("#shequid").value;
    //     var inputname = myform.shequname.value;
    //     // var namelen = inputname.length
    //     alert(inputname);
    //     console.log(inputname);
    // });

    // function checklen(){
    //     var inputname = myform.shequname.value;
    //     alert(inputname);
    //     if (inputname.length < 2){
    //         alert('请至少输入2个字！');
    //         return false;
    //     }
    //     else{
    //         return true;
    //     }

    // }
    
});