document.addEventListener("DOMContentLoaded", function() {

    const signinLink = document.getElementById('signin-link');
    const signupLink = document.getElementById('signup-link');
    const forgotPasswordLink = document.getElementById('forgot-password-link');
  
    const signinSection = document.getElementById('signin-section');
    const signupSection = document.getElementById('signup-section');
    const forgotPasswordSection = document.getElementById('forgot-password-section');
  
    signinLink.addEventListener('click', function(event) {
      event.preventDefault();
      signupSection.classList.remove('show');
      forgotPasswordSection.classList.remove('show');
      signinSection.classList.add('show');
    });
  
    signupLink.addEventListener('click', function(event) {
      event.preventDefault();
      signinSection.classList.remove('show');
      forgotPasswordSection.classList.remove('show');
      signupSection.classList.add('show');
    });
  
    forgotPasswordLink.addEventListener('click', function(event)
  