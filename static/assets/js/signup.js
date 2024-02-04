const usernameField = document.getElementById("id_username");
const userFeedbackArea = document.querySelector('.userInvalidFeedback');
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput');

const emailField = document.getElementById("id_email");
const emailFeedbackArea = document.querySelector('.emailFeedbackArea');
const emailSuccessOutput = document.querySelector('.emailSuccessOutput');

const passwordField = document.getElementById("id_password1");
const passwordFeedbackArea = document.querySelector('.passwordFeedbackArea');
const passwordSuccessOutput = document.querySelector('.passwordSuccessOutput');
const confirmPasswordField = document.getElementById("id_password2");
const confirmPasswordFeedbackArea = document.querySelector('.confirmPasswordFeedbackArea');

const showPasswordToggle = document.querySelector('.showPasswordToggle');

const submitBtn = document.querySelector('.btn-submit');

let timeoutId;

// validate username

usernameField.addEventListener('keyup', (e) => {
    const usernameVal = e.target.value;
    usernameField.classList.remove('is-invalid');
    userFeedbackArea.style.display = 'none';

    clearTimeout(timeoutId);

    if (usernameVal.length > 0) {
        usernameSuccessOutput.style.display = 'block';
        usernameSuccessOutput.textContent = `Checking ${usernameVal}`;

        timeoutId = setTimeout(() => {
            fetch('/userauthentication/validate-username/', {
                body: JSON.stringify({
                    username: usernameVal,
                    // password: passwordField.value, // pass the password along with the username
                }),
                method: 'POST',
            })
                .then(res => res.json())
                .then(data => {
                    // console.log('username_data', data);
                    usernameSuccessOutput.style.display = 'none';
                    if (data.username_error) {
                        submitBtn.disabled = true;
                        usernameField.classList.add('is-invalid');
                        userFeedbackArea.style.display = 'block';
                        userFeedbackArea.innerHTML = `<p>${data.username_error}</p>`;
                    } else {
                        submitBtn.removeAttribute('disabled');
                    }
                });
        }, 500);
    } else {
        usernameSuccessOutput.style.display = 'none';
    }
});


// validate email

emailField.addEventListener('keyup', (e) => {
    const emailVal = e.target.value;
    emailField.classList.remove('is-invalid');
    emailFeedbackArea.style.display = 'none';

    clearTimeout(timeoutId);

//     make an API call to our server
    // pick what the user is typing
    if (emailVal.length > 0) {
        emailSuccessOutput.style.display = 'block';
        emailSuccessOutput.textContent = `Checking ${emailVal}`; // to append what we are checking

        timeoutId = setTimeout(() => {
            fetch('/userauthentication/validate-email/', {
                body: JSON.stringify({email: emailVal}),
                method: 'POST',
            })
                .then(res => res.json())
                .then(data => {
                    console.log('email_data', data);
                    emailSuccessOutput.style.display = 'none';
                    if (data.email_error) {
                        submitBtn.disabled = true;
                        emailField.classList.add('is-invalid');
                        emailFeedbackArea.style.display = 'block';
                        emailFeedbackArea.innerHTML = `<p>${data.email_error}</p>`;
                    } else {
                        submitBtn.removeAttribute('disabled'); // if there is no error
                    }
                });
        }, 500); // The API request is made after a certain delay, giving the user some time to finish typing
    } else {
        emailSuccessOutput.style.display = 'none';
    }
});


const handleToggleInput = (e) => {
    if (showPasswordToggle.textContent === 'Show') {
        showPasswordToggle.textContent = 'Hide';
        passwordField.setAttribute('type', 'text');
    } else {
        showPasswordToggle.textContent = 'Show';
        passwordField.setAttribute('type', 'password');
    }
};
showPasswordToggle.addEventListener('click', handleToggleInput);


// validate password
passwordField.addEventListener('keyup', (e) => {
    const passwordVal = e.target.value;
    passwordField.classList.remove('is-invalid');
    passwordFeedbackArea.style.display = 'none';

    clearTimeout(timeoutId);

    if (passwordVal.length > 0) {
        passwordSuccessOutput.style.display = 'block';

        timeoutId = setTimeout(() => {
            fetch('/userauthentication/validate-password/', {
                body: JSON.stringify({password: passwordVal}),
                method: 'POST',
            })
                .then(res => res.json())
                .then(data => {
                    console.log('password_data', data);
                    if (data.password_error) {
                        submitBtn.disabled = true;
                        passwordField.classList.add('is-invalid');
                        passwordFeedbackArea.style.display = 'block';
                        passwordFeedbackArea.innerHTML = `<p>${data.password_error}</p>`;
                    } else {
                        submitBtn.removeAttribute('disabled');
                    }
                });
        }, 500);
    } else {
        passwordSuccessOutput.style.display = 'none';
    }
});

// validate password confirmation
confirmPasswordField.addEventListener('input', (e) => {
    const confirmPasswordVal = e.target.value;
    confirmPasswordField.classList.remove('is-invalid');
    confirmPasswordFeedbackArea.style.display = 'none';

    clearTimeout(timeoutId);

    const passwordVal = passwordField.value;

    if (confirmPasswordVal !== passwordVal) {
        submitBtn.disabled = true;
        confirmPasswordField.classList.add('is-invalid');
        confirmPasswordFeedbackArea.style.display = 'block';
        confirmPasswordFeedbackArea.innerHTML = '<p>The two passwords must match.</p>';
    } else {
        submitBtn.removeAttribute('disabled');
        confirmPasswordField.classList.remove('is-invalid');  // Clear error when passwords match
        confirmPasswordFeedbackArea.style.display = 'none';
    }
});

