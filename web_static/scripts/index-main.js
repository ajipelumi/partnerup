$(document).ready(() => {
    $('button').on('click', (event) => {
        event.preventDefault();

        let username = $('input[name="username"]').val();
        username = username.replace('@', '');
	const password = $('input[name="password"]').val();

        if (username.trim() === '' || password.trim() === '') {
            toastr.error('Oops!, You forgot to enter your username and password!', {
                timeOut: 2000,
            });
          return;
        }

        let user = {
            "username": username,
            "password": password
        };

        $.ajax({
            type: 'POST',
            url: 'http://34.207.127.10/api/v1/users',
            contentType: 'application/json',
            data: JSON.stringify(user),
            success: (response) => {
                toastr.success('Hooray! You\'re in!', 'Success', {
                    timeOut: 2000,
                });
                window.location.replace('/profile');
            },
            error: (xhr) => {
                let errorMessage = 'Oops! An error occurred while processing your request.';
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    errorMessage = xhr.responseJSON.message;
                }
                toastr.error(errorMessage, {
                    timeOut: 2000,
                });
            }
        });
    });
});
