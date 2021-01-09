
function checkFileExtension() {
    fileName = $('#picture').val();
    extension = fileName.split('.').pop();
    if (['png', 'jpg', "jpeg", "gif"].includes(extension)) {
        $("#picture-error").text("");
        $(".account-img").attr("src", fileName);
        $('#picture').removeClass("is-invalid");
    } else {
        $("#picture-error").text("File does not have an approved extension: png, jpg, jpeg or gif.");
        $('#picture').addClass("is-invalid");
    }

    if ($('.is-invalid').length == 0) {
        $(".btn").prop('disabled', false);
    } else {
        $(".btn").prop('disabled', true);
    }
}

function checkEmailValidity() {
    email = $('#email').val();
    let re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if (re.test(email)) {
        $('#email').removeClass("is-invalid");
    } else {
        $('#email').addClass("is-invalid");
        $('#email-feedback').addClass("invalid-feedback").text('Invalid email address.');
    }
    if ($('.is-invalid').length == 0) {
        $(".btn").prop('disabled', false);
    } else {
        $(".btn").prop('disabled', true);
    }
}

$('.account-img').on('click', function (e) {
    $('#picture').click();
});

$(document).ready(function () {
    $('form').on('submit', function (event) {
        event.preventDefault();
        var email = $('#email').val();
        var data = new FormData(this);
        $("#nav-user, .account-heading").text($('#username').val());

        data.append("current_email", $(".text-secondary").text());
        ajaxCall(data, "/V1/update/account");
       
        function ajaxCall(ajaxData, url) {
            $.ajax({
                url: url,
                type: 'POST',
                data: ajaxData,
                contentType: false,
                processData: false,
            }).done(function (data) {
                if (data.response) { 
                    $(".text-secondary").text(email);
                    if (data.image) {
                        $(".account-img").attr("src", data.image);
                        $("#picture").val("");
                    }
                } else {
                    $('#email').addClass("is-invalid");
                    $('#email-feedback').addClass("invalid-feedback").text(data.error);
                    $(".btn").prop('disabled', true);
                }
            });
        }
    });
});