
document.addEventListener('DOMContentLoaded', function () {
    const subjectInputs = document.querySelectorAll('.subjects-grid input[type="number"]');
    const overallAverageInput = document.getElementById('overallAverage');
    const academicForm = document.getElementById('academicForm2');

    function calculateAverage() {
        let total = 0;
        let count = 0;

        subjectInputs.forEach(input => {
            const value = parseFloat(input.value);
            if (!isNaN(value) && value > 0) {
                total += value;
                count++;
            }
        });

        if (count > 0) {
            const average = (total / count).toFixed(2);
            overallAverageInput.value = average;
        } else {
            overallAverageInput.value = '';
        }
    }

    subjectInputs.forEach(input => {
        input.addEventListener('input', calculateAverage);
    });

    const fileInputs = document.querySelectorAll('input[type="file"]');

    fileInputs.forEach(fileInput => {
        const fileButton = fileInput.parentElement.querySelector('.file-button');
        const fileName = fileInput.parentElement.querySelector('.file-name');

        fileButton.addEventListener('click', () => {
            fileInput.click();
        });

        fileInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                fileName.textContent = this.files[0].name;
            } else {
                fileName.textContent = 'No file chosen';
            }
        });
    });

    const dostExamSelect = document.getElementById('dostExam');
    const dostProofGroup = document.getElementById('dostProofGroup');
    const dostProofInput = document.getElementById('dostProof');

    dostExamSelect.addEventListener('change', function () {
        if (this.value === 'passed') {
            dostProofGroup.style.display = 'block';
            dostProofInput.required = true;
        } else {
            dostProofGroup.style.display = 'none';
            dostProofInput.required = false;
            dostProofInput.value = '';
            dostProofGroup.querySelector('.file-name').textContent = 'No file chosen';
        }
    });

    const workingStudentSelect = document.getElementById('workingStudent');
    const workTypeGroup = document.getElementById('workTypeGroup');
    const workTypeSelect = document.getElementById('workType');

    workingStudentSelect.addEventListener('change', function () {
        if (this.value === 'yes') {
            workTypeGroup.style.display = 'block';
            workTypeSelect.required = true;
        } else {
            workTypeGroup.style.display = 'none';
            workTypeSelect.required = false;
            workTypeSelect.value = '';
        }
    });

    const disabilitySelect = document.getElementById('disability');
    const disabilityTypeGroup = document.getElementById('disabilityTypeGroup');
    const disabilityTypeSelect = document.getElementById('disabilityType');

    disabilitySelect.addEventListener('change', function () {
        if (this.value === 'yes') {
            disabilityTypeGroup.style.display = 'block';
            disabilityTypeSelect.required = true;
        } else {
            disabilityTypeGroup.style.display = 'none';
            disabilityTypeSelect.required = false;
            disabilityTypeSelect.value = '';
        }
    });

    academicForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission
        
        // Basic form validation
        const requiredFields = this.querySelectorAll("[required]");
        let isValid = true;

        requiredFields.forEach((field) => {
            if (!field.value.trim()) {
                isValid = false;
                field.style.borderColor = "#c00"; // Highlight empty required fields
            } else {
                field.style.borderColor = ""; // Reset border color for valid fields
            }
        });

        if (isValid) {
            // If valid, redirect to the section placement page
            window.location.href = redirectUrl; // Use the URL defined in the template
        } else {
            alert("Please fill in all required fields.");
        }
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const workingStudentSelect = document.getElementById('workingStudent');
    const workTypeGroup = document.getElementById('workTypeGroup');
    const workTypeSelect = document.getElementById('workType');

    const disabilitySelect = document.getElementById('disability');
    const disabilityTypeGroup = document.getElementById('disabilityTypeGroup');
    const disabilityTypeSelect = document.getElementById('disabilityType');

    function toggleWorkType() {
        if (workingStudentSelect.value === 'yes') {
            workTypeGroup.style.display = 'block';
            workTypeSelect.disabled = false;
        } else {
            workTypeGroup.style.display = 'none';
            workTypeSelect.disabled = true;
            workTypeSelect.value = '';
        }
    }

    function toggleDisabilityType() {
        if (disabilitySelect.value === 'yes') {
            disabilityTypeGroup.style.display = 'block';
            disabilityTypeSelect.disabled = false;
        } else {
            disabilityTypeGroup.style.display = 'none';
            disabilityTypeSelect.disabled = true;
            disabilityTypeSelect.value = '';
        }
    }

    // Initial toggle on page load
    toggleWorkType();
    toggleDisabilityType();

    // Add event listeners
    workingStudentSelect.addEventListener('change', toggleWorkType);
    disabilitySelect.addEventListener('change', toggleDisabilityType);
});

