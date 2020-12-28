
const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
$(document).ready(function () {
    $('form').on('submit', function (event) {
        event.preventDefault();
        
        var emailVal = $('#email').val();
        var title = document.title;
        if (re.test(emailVal)) {
            var data = {
                email: emailVal,
                password: $('#password').val(),
            };
            switch (title) {
                case "Flask Blog - Login": 
                    data['remember'] = $('#remember').val();
                    show_success("#email");
                    ajaxCall(data, "/V1/validate/account");
                    break;
                case "Flask Blog - Register":
                    show_success("#email");
                    if ($("#password").val() != $("#confirm_password").val()) {
                        throw_error("#confirm_password", "Field must be equal to password.");
                    } else {
                        data['username'] = $('#username').val();
                        ajaxCall(data, "/V1/register/account");
                    }
                    break;
            }
        } else {
            throw_error("#email", "Invalid email address.");
            if (title == "Flask Blog - Register") {
                if ($("#password").val() != $("#confirm_password").val()) {
                    throw_error("#confirm_password", "Field must be equal to password.");
                }
            }
        }

        function ajaxCall(data, url) {
            $.ajax({
                data: data,
                type: 'POST',
                url: url
            }).done(function (data) {
                if (data.response) {
                    window.location.href = data.redirect;
                } else if (data.error) {
                    throw_error("#email", data.error);
                }
            });
        }

        function show_success(id) {
            $(id).css('border-color', '#ced4da');
            $(id + "-error").hide();
            $(id).focus(function () {
                $(this).css({ "box-shadow": "0 0 0 0.25rem rgba(13, 110, 253, 0.25)" });
            }).blur(
                function () {
                    $(this).css({ "box-shadow": "none" });
                });
        }

        function throw_error(id, text) {
            $(id).css('border-color', '#dc3545');
            $(id + "-error").text(text).show();
            $(id).focus(function () {
                $(this).css({ "box-shadow": "0 0 0 0.25rem rgba(220, 53, 69, 0.25)" });
            }).blur(
                function () {
                    $(this).css({ "box-shadow": "none" });
                });
        }
    });
});