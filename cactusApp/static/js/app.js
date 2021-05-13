// -----------------------Create csrftoken -------------------------//
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



$(".err_msg").text("");
$(".err_msg").css('visibility', 'hidden');
$(".err_msg").css('color', 'red');
$(".err_msg_re").css('color', 'red');


$('#login').submit( event => {

    event.preventDefault();

    $(".err_msg").text("");
    $(".err_msg").css('visibility', 'hidden');

    const username = document.querySelector('#username').value;
    const password = document.querySelector('#password').value;

    if(username == ""){
		$(".err_msg").text("Please enter the username");
    	$(".err_msg").css('visibility', 'visible');
    	return false;
	}

    if(password == ""){
		$(".err_msg").text("Please enter the password");
    	$(".err_msg").css('visibility', 'visible');

    	return false;
	}

    var data ={
		username: username,
		password: password
	}
    console.log(data);
    loading()

    $.ajax({
        type: 'post',
        url: '/login',
        data: JSON.stringify(data),
        headers: {
          'Content-Type':'application/json',
          'HTTP_X_REQUESTED_WITH':'XMLHttpRequest',
          'X-Requested-With':'XMLHttpRequest',
          'X-CSRFToken':getCookie('csrftoken'),
      },
        success: function (response) {
            unloading()
          console.log(response['message']);

          if ('message' in response) {
              $(".err_msg").text(response['message']);
              $(".err_msg").css('visibility', 'visible');
          } else {
              window.location = "/home";
          }

      },
       error: function (response) {
         console.log(response);
     }
      });

});


$('#register').submit( event => {

    event.preventDefault();

    $(".err_msg_re").text("");
    $(".err_msg_re").css('visibility', 'hidden');

    const username = document.querySelector('#register-name').value;
    const password = document.querySelector('#register-password').value;
    const password2 = document.querySelector('#register-password2').value;

    if(username == ""){
		$(".err_msg_re").text("Please enter the username");
    	$(".err_msg_re").css('visibility', 'visible');
    	return false;
	}

    if(password == "" || password2 == ""){
		$(".err_msg_re").text("Please enter the password");
    	$(".err_msg_re").css('visibility', 'visible');

    	return false;
	}

    if(password !== password2 ){
		$(".err_msg_re").text("password must match");
    	$(".err_msg_re").css('visibility', 'visible');

    	return false;
	}

    var data ={
		username: username,
		password: password,
        password2: password2,
	}
    console.log(data);
    loading()

    $.ajax({
        type: 'post',
        url: '/register',
        data: JSON.stringify(data),
        headers: {
          'Content-Type':'application/json',
          'HTTP_X_REQUESTED_WITH':'XMLHttpRequest',
          'X-Requested-With':'XMLHttpRequest',
          'X-CSRFToken':getCookie('csrftoken'),
      },
        success: function (response) {
            unloading()
          console.log(response['message']);

          if ('message' in response) {
              $(".err_msg_re").text(response['message']);
              $(".err_msg_re").css('visibility', 'visible');
          } else {
              window.location = "/home";
          }

      },
       error: function (response) {
         console.log(response);
     }
      });

});


$('#childForm').submit( event => {

    event.preventDefault();

    $(".err_msg_re").text("");
    $(".err_msg_re").css('visibility', 'hidden');

    const childname = document.querySelector('#childname').value;
    const childdate = document.querySelector('#childdate').value;
    const gender = $("#childgender :selected").val();

    if(childname == ""){
        $(".err_msg_re").text("Please enter the child name");
        $(".err_msg_re").css('visibility', 'visible');
        return false;
    }

    if(childdate == ''){
        $(".err_msg_re").text("Please enter the child birthday");
        $(".err_msg_re").css('visibility', 'visible');

        return false;
    }

    if(gender == 'Choose Gender...' ){
        $(".err_msg_re").text("Please enter the child gender");
        $(".err_msg_re").css('visibility', 'visible');

        return false;
    }

    var data ={
        childname: childname,
        childdate: childdate,
        childgender: gender,
    }
    console.log(data);
    loading()

    $.ajax({
        type: 'post',
        url: '/home',
        data: JSON.stringify(data),
        headers: {
          'Content-Type':'application/json',
          'HTTP_X_REQUESTED_WITH':'XMLHttpRequest',
          'X-Requested-With':'XMLHttpRequest',
          'X-CSRFToken':getCookie('csrftoken'),
      },
        success: function (response) {
            unloading()

          if ('message' in response) {
              $(".err_msg_re").text(response['message']);
              $(".err_msg_re").css('visibility', 'visible');
          } else {
              window.location = "/kids";
          }

      },
       error: function (response) {
         console.log(response);
     }
      });

});


$('#measureForm').submit( event => {

    event.preventDefault();

    $(".err_msg_re").text("");
    $(".err_msg_re").css('visibility', 'hidden');

    const weight = document.querySelector('#weight').value;
    const height = document.querySelector('#height').value;
    const head = document.querySelector('#head').value;
    const measuredate = document.querySelector('#measuredate').value;


    if(weight == ""){
        $(".err_msg_re").text("Please enter the child weight");
        $(".err_msg_re").css('visibility', 'visible');
        return false;
    }

    if(height == ''){
        $(".err_msg_re").text("Please enter the child height");
        $(".err_msg_re").css('visibility', 'visible');

        return false;
    }

    if(measuredate == '' ){
        $(".err_msg_re").text("Please enter the measuer date");
        $(".err_msg_re").css('visibility', 'visible');

        return false;
    }
    $("#measurebtn").prop('value', 'Processing...');
    $("#measurebtn").prop('disabled', true);
    var data ={
        weight: weight,
        height: height,
        head: head,
        measuredate: measuredate,
        kid_id: kid_id,
    }
    console.log(data);
    loading()

    $.ajax({
        type: 'post',
        url: '/measurement',
        data: JSON.stringify(data),
        headers: {
          'Content-Type':'application/json',
          'HTTP_X_REQUESTED_WITH':'XMLHttpRequest',
          'X-Requested-With':'XMLHttpRequest',
          'X-CSRFToken':getCookie('csrftoken'),
      },
        success: function (response) {
            // unloading()
            console.log(response);
            $("#measurebtn").prop('value', 'Continue');
            $("#measurebtn").prop('disabled', false);

          if ('message' in response) {
              $(".err_msg_re").text(response['message']);
              $(".err_msg_re").css('visibility', 'visible');
          } else {
              window.location = "/charts/"+ kid_id;
          }

      },
       error: function (response) {
         console.log(response);
     }
      });

});




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
