
$(document).ready(function () {
    $('select').on('change', function() {
        $('#link').attr("placeholder", "https://open.spotify.com/" + this.value);
    });
});