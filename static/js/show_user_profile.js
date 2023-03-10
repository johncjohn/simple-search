
  const studentForm = document.getElementById('student_form');
  const stafferForm = document.getElementById('staffer_form');
  const userTypeField = document.getElementById('user_type');

  userTypeField.addEventListener('change', (event) => {
    const selectedOption = event.target.value;

    if (selectedOption === 'student') {
      studentForm.style.display = 'block';
      stafferForm.style.display = 'none';
    } else if (selectedOption === 'staffer') {
      studentForm.style.display = 'none';
      stafferForm.style.display = 'block';
    }
  });

