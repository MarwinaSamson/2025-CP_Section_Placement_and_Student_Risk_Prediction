// document.addEventListener("DOMContentLoaded", () => {
  
//   const studentFileInput = document.getElementById("photo-upload")
//   const studentPhotoPreview = document.getElementById("photo-preview")
//   const studentUploadIcon = document.querySelector(".upload-icon-container")

//   if (studentFileInput) {
//     studentFileInput.addEventListener("change", (event) => {
//       const file = event.target.files[0]
//       if (file) {
//         const reader = new FileReader()
//         reader.onload = (e) => {
//           studentPhotoPreview.src = e.target.result
//           studentPhotoPreview.style.display = "block"
//           studentUploadIcon.style.display = "none"
//         }
//         reader.readAsDataURL(file)
//       }
//     })
//   }

  
//   const parentFileInput = document.getElementById("parent-photo-upload")
//   const parentPhotoPreview = document.getElementById("parent-photo-preview")
//   const parentUploadIcon = document.querySelector(".upload-area .upload-icon-container")

//   if (parentFileInput) {
//     parentFileInput.addEventListener("change", (event) => {
//       const file = event.target.files[0]
//       if (file) {
//         const reader = new FileReader()
//         reader.onload = (e) => {
//           parentPhotoPreview.src = e.target.result
//           parentPhotoPreview.style.display = "block"
//           if (parentUploadIcon) {
//             parentUploadIcon.style.display = "none"
//           }
//         }
//         reader.readAsDataURL(file)
//       }
//     })
//   }
// })

// document.addEventListener("DOMContentLoaded", () => {
//     const fourPsCheckbox = document.getElementById("fourPs");
//     const otherCheckboxes = document.querySelectorAll(".checkbox-options .option:not(#fourPs)");

//     fourPsCheckbox.addEventListener("change", () => {
//         if (fourPsCheckbox.checked) {
//             // Enable other checkboxes if 4 Ps is selected
//             otherCheckboxes.forEach(checkbox => {
//                 checkbox.disabled = false;  // Enable them
//             });
//         } else {
//             // If 4 Ps is not selected, uncheck all other checkboxes and enable them
//             otherCheckboxes.forEach(checkbox => {
//                 checkbox.checked = false; // Uncheck them
//                 checkbox.disabled = false; // Enable them
//             });
//         }
//     });

//     // Add event listeners to other checkboxes
//     otherCheckboxes.forEach(checkbox => {
//         checkbox.addEventListener("change", () => {
//             if (checkbox.checked) {
//                 // Uncheck all other checkboxes if one of them is checked
//                 otherCheckboxes.forEach(other => {
//                     if (other !== checkbox) {
//                         other.checked = false;
//                     }
//                 });
//             }
//         });
//     });
// });

 
// document.addEventListener("DOMContentLoaded", function () {
//   /**
//    * Enables or disables a text input field
//    * based on the selected radio button value.
//    *
//    * @param {string} radioName - Name attribute of the radio group
//    * @param {string} inputId - ID of the text input to enable/disable
//    */
//   function setupRadioControl(radioName, inputId) {
//     const radios = document.querySelectorAll(`input[name="${radioName}"]`);
//     const textInput = document.getElementById(inputId);

//     radios.forEach(radio => {
//       radio.addEventListener("change", function () {
//         if (this.value === "True") {
//           textInput.disabled = false;
//           textInput.focus();
//         } else {
//           textInput.disabled = true;
//           textInput.value = ""; // Clear text when disabled
//         }
//       });
//     });
//   }

//   // Initialize both sections
//   setupRadioControl("is_sped", "additional-info"); 
//   setupRadioControl("is_working_student", "additional-info-working");
// });

console.log("preEnlistment.js is loaded!");

document.addEventListener("DOMContentLoaded", () => {
  /*** STUDENT PHOTO PREVIEW ***/
  const studentFileInput = document.getElementById("photo-upload");
  const studentPhotoPreview = document.getElementById("photo-preview");
  const studentUploadIcon = document.querySelector(".upload-icon-container");
  const photoValidation = document.getElementById("photo-validation");
  const uploadAreaLabel = document.getElementById("upload-area-label"); 

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
                uploadAreaLabel.classList.add('has-preview'); // ADD THIS
            }

            // Preview logic
            if (file.type.startsWith("image/")) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    if (studentPhotoPreview) {
                        studentPhotoPreview.src = e.target.result;
                        studentPhotoPreview.style.display = "block";
                    }
                    // Remove the upload icon display logic - let CSS handle it
                };
                reader.readAsDataURL(file);
            } else {
                alert("Please select a valid image file.");
                studentFileInput.value = ""; // reset input
                if (studentPhotoPreview) {
                    studentPhotoPreview.style.display = "none";
                }
                if (uploadAreaLabel) {
                    uploadAreaLabel.classList.remove('has-preview'); // REMOVE PREVIEW STATE
                }
            }
        }
    });
}

  /*** 4Ps CHECKBOX LOGIC ***/
  const checkboxes = document.querySelectorAll(".checkbox-options input[type='checkbox']");
  let fourPsCheckbox = null;

  checkboxes.forEach((checkbox) => {
    const labelText = checkbox.parentElement.textContent.trim().toLowerCase();
    if (labelText.includes("4 ps member")) {
      fourPsCheckbox = checkbox;
    }
  });

  if (fourPsCheckbox) {
    console.log("4Ps checkbox detected:", fourPsCheckbox);

    const otherCheckboxes = Array.from(checkboxes).filter(cb => cb !== fourPsCheckbox);

    fourPsCheckbox.addEventListener("change", () => {
      if (fourPsCheckbox.checked) {
        otherCheckboxes.forEach(cb => cb.disabled = false);
      } else {
        otherCheckboxes.forEach(cb => {
          cb.checked = false;
          cb.disabled = false;
        });
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


