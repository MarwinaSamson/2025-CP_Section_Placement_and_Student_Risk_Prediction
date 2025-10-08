<<<<<<< Updated upstream
document.addEventListener("DOMContentLoaded", () => {
  
  const studentFileInput = document.getElementById("photo-upload")
  const studentPhotoPreview = document.getElementById("photo-preview")
  const studentUploadIcon = document.querySelector(".upload-icon-container")

  if (studentFileInput) {
    studentFileInput.addEventListener("change", (event) => {
      const file = event.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          studentPhotoPreview.src = e.target.result
          studentPhotoPreview.style.display = "block"
          studentUploadIcon.style.display = "none"
        }
        reader.readAsDataURL(file)
      }
    })
  }
=======
console.log("preEnlistment.js is loaded!");

document.addEventListener("DOMContentLoaded", () => {
  /*** STUDENT PHOTO PREVIEW & VALIDATION ***/
  const studentFileInput = document.getElementById("photo-upload");
  const studentPhotoPreview = document.getElementById("photo-preview");
  const studentUploadIcon = document.querySelector(".upload-icon-container");
  const photoValidation = document.getElementById("photo-validation");
  const uploadAreaLabel = document.getElementById("upload-area-label");

  

  // In preEnlistment.js - Update the student photo preview section
if (studentFileInput) {
    console.log("Photo upload input detected.");
    
    studentFileInput.removeAttribute('required');

    studentFileInput.addEventListener("change", (event) => {
        const file = event.target.files[0];
        
        if (file) {
            // Hide validation message and remove error styling
            if (photoValidation) {
                photoValidation.style.display = 'none';
            }
            if (uploadAreaLabel) {
                uploadAreaLabel.classList.remove('has-error');
            }

            // Preview logic
            if (file.type.startsWith("image/")) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    if (studentPhotoPreview) {
                        studentPhotoPreview.src = e.target.result;
                        studentPhotoPreview.style.display = "block";
                        uploadAreaLabel.classList.add("has-preview");
                    }
                    if (studentUploadIcon) {
                        studentUploadIcon.style.display = "none";
                    }
                };
                reader.readAsDataURL(file);
            } else {
                alert("Please select a valid image file.");
                studentFileInput.value = ""; // reset input
                if (studentPhotoPreview) {
                    studentPhotoPreview.style.display = "none";
                    uploadAreaLabel.classList.remove("has-preview");
                }
                if (studentUploadIcon) {
                    studentUploadIcon.style.display = "flex";
                }
            }
        }
    });
}  else {
    console.warn("Photo upload input NOT found!");
}
>>>>>>> Stashed changes

  
  const parentFileInput = document.getElementById("parent-photo-upload")
  const parentPhotoPreview = document.getElementById("parent-photo-preview")
  const parentUploadIcon = document.querySelector(".upload-area .upload-icon-container")

  if (parentFileInput) {
    parentFileInput.addEventListener("change", (event) => {
      const file = event.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          parentPhotoPreview.src = e.target.result
          parentPhotoPreview.style.display = "block"
          if (parentUploadIcon) {
            parentUploadIcon.style.display = "none"
          }
        }
        reader.readAsDataURL(file)
      }
    })
  }
})


// StudentAcademic.html

document.addEventListener('DOMContentLoaded', function () {
            const subjectInputs = document.querySelectorAll('.subjects-grid input[type="number"]');
            const overallAverageInput = document.getElementById('overallAverage');

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
        });
<<<<<<< Updated upstream
=======
      }
    });

    otherCheckboxes.forEach(checkbox => {
      checkbox.addEventListener("change", () => {
        if (checkbox.checked) {
          otherCheckboxes.forEach(other => {
            if (other !== checkbox) other.checked = false;
          });
        }
      });
    });

  } else {
    console.warn("4Ps checkbox NOT found!");
  }

  /*** PWD & WORKING STUDENT LOGIC ***/
  const spedDetails = document.getElementById("id_sped_details");
  const workingDetails = document.getElementById("id_working_details");

  if (spedDetails) spedDetails.disabled = true;
  if (workingDetails) workingDetails.disabled = true;

  function handleRadioToggle(radioName, inputField) {
    const radios = document.querySelectorAll(`input[name="${radioName}"]`);
    radios.forEach(radio => {
      radio.addEventListener("change", function () {
        if (this.value === "1") {
          inputField.disabled = false;
          inputField.focus(); // auto-highlight when enabled
        } else {
          inputField.disabled = true;
          inputField.value = ""; // clear if disabled
        }
      });
    });
  }

  if (spedDetails) {
    handleRadioToggle("is_sped", spedDetails);
  }

  if (workingDetails) {
    handleRadioToggle("is_working_student", workingDetails);
  }

  /*** LRN VALIDATION ***/
  const lrnInput = document.getElementById("id_lrn");
  const lrnValidation = document.getElementById("lrn-validation");

  if (lrnInput) {
    lrnInput.setAttribute("maxlength", "12");
    lrnInput.setAttribute("pattern", "\\d{12}");
    lrnInput.setAttribute("title", "LRN must be exactly 12 digits.");

    lrnInput.addEventListener("input", function() {
      const lrnValue = this.value.replace(/[^0-9]/g, '');
      this.value = lrnValue;
      
      if (lrnValue.length > 0 && lrnValue.length !== 12) {
        if (lrnValidation) {
          lrnValidation.style.display = 'block';
        }
        this.classList.add('field-error');
      } else {
        if (lrnValidation) {
          lrnValidation.style.display = 'none';
        }
        this.classList.remove('field-error');
      }
    });
    
    // Trigger validation on page load if there's existing value
    if (lrnInput.value) {
      lrnInput.dispatchEvent(new Event('input'));
    }
  }

  /*** AGE CALCULATION FROM BIRTHDATE ***/
  function calculateAge(birthDate) {
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
      age--;
    }
    
    return age;
  }
  
  const birthDateInput = document.getElementById("id_date_of_birth");
  const ageDisplay = document.getElementById("student-age-display");
  
  if (birthDateInput && ageDisplay) {
    birthDateInput.addEventListener("change", function() {
      if (this.value) {
        const birthDate = new Date(this.value);
        const age = calculateAge(birthDate);
        ageDisplay.textContent = `Age: ${age}`;
      } else {
        ageDisplay.textContent = "Age: --";
      }
    });
    
    // Calculate age on page load if birthdate exists
    if (birthDateInput.value) {
      birthDateInput.dispatchEvent(new Event('change'));
    }
  }

  /*** FORM VALIDATION BEFORE SUBMISSION ***/
  const form = document.getElementById("studentDataForm");
  if (form) {
    form.addEventListener("submit", function(event) {
      let isValid = true;
      
      // LRN validation
      if (lrnInput && lrnInput.value.length !== 12) {
        if (lrnValidation) {
          lrnValidation.style.display = 'block';
        }
        lrnInput.classList.add('field-error');
        isValid = false;
      }
      
      // Photo validation
      if (studentFileInput && (!studentFileInput.files || studentFileInput.files.length === 0)) {
        if (photoValidation) {
          photoValidation.style.display = 'block';
        }
        if (uploadAreaLabel) {
          uploadAreaLabel.classList.add('has-error');
        }
        isValid = false;
        
        // Scroll to photo upload area
        if (photoValidation) {
          photoValidation.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }
      
      if (!isValid) {
        event.preventDefault();
        // Scroll to first error
        const firstError = document.querySelector('.field-error, .file-validation-message[style*="display: block"]');
        if (firstError) {
          firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }
    });
  }

  /*** PARENT PHOTO PREVIEW (for familyData.html) ***/
  const parentFileInput = document.getElementById("id_parent_photo");
  const parentPhotoPreview = document.getElementById("parent-photo-preview");
  const parentUploadIcon = document.querySelector(".upload-area .upload-icon-container");

  if (parentFileInput && parentPhotoPreview && parentUploadIcon) {
    parentFileInput.addEventListener("change", (event) => {
      const file = event.target.files[0];
      if (file && file.type.startsWith("image/")) {
        const reader = new FileReader();
        reader.onload = (e) => {
          parentPhotoPreview.src = e.target.result;
          parentPhotoPreview.style.display = "block";
          parentUploadIcon.style.display = "none";
        };
        reader.readAsDataURL(file);
      } else {
        alert("Please select a valid image file.");
        parentFileInput.value = ""; // reset input
        parentPhotoPreview.style.display = "none";
        parentUploadIcon.style.display = "block";
      }
    });
  }

}); // DOMContentLoaded ends here
>>>>>>> Stashed changes
