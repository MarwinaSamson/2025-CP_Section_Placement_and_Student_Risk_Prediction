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

document.addEventListener("DOMContentLoaded", () => {
    const fourPsCheckbox = document.getElementById("fourPs");
    const otherCheckboxes = document.querySelectorAll(".checkbox-options .option:not(#fourPs)");

    fourPsCheckbox.addEventListener("change", () => {
        if (fourPsCheckbox.checked) {
            // Enable other checkboxes if 4 Ps is selected
            otherCheckboxes.forEach(checkbox => {
                checkbox.disabled = false;  // Enable them
            });
        } else {
            // If 4 Ps is not selected, uncheck all other checkboxes and enable them
            otherCheckboxes.forEach(checkbox => {
                checkbox.checked = false; // Uncheck them
                checkbox.disabled = false; // Enable them
            });
        }
    });

    // Add event listeners to other checkboxes
    otherCheckboxes.forEach(checkbox => {
        checkbox.addEventListener("change", () => {
            if (checkbox.checked) {
                // Uncheck all other checkboxes if one of them is checked
                otherCheckboxes.forEach(other => {
                    if (other !== checkbox) {
                        other.checked = false;
                    }
                });
            }
        });
    });
});

 
document.addEventListener("DOMContentLoaded", function () {
  /**
   * Enables or disables a text input field
   * based on the selected radio button value.
   *
   * @param {string} radioName - Name attribute of the radio group
   * @param {string} inputId - ID of the text input to enable/disable
   */
  function setupRadioControl(radioName, inputId) {
    const radios = document.querySelectorAll(`input[name="${radioName}"]`);
    const textInput = document.getElementById(inputId);

    radios.forEach(radio => {
      radio.addEventListener("change", function () {
        if (this.value === "True") {
          textInput.disabled = false;
          textInput.focus();
        } else {
          textInput.disabled = true;
          textInput.value = ""; // Clear text when disabled
        }
      });
    });
  }

  // Initialize both sections
  setupRadioControl("is_sped", "additional-info"); 
  setupRadioControl("is_working_student", "additional-info-working");
});
