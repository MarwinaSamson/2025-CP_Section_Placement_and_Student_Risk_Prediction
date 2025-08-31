 // Function to toggle the DOST exam result upload visibility
        function toggleDOSTUpload() {
    const dostExamSelect = document.getElementById('dostExam');
    const dostUploadContainer = document.getElementById('dostUploadContainer');
    
    if (dostExamSelect.value === 'passed') {
        dostUploadContainer.style.display = 'block'; // Show upload section if passed
    } else {
        dostUploadContainer.style.display = 'none'; // Hide upload section if failed or not taken
    }
}

// Call the function on page load to set the initial state
document.addEventListener("DOMContentLoaded", toggleDOSTUpload);

document.addEventListener("DOMContentLoaded", function () {
  const subjectInputs = document.querySelectorAll('.subjects-grid input[type="number"]');
  const overallAverageInput = document.getElementById("overallAverage");

  function calculateAverage() {
    let total = 0;
    let count = 0;

    subjectInputs.forEach((input) => {
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
      overallAverageInput.value = "";
    }
  }

  subjectInputs.forEach((input) => {
    input.addEventListener("input", calculateAverage);
  });

  // File upload handling for report card
  const reportCardInput = document.getElementById("reportCard");
  const reportCardButton = document.querySelector("label[for='reportCard'] + .file-input-container .file-button");
  const reportCardFileName = document.querySelector("label[for='reportCard'] + .file-input-container .file-name");

  reportCardButton.addEventListener("click", () => {
    reportCardInput.click();
  });

  reportCardInput.addEventListener("change", function () {
    if (this.files.length > 0) {
      reportCardFileName.textContent = this.files[0].name;
    } else {
      reportCardFileName.textContent = "No file chosen";
    }
  });

  // File upload handling for DOST exam result
  const dostResultInput = document.getElementById("dost_result");
  const dostResultButton = document.querySelector("label[for='distresult'] + .file-input-container .file-button");
  const dostResultFileName = document.querySelector("label[for='distresult'] + .file-input-container .file-name");

  dostResultButton.addEventListener("click", () => {
    dostResultInput.click();
  });

  dostResultInput.addEventListener("change", function () {
    if (this.files.length > 0) {
      dostResultFileName.textContent = this.files[0].name;
    } else {
      dostResultFileName.textContent = "No file chosen";
    }
  });

  const academicForm = document.getElementById("academicForm2");
  academicForm.addEventListener("submit", function (e) {
    e.preventDefault();

    // Basic form validation
    const requiredFields = this.querySelectorAll("[required]");
    let isValid = true;

    requiredFields.forEach((field) => {
      if (!field.value.trim()) {
        isValid = false;
        field.style.borderColor = "#c00";
      } else {
        field.style.borderColor = "";
      }
    });

    if (isValid) {
      // Use the URL defined in the template
      window.location.href = redirectUrl; // This should work now
    } else {
      alert("Please fill in all required fields.");
    }
  });
});