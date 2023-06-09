$(document).ready(() => {
    $('#home-link').on('click', function(event) {
        event.preventDefault();
        window.location.href = '/profile';
    });

    $('#logout-link').on('click', function(event) {
        event.preventDefault();
        window.location.replace('/index.html');
    });

    $('.prev').on('click', function(event) {
        event.preventDefault();
        window.location.href = '/previous-matches';
    });
});