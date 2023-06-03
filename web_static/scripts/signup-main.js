$(document).ready(() => {
    $('button').on('click', (event) => {
        event.preventDefault();

	let username = $('input[name="username"]').val();
        username = username.replace('@', '');
        const email = $('input[name="email"]').val();
        const password = $('input[name="password"]').val();

        if (username.trim() === '' || email.trim() === '' || password.trim() === '') {
            toastr.error('Oops!, You forgot to enter your username, email and password!', {
                timeOut: 2000,
            });
          return;
        }

        let new_partner = {
            "username": username,
            "email": email,
        }

        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5000/api/v1/partners',
            contentType: 'application/json',
            data: JSON.stringify(new_partner),
            success: (response) => {
                
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


        let new_user = {
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
