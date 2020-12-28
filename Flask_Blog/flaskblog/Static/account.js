const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

$(document).ready(function () {
    $('form').on('submit', function (event) {
        event.preventDefault();
        var email = $('#email').val();
        var username = $('#username').val();

        $("#nav-user").text(username);
        $(".account-heading").text(username);
        if (re.test(email)) {
            show_success('#email');
            var data = {
                email: email,
                username: username,
                current_email: $(".text-secondary").text()
            };
            ajaxCall(data, "/V1/update/account");
        } else {
            throw_error("#email", "Invalid email address.");
        }

        function ajaxCall(ajaxData, url) {
            $.ajax({
                data: ajaxData,
                type: 'POST',
                url: url
            }).done(function (data) {
                if (data.response) {  
                    $(".text-secondary").text(ajaxData.email);
                } else (data.error) {
                    throw_error("#email", data.error);
                }
            });
        }

        function show_success(id) {
            $(id).css('border-color', '#ced4da');
            $(id + "-error").hide();
            $(id).focus(function () {
                $(this).css({ "box-shadow": "0 0 0 0.25rem rgba(13, 110, 253, 0.25)" });
            }).blur(function () {
                $(this).css({ "box-shadow": "none" });
            });
        }

        function throw_error(id, text) {
            $(id).css('border-color', '#dc3545');
            $(id + "-error").text(text).show();
            $(id).focus(function () {
                $(this).css({ "box-shadow": "0 0 0 0.25rem rgba(220, 53, 69, 0.25)" });
            }).blur(function () {
                $(this).css({ "box-shadow": "none" });
            });
        }
    });
});