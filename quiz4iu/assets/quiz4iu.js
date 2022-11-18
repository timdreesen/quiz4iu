$(document).ready(function(){

var csrf = $("input[name=csrfmiddlewaretoken]").val();
var url = $(location).attr('href');
 
//stellt sicher, dass die Funktion nur auf der homepage ausgelöst wird
if (document.location.pathname == '/')
    //Zeit in ms in der getLobbies ausgeführt wird
    setInterval(getLobbies,5000);
    
//Lobbyliste auf homepage wird refreshed
function getLobbies(){
    $.ajax({

        type: 'POST',
        url: '/llv/', 
        data: {
            lobbies: 'LobbyList',
            csrfmiddlewaretoken: csrf
        },

        success: function(response) {
            //container id in welche die Antowrt geschrieben wird
            $("#ll").html(response)
        }
    })
    //check um in der js console (browser(f12)) zu gucken ob die funktion ausgeführt wird
    //console.log("getLobbies")
}
});



  /*function loadLobbies() {
    $("#button1").click(function(){
        // create an AJAX call
        $.ajax({

            url: ' ',
            type: 'get',
            data: {
                div_inhalt: $(" #lobbies").serialize()
            },
            
            // on success
            success: function (data) {
                $("#lobbies").text("<p>" + data + "</p>")
                //$("#lobbies").replaceWith(response)
                //$("#lobbies").html(response)
                console.log("loadLobbies success (js)")
                
            },
            // on error
            error: function (response) {
                console.log(response.responseJSON.errors)
                console.log("loadLobbies error")
            }
        });
    });
});


/* AJAX TUTORIAL

var csrf = $("input[name=csrfmiddlewaretoken]").val();

$("#button1").click(function(){
    $.ajax({
        url:'ajax_test',
        type:'get',
        data: {
            button_text: $(this).text()
        },
        success: function(response) {
            $("#button1").text(response.seconds)
            $("#seconds").append('<li>' + response.seconds + '</li>')
        }
    });
  });

$("#seconds").on('click','li',function() {
    $.ajax({
        url: 'ajax_test',
        type: 'post',
        data: {
            text: $(this).text(),
            csrfmiddlewaretoken: csrf
        },
        success: function(response) {
            $("#right").append('<li>' + response.data + '<li>')
        }
    })
});

*/

/* setInterval(reloadLobbies,5000);

function reloadLobbies()
{
    $('#aktiveLobbies').load(document.URL + ' #aktiveLobbies');
    console.log("Die Lobby wurde aktualisiert");
};


});


/* 
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
*/