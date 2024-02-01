const usernameField = document.getElementById("id_username");
const userFeedbackArea = document.querySelector('.userInvalidFeedback');

const emailField = document.getElementById("id_email");
const emailFeedbackArea = document.querySelector('.emailFeedbackArea');

const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput');
const emailSuccessOutput = document.querySelector('.emailSuccessOutput');

const passwordField = document.getElementById("id_password1");
const showPasswordToggle = document.querySelector('.showPasswordToggle');


const handleToggleInput = (e) => {
    if(showPasswordToggle.textContent === 'Show') {
        showPasswordToggle.textContent = 'Hide';
        passwordField.setAttribute('type', 'text');
    } else {
        showPasswordToggle.textContent = 'Show';
        passwordField.setAttribute('type', 'password');
    }
};

showPasswordToggle.addEventListener('click', handleToggleInput);


// validate email

let timeoutId;
emailField.addEventListener('keyup', (e) => {
    const emailVal = e.target.value;
    emailField.classList.remove('is-invalid');
    emailFeedbackArea.style.display='none';

    clearTimeout(timeoutId);

//     make an API call to our server
    if (emailVal.length > 0) {
        emailSuccessOutput.style.display = 'block';
        emailSuccessOutput.textContent=`Checking ${emailVal}`; // to append what we are checking

        timeoutId = setTimeout(() => {
          fetch('/userauthentication/validate-email/',{
             body: JSON.stringify({ email: emailVal }),
             method: 'POST',
          })
              .then(res => res.json())
              .then(data => {
                  console.log('email_data', data);
                  emailSuccessOutput.style.display = 'none';
                  if(data.email_error) {
                      // emailFeedbackArea.classList.add('invalid-feedback');
                      emailField.classList.add('is-invalid');
                      emailFeedbackArea.style.display='block';
                      emailFeedbackArea.innerHTML=`<p>${data.email_error}</p>`;
                  }
              });
        }, 500); // The API request is made after a certain delay, giving the user some time to finish typing
    } else {
        emailSuccessOutput.style.display = 'none';
    }
});


// validate username

// pick what the user is typing
usernameField.addEventListener('keyup',(e)=> {
    const usernameVal = e.target.value;
    usernameField.classList.remove('is-invalid');
    userFeedbackArea.style.display='none';

    clearTimeout(timeoutId);

    if (usernameVal.length > 0) {
        usernameSuccessOutput.style.display = 'block';
        usernameSuccessOutput.textContent=`Checking ${usernameVal}`;

        timeoutId = setTimeout(() => {
            //     make an API call to our server
            fetch('/userauthentication/validate-username/', {
                body: JSON.stringify({username: usernameVal}),
                method: 'POST',
            })
                .then(res => res.json())
                .then(data => {
                    console.log('username_data', data);
                    usernameSuccessOutput.style.display = 'none';
                    if (data.username_error) {
                        usernameField.classList.add('is-invalid');
                        userFeedbackArea.style.display = 'block';
                        userFeedbackArea.innerHTML = `<p>${data.username_error}</p>`;
                    }
                });
        }, 500);
    } else {
        usernameSuccessOutput.style.display = 'none';
    }
});





