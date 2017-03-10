$(() => {

  function updateThread(msg, isServer) {
    let threadHTML = $("#thread").html();
    let response;
    if (isServer) {
      response = "Server: " + msg;
    }
    else {
      response = "You: " + msg;
    }
    let formattedResponse = $("<p></p>").text(response);

    $("#thread").append(formattedResponse);
  }
  
  var socket = io();
  
  socket.on("connect", function() {
    console.log("Connected to socket!");
  });

  socket.on("message", function(msg) {
    updateThread(msg, true);
    if (msg === "Would you like to play again?") {
      let threadHTML = $("#thread").html();
      let buttons = "<button class='yes'>Yes</button><button class='no'>No</button>";
      threadHTML += "<p>" + buttons + "</p>";
      $("#thread").html(threadHTML);

      $(".yes").click(function() {
        $("#thread").html(""); // clear thread first
        socket.emit("restart");
      });

      $(".no").click(function() {
        updateThread("Stopping the game...", true);
        updateThread("Disconnected.", true);
        socket.disconnect();
      });
    }
  });

  $("#send").click(function() {
    var guessAttempt = $("#guess").val();
    updateThread(guessAttempt, false);
    socket.send(guessAttempt);
  });
});
