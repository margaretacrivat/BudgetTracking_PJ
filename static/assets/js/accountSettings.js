const oldPasswordField = document.getElementById('id_old_password');
const oldPasswordToggleBtn = document.querySelector('.toggle-old-password')

const newPasswordField = document.getElementById('id_new_password1');
const newPasswordToggleBtn = document.querySelector('.toggle-new-password')

oldPasswordToggleBtn.addEventListener('click', function() {
    this.classList.toggle('bxs-show');

    // Toggle the type attribute between 'password' and 'text' for the password field
    const type = oldPasswordField.getAttribute('type')
    === 'password' ? 'text' : 'password';
    oldPasswordField.setAttribute('type', type);
})

newPasswordToggleBtn.addEventListener('click', function() {
    this.classList.toggle('bxs-show');
    const type = newPasswordField.getAttribute('type')
    === 'password' ? 'text' : 'password';
    newPasswordField.setAttribute('type', type);
})



