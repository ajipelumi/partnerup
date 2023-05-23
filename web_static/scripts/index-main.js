$(document).ready(() => {
    $('button').on('click', (event) => {
        event.preventDefault();

        const username = $('input[name="username"]').val();
        const password = $('input[name="password"]').val();

        if (username.trim() === '' || password.trim() === '') {
            toastr.error('Oops!, You forgot to enter your username and password!', {
                timeOut: 2000,
            });
          return;
        }
        });
});