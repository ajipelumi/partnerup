$(document).ready(() => {
    $('#search-form').submit(function(event) {
        event.preventDefault();

        let project = $('#projectOption').val();
        let repo = $('#repoOption').val();
        let time = $('#timeOption').val();

        let redirectUrl = '/match?project=' + project + '&repo=' + repo + '&time=' + time;
        window.location.href = redirectUrl;
    });
});
