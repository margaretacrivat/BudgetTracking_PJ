const usernameField = document.getElementById("id_username");
const feedbackArea = document.querySelector('.invalid-feedback');

// validate username
// pick what the user is typing
usernameField.addEventListener('keyup',(e)=>{
    // console.log('77777', 77777);
    const usernameVal=e.target.value;

usernameField.classList.remove('is-invalid');
feedbackArea.style.display='none';


//     make an API call to our server
    if (usernameVal.length > 0){
      fetch('/userauthentication/validate-username/',{
         body: JSON.stringify({ username: usernameVal }),
         method: 'POST',
    })
      .then(res => res.json())
      .then(data => {
        console.log('userdata', data);
        if(data.username_error) {
            feedbackArea.classList.add('invalid-feedback');
            usernameField.classList.add('is-invalid');
            feedbackArea.style.display='block';
            feedbackArea.innerHTML=`<p>${data.username_error}</p>`;
        }
      });
    }
});


