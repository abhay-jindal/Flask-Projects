
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

$('#picture').on('change', function (event) {
    const file = this.files[0]
    if (file) {
        if (['image/png', 'image/jpg', "image/jpeg", "image/gif"].includes(file.type)) {
            $("#picture-error").text("");
            $('#picture').removeClass("is-invalid");
            const reader = new FileReader();
            reader.onload = function () {
                $('.account-img').attr('src', this.result);
            }
            reader.readAsDataURL(file); // convert to base64 string
        } else {
            $("#picture-error").text("File does not have an approved extension: png, jpg, jpeg or gif.");
            $('#picture').addClass("is-invalid");
        }
    }

    $("#picture").change(function () {
        readURL(this);
    });

    if ($('.is-invalid').length == 0) {
        $(".btn").prop('disabled', false);
    } else {
        $(".btn").prop('disabled', true);
    }
});


$(document).ready(function () {

    $('.image-text').on('click', function (e) {
        $('#picture').click();
    });

    $('.close').on('click', function (e) {
        $('.alert').addClass('collapse');
    });

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
                    $(".alert").removeClass("collapse");
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