$(document).ready(() => {
    $('#home-link').on('click', function(event) {
        event.preventDefault();
        window.location.href = '/profile';
    });

    $('#logout-link').on('click', function(event) {
        event.preventDefault();
        window.location.replace('/login.html');
    });

    $('#search-form').submit(function(event) {
        event.preventDefault();

        let project = $('#projectOption').val();
        let repo = $('#repoOption').val();
        let time = $('#timeOption').val();

        let redirectUrl = '/match?project=' + project + '&repo=' + repo + '&time=' + time;
        window.location.href = redirectUrl;
    });

    $('.prev').on('click', function(event) {
        event.preventDefault();
        window.location.href = '/previous-matches';
    });
});
