const togglePassword = document.querySelector("#togglePassword");
const password = document.querySelector("#password");
$('#togglePassword').on('click', function() {
    // toggle the type attribute
    const type = password.getAttribute("type") === "password" ? "text" : "password";
    password.setAttribute("type", type);
    $(this).find('i').toggleClass('bi-eye bi-eye-slash');
})

let usernameValid = false
let usernameErrorMessage = ''
$('#username').on('keyup', function() {
    const value = $(this).val()

    if (value != '') {
        $.ajax({
            'url': '/authentication/validate-username',
            'method': 'POST',
            'datatype': 'jsonp',
            'data': JSON.stringify({username: value}),
            'success': function (response) {
                usernameValid = true
            },
            'error': function (e) {
                usernameValid = false
                usernameErrorMessage = e.responseJSON.username_error
            }
        })
    }
})

$('#username').on('change', function() {
    var messageElement = $('#username').next()

    if (usernameValid) {
        $('#username').removeClass('is-invalid')
        $('#username').addClass('is-valid')
        messageElement.html('')
        messageElement.removeClass('text-danger')
        messageElement.addClass('text-success')
    }
    else {
        if (usernameErrorMessage != '') {
            $('#username').removeClass('is-valid')
            $('#username').addClass('is-invalid')
            messageElement.html(usernameErrorMessage)
            messageElement.removeClass('text-success')
            messageElement.addClass('text-danger')
        }
    }

    toggleRegisterButton()
})

let emailValid = false
let emailErrorMessage = ''
$('#email').on('keyup', function() {
    const value = $(this).val()

    if (value != '') {
        $.ajax({
            'url': '/authentication/validate-email',
            'method': 'POST',
            'datatype': 'jsonp',
            'data': JSON.stringify({email: value}),
            'success': function (response) {
                emailValid = true
            },
            'error': function (e) {
                emailValid = false
                emailErrorMessage = e.responseJSON.email_error
            }
        })
    }
})

$('#email').on('change', function() {
    var messageElement = $('#email').next()

    if (emailValid) {
        $('#email').removeClass('is-invalid')
        $('#email').addClass('is-valid')
        messageElement.html('')
        messageElement.removeClass('text-danger')
        messageElement.addClass('text-success')
    }
    else {
        if (emailErrorMessage != '') {
            $('#email').removeClass('is-valid')
            $('#email').addClass('is-invalid')
            messageElement.html(emailErrorMessage)
            messageElement.removeClass('text-success')
            messageElement.addClass('text-danger')
        }
    }

    toggleRegisterButton()
})

let passwordValid = false
let passwordErrorMessage = ''
$('#password').on('change', function () {
    const value = $(this).val()
    var passwordAlert = $(this).parent().next()

    passwordValid = false
    if (value != '') {
        passwordValid = value.length >= 8
        if (value.length < 8) {
            passwordErrorMessage = 'Password must have a minimum of 8 characters'
            passwordAlert.html(passwordErrorMessage)
            passwordAlert.addClass('text-danger')
            $(this).removeClass('is-valid')
            $(this).addClass('is-invalid')
        }
        else {
            passwordAlert.html('')
            $(this).removeClass('is-invalid')
            $(this).addClass('is-valid')
        }
    }

    toggleRegisterButton()
})

function toggleRegisterButton() {
    if (usernameValid && emailValid && passwordValid) {
        $('#btn-register').removeAttr('disabled')
    }
    else {
        $('#btn-register').attr('disabled', 'disabled')
    }
}