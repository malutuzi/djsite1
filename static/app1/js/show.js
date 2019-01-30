console.log('show.js is succesfully loaded')  //证明该js已经成功导入

// function showhis()
// {
// document.getElementById("history").style.display = "block";
// }

// function hidehis(){    
//     document.getElementById("history").style.display ="none";
// }

$(document).ready(function(){
    
    $("#alter").click(function(){
    $("#history").toggle();    //jquery里面，切换hide 和 show。
    });


    $("#refresh").click(function(){
        $("#realtime").load("rtsell/ #ajax1");  //realtime这个div，调用/show/rtsell 这个url对应的app1/rtsell.html 里面的id为ajax1的元素。
    
    });

  });