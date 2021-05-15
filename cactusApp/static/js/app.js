// -----------------------Create csrftoken -------------------------//
// Generate csrftoken to use it in ajax call for django form
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

// Hide all error messages for form validation
$(".err_msg").text("");
$(".err_msg").css('visibility', 'hidden');
$(".err_msg").css('color', 'red');
$(".err_msg_re").css('color', 'red');

// When submit login form
$('#login').submit( event => {

    event.preventDefault();
    // Hid error message
    $(".err_msg").text("");
    $(".err_msg").css('visibility', 'hidden');
    // Get the username, password values
    const username = document.querySelector('#username').value;
    const password = document.querySelector('#password').value;
    // Validate the form
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

    // Display the spiner
    loading()
    // Send XHRHTTPrequest, to send the date from client to the server
        const url = '/login'
        const method = "POST"
        const data = JSON.stringify({
            username: username,
    		password: password
        })
        console.log(data);
        // var csrftoken = getCookie('csrftoken')

        const xhr = new XMLHttpRequest()
        const csrftoken = getCookie('csrftoken');
        xhr.responseType = 'json'
        xhr.open(method, url)
        xhr.setRequestHeader("Content-Type", "application/json")
        xhr.setRequestHeader('HTTP_X_REQUESTED_WITH', "XMLHttpRequest")
        xhr.setRequestHeader('X-Requested-With', "XMLHttpRequest")
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
        xhr.onload = function(response) {
            // Hide the spinner
            unloading()
            // If error occurs, display it to the user
            if ('message' in xhr.response) {
                $(".err_msg").text(xhr.response['message']);
                $(".err_msg").css('visibility', 'visible');
            } else {
                // success, rediret to the home page
                window.location = "/home";
            }
        }
        xhr.send(data)

});

// When submit the register form
$('#register').submit( event => {

    event.preventDefault();
    // Hide the error message
    $(".err_msg_re").text("");
    $(".err_msg_re").css('visibility', 'hidden');
    // Get the user data
    const username = document.querySelector('#register-name').value;
    const password = document.querySelector('#register-password').value;
    const password2 = document.querySelector('#register-password2').value;
    // Validate the form
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
          }
          else if ("error" in response) {
              console.log(response["error"]);
              window.location = "/";
          }
          else {
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
            unloading()
            console.log(response);
            $("#measurebtn").prop('value', 'Continue');
            $("#measurebtn").prop('disabled', false);

          if ('message' in response) {
              $(".err_msg_re").text(response['message']);
              $(".err_msg_re").css('visibility', 'visible');

          }
         else if ("error" in response) {
              console.log(response["error"]);
              window.location = "/";
          }
          else {
              window.location = "/charts/"+ kid_id;
          }

      },
       error: function (response) {
         console.log(response);
     }
      });

});




$('#bmi-img').hide()
$('#bmi-chart').hide()
$("#weight").css("color", "green");


function loading(){
	$(".loader").show();
}
function unloading(){
	$(".loader").hide();
}
