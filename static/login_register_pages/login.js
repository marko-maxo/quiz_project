var url_check = document.getElementById("login_script").getAttribute("data-url-check");
var url_check_after = document.getElementById("login_script").getAttribute("data-url-check-after");
var url_redirect = document.getElementById("login_script").getAttribute("data-url-redirect");


$(document).on('submit', "#loginForm", function (e) {
    $("#login_btn").attr("disabled", true);
    e.preventDefault();
    $('.loader').css("display", "block");
    $("#response_message").css("display", "none");
    $("#response_message_success").css("display", "none");
    let data = {
        username: $('#username').val(),
        password: $('#password').val(),
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
            $("#response_message").css("display", "block");
            $("#login_btn").attr("disabled", false);
            $('.loader').css("display", "none");
        }
    }

})