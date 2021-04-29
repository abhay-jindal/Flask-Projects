
function checkEmailValidity() {
    email = $('#email').val();
    let re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if (re.test(email)) {
        $('#email').removeClass("is-invalid");
    } else {
        $('#email').addClass("is-invalid");
        $('#email-feedback').addClass("invalid-feedback").text('Enter a valid email address.');
    }

    if ($('.is-invalid').length == 0) {
        $(".btn").prop('disabled', false);
    } else {
        $(".btn").prop('disabled', true);
    }
}

function checkConfirmPassword() {
    if ($("#password").val() != $("#confirm_password").val()) {
        $('#confirm_password').addClass("is-invalid");
        $('#password-feedback').addClass("invalid-feedback").text('The passwords you entered do not match.');
    } else {
        $('#confirm_password').removeClass("is-invalid");
    }

    if ($('.is-invalid').length == 0) {
        $(".btn").prop('disabled', false);
    } else {
        $(".btn").prop('disabled', true);
    }
    
}

$(document).ready(function () {

    $('.close').on('click', function (e) {
        $('.alert').addClass('collapse');
    });

    $('form').on('submit', function (event) {
        event.preventDefault();
        
        var title = document.title;
        var data = new FormData(this);
        switch (title) {
            case "BlogChef - Login":  
                ajaxCall(data, "/V1/validate/account");
                break;
            case "BlogChef - Register":     
                ajaxCall(data, "/V1/register/account"); 
                break;
            }

        function ajaxCall(data, url) {
            $.ajax({
                data: data,
                type: 'POST',
                url: url,
                processData: false,
                contentType: false
            }).done(function (data) {
                if (data.response) {
                    window.location.href = data.redirect;
                } else if (data.error) {
                    $('#email').addClass("is-invalid");
                    $('#email-feedback').addClass("invalid-feedback").text(data.error);
                    $(".btn").prop('disabled', true);
                } else {
                    $(".alert").removeClass("collapse");
                }
            });
        }
    });
});