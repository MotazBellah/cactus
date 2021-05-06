$('#bmi-img').hide()
$("#weight").css("color", "green");


$('#weight').click(function(){

    $("#weight").css("color", "green");
    $("#bmi").css("color", "black");
    $( "#bmi-img" ).hide( "slow", function() {
        alert( "Animation complete." );
      });

    $('#weight-img').show(1000)

});


$('#bmi').click(function(){

    $("#bmi").css("color", "green");
    $("#weight").css("color", "black");
    $( "#weight-img" ).hide( "slow", function() {
        alert( "Animation complete." );
      });
    $('#bmi-img').show(1000)

});
