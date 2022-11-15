$(document).ready(function(){

console.log("test");
console.log(document.head);

$("#button1").click(function(){
    $("#modus").text("Modus: Quiz-Duell");
  });

$("#button2").click(function(){
    $("#modus").text("Modus: Team-Quiz");
  });

$("#1").click(function(){
    $("#kurs").text("Kurs: " + $("#1").text());
  });

$("#2").click(function(){
    $("#kurs").text("Kurs: " + $("#2").text());
});

$("#3").click(function(){
    $("#kurs").text("Kurs: " + $("#3").text());
});

$("#4").click(function(){
    $("#kurs").text("Kurs: " + $("#4").text());
});

$("#5").click(function(){
    $("#kurs").text("Kurs: " + $("#5").text());
});

$("#6").click(function(){
    $("#kurs").text("Kurs: " + $("#6").text());
});

$("#7").click(function(){
    $("#kurs").text("Kurs: " + $("#7").text());
});

$("#8").click(function(){
    $("#kurs").text("Kurs: " + $("#8").text());
});

$("#9").click(function(){
    $("#kurs").text("Kurs: " + $("#9").text());
});

$("#10").click(function(){
    $("#kurs").text("Kurs: " + $("#10").text());
});
  

});