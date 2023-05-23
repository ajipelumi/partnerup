$(document).ready(() => {
    $('button').on('click', (event) => {
        event.preventDefault();

        const username = $('input[name="username"]').val();
        const email = $('input[name="email"]').val();
        const password = $('input[name="password"]').val();

        if (username.trim() === '' || password.trim() === '') {
            toastr.error('Oops!, You forgot to enter your username and password!', {
                timeOut: 2000,
            });
          return;
        }

        new_user = {
            "username": username,
            "email": email,
            "password": password
        };

        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5000/api/v1/users',
            contentType: 'application/json',
            data: JSON.stringify(new_user),
            success: (response) => {

            }
        });
    });
});