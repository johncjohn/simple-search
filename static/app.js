const tabButtons = document.querySelectorAll('.tab-container .tabs button');
  const forms = document.querySelectorAll('.tab-container form');

  // Add a click event listener to each tab button
  tabButtons.forEach((button, index) => {
    button.addEventListener('click', () => {
      // Remove the "active" class from all tab buttons and forms
      tabButtons.forEach(btn => btn.classList.remove('active'));
      forms.forEach(form => form.style.display = 'none');

      // Add the "active" class to the clicked tab button and show the corresponding form
      button.classList.add('active');
      forms[index].style.display = 'block';
    });
  });

  // Show the first form by default
  tabButtons[0].click();