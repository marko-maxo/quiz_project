var url_check = document.getElementById("register_script").getAttribute("data-url-check");
var url_check_after = document.getElementById("register_script").getAttribute("data-url-check-after");
var url_redirect = document.getElementById("register_script").getAttribute("data-url-redirect");

var password = $("#password");
var passwordConfirm = $("#passwordConfirm");
var passwordMatch = false;


password.keyup(function (e) {
    if (password.val() == passwordConfirm.val()) {
        passwordMatch = true;
        passwordConfirm.css('color', "#1cc88a");
    } else {
        passwordMatch = false;
        passwordConfirm.css('color', "#e74a3b");
    }
});
passwordConfirm.keyup(function (e) {
    if (password.val() == passwordConfirm.val()) {
        passwordMatch = true;
        passwordConfirm.css('color', "#1cc88a");
    } else {
        passwordMatch = false;
        passwordConfirm.css('color', "#e74a3b");
    }
});


$(document).on('submit', "#registerForm", function (e) {
    $("#username_bad_characters").css("display", "none");
    e.preventDefault();

    $("#email_in_use").css("visibility", "hidden");
    $("#username_in_use").css("visibility", "hidden");
    $("#password6").css("visibility", "hidden");
    $("#password_match").css("display", "none");
    $(".fields_to_disable").attr("disabled", true);

    function containsSpecialChars(str) {
        const specialChars = /[`!@#$%^&*()+\-=\[\]{};':"\\|,.<>\/?~]/;
        return specialChars.test(str);
    }


    if (passwordMatch) {
        $('.loader').css("display", "block");
        $("#register_btn").attr("disabled", true);

        let data = {
            username: $('#username').val(),
            password: $('#password').val(),
            email: $('#email').val(),
        }
        let login_request = new XMLHttpRequest();
        login_request.open("POST", url_check, true);
        login_request.withCredentials = true;
        login_request.send(JSON.stringify(data));
        login_request.onload = function () {
            let request_response = JSON.parse(login_request.responseText);
            if (this.status === 200) {
                $("input[type='text']").addClass("bg-success");
                $("input[type='password']").addClass("bg-success");
                $("#response_message_success").css("display", "block");
                setInterval(function () {
                    let login_check = new XMLHttpRequest();
                    login_check.open("GET", url_check_after, true);
                    login_check.withCredentials = true;
                    login_check.send(JSON.stringify(data));
                    login_check.onload = function () {
                        if (login_check.status === 200) {
                            window.location.replace(url_redirect)
                        }
                    }
                }, 500)
            } else {
                if (request_response["error"].hasOwnProperty("username")) {
                    $("#username_in_use").css("visibility", "visible");
                }
                if (request_response["error"].hasOwnProperty("email")) {
                    $("#email_in_use").css("visibility", "visible");
                }
                if (request_response["error"].hasOwnProperty("password")) {
                    $("#password6").css("visibility", "visible");
                }
                if (request_response["error"].hasOwnProperty("bad_characters")) {
                    $("#username_bad_characters").css("display", "block");
                }
                $("#register_btn").attr("disabled", false);
                $(".fields_to_disable").attr("disabled", false);
                $('.loader').css("display", "none");
            }
        }
    } else {
        $("#password_match").css("display", "block");
        $(".fields_to_disable").attr("disabled", false);
    }
})