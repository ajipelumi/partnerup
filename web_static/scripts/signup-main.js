$(document).ready(() => {
    $('button').on('click', (event) => {
        event.preventDefault();

        const username = $('input[name="username"]').val();
        const email = $('input[name="email"]').val();
        const password = $('input[name="password"]').val();

        if (username.trim() === '' || email.trim() === '' || password.trim() === '') {
            toastr.error('Oops!, You forgot to enter your username, email and password!', {
                timeOut: 2000,
            });
          return;
        }

        let new_user = {
            "username": username,
            "email": email,
            "password": password
        };

        $.ajax({
            type: 'POST',
            url: 'http://34.207.127.10:5000/api/v1/users',
            contentType: 'application/json',
            data: JSON.stringify(new_user),
            success: (response) => {
                toastr.success('Hooray! You\'re in!', 'Success', {
                    timeOut: 2000,
                });
            }
        });
    });
});