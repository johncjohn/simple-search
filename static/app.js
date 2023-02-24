// Hide all the forms by default
const forms = document.querySelectorAll('.tab-container form');
forms.forEach(form => form.classList.add('hidden'));

// Show the sign in form by default
const signInForm = document.querySelector('.signin-form');
signInForm.classList.remove('hidden');

// Add event listeners to the tab buttons
const tabButtons = document.querySelectorAll('.tablinks');
tabButtons.forEach(button => {
  button.addEventListener('click', (event) => {
    // Hide all the forms
    forms.forEach(form => form.classList.add('hidden'));

    // Show the corresponding form
    const target = event.currentTarget.getAttribute('data-target');
    const formToShow = document.querySelector(`.${target}`);
    formToShow.classList.remove('hidden');
  });
});

