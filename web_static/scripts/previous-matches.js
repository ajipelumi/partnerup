$(document).ready(() => {
    $('#home-link').on('click', function(event) {
        event.preventDefault();
        window.location.href = '/profile';
    });

    $('#logout-link').on('click', function(event) {
        event.preventDefault();
        window.location.replace('/login');
    });
});