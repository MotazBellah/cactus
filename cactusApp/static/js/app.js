$('#bmi-img').hide()
$("#weight").css("color", "green");


function loading(){
	$(".loader").show();
}
function unloading(){
	$(".loader").hide();
}

$('#weight').click(function(){

    $("#weight").css("color", "green");
    $("#bmi").css("color", "black");

    $('#bmi-img').hide(1000)
    $('#weight-img').show(1000)

});


$('#bmi').click(function(){

    $("#bmi").css("color", "green");
    $("#weight").css("color", "black");

    $('#weight-img').hide(1000)
    $('#bmi-img').show(1000)

});
