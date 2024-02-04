const currentPasswordField = document.getElementById("current_password");
const currentPasswordFeedbackArea = document.querySelector('.currentPasswordFeedbackArea');
const currentPasswordSuccessOutput = document.querySelector('.currentPasswordSuccessOutput');

const newPasswordField = document.getElementById("new_password1");
const newPasswordFeedbackArea = document.querySelector('.newPasswordFeedbackArea');
const newPasswordSuccessOutput = document.querySelector('.newPasswordSuccessOutput');

const confirmNewPasswordField = document.getElementById("new_password2");
const confirmNewPasswordFeedbackArea = document.querySelector('.confirmNewPasswordFeedbackArea');

const showPasswordToggle1 = document.querySelector('.showPasswordToggle1');
const showPasswordToggle2 = document.querySelector('.showPasswordToggle2');

const submitPswBtn = document.querySelector('.btn-submit-psw');

const handleToggleInput1 = (e) => {
    if (showPasswordToggle1.textContent === 'Show') {
        showPasswordToggle1.textContent = 'Hide';
        currentPasswordField.setAttribute('type', 'text');
    } else {
        showPasswordToggle1.textContent = 'Show';
        currentPasswordField.setAttribute('type', 'password');
    }
};
showPasswordToggle1.addEventListener('click', handleToggleInput1);


const handleToggleInput2 = (e) => {
    if (showPasswordToggle2.textContent === 'Show') {
        showPasswordToggle2.textContent = 'Hide';
        newPasswordField.setAttribute('type', 'text');
    } else {
        showPasswordToggle2.textContent = 'Show';
        newPasswordField.setAttribute('type', 'password');
    }
};

showPasswordToggle2.addEventListener('click', handleToggleInput2);


let timeoutId;

// validate current password
currentPasswordField.addEventListener('keyup', (e) => {
    const currentPasswordVal = e.target.value;
    currentPasswordField.classList.remove('is-invalid');
    currentPasswordFeedbackArea.style.display = 'none';

    clearTimeout(timeoutId);

    if (currentPasswordVal.length > 0) {
        currentPasswordSuccessOutput.style.display = 'block';

        timeoutId = setTimeout(() => {
            fetch('/userauthentication/validate-current-password/', {
                body: JSON.stringify({
                    current_password: currentPasswordVal,
                    new_password1: newPasswordField.value  // Include the new password
                }),
                method: 'POST',
            })
                .then(res => res.json())
                .then(data => {
                    console.log('password_data', data);
                    if (data.password_error) {
                        submitPswBtn.disabled = true;
                        currentPasswordField.classList.add('is-invalid');
                        currentPasswordFeedbackArea.style.display = 'block';
                        currentPasswordFeedbackArea.innerHTML = `<p>${data.password_error}</p>`;
                    } else {
                    currentPasswordSuccessOutput.style.display = 'none';
                    newPasswordField.removeAttribute('disabled'); // Enable the new password field
                    confirmNewPasswordField.removeAttribute('disabled'); // Enable the confirm new password field
                }
            });
        }, 500);
    } else {
        currentPasswordSuccessOutput.style.display = 'none';
    }
});


// new password

newPasswordField.addEventListener('keyup', (e) => {
    const newPasswordVal = e.target.value;
    newPasswordField.classList.remove('is-invalid');
    newPasswordFeedbackArea.style.display = 'none';

    // Check if the new password is the same as the current password
    if (newPasswordVal === currentPasswordField.value) {
        submitPswBtn.disabled = true;
        newPasswordField.classList.add('is-invalid');
        newPasswordFeedbackArea.style.display = 'block';
        newPasswordFeedbackArea.innerHTML = '<p>The new password must be different than the current password</p>';
        return; // Stop further processing if the passwords match
    }

    clearTimeout(timeoutId);

    if (newPasswordVal.length > 0) {
        newPasswordSuccessOutput.style.display = 'block';

        timeoutId = setTimeout(() => {
            fetch('/userauthentication/set-new-password/', {
                body: JSON.stringify({new_password1: newPasswordVal}),
                method: 'POST',
            })
                .then(res => res.json())
                .then(data => {
                    console.log('password_data', data);
                    if (data.password_error) {
                        submitPswBtn.disabled = true;
                        newPasswordField.classList.add('is-invalid');
                        newPasswordFeedbackArea.style.display = 'block';
                        newPasswordFeedbackArea.innerHTML = `<p>${data.password_error}</p>`;
                    } else {
                        submitPswBtn.removeAttribute('disabled');
                    }
                });
        }, 500);
    } else {
        newPasswordSuccessOutput.style.display = 'none';
    }
});


// validate new password confirmation
confirmNewPasswordField.addEventListener('input', (e) => {
    const confirmNewPasswordVal = e.target.value;
    confirmNewPasswordField.classList.remove('is-invalid');
    confirmNewPasswordFeedbackArea.style.display = 'none';

    clearTimeout(timeoutId);

    const newPasswordVal = newPasswordField.value;

    if (confirmNewPasswordVal !== newPasswordVal) {
        submitPswBtn.disabled = true;
        confirmNewPasswordField.classList.add('is-invalid');
        confirmNewPasswordFeedbackArea.style.display = 'block';
        confirmNewPasswordFeedbackArea.innerHTML = '<p>The two passwords must match.</p>';
    } else {
        // successful confirmation
        submitPswBtn.removeAttribute('disabled');
        confirmNewPasswordField.classList.remove('is-invalid');  // Clear error when passwords match
        confirmNewPasswordFeedbackArea.style.display = 'none';

        // After successful confirmation, log out the user
        fetch('/userauthentication/logout/', {
            method: 'POST',
        })
        .then(res => res.json())
        .then(data => {
            if (data.logout_success) {
                // Redirect to login page or perform any other actions
                window.location.href = '/userauthentication/login/';
            }
        });
    }
});
