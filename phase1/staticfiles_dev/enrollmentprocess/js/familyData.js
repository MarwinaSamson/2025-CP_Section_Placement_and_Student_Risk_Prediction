console.log("familyData.js is loaded!")

document.addEventListener("DOMContentLoaded", () => {
  /*** AGE CALCULATION FROM BIRTHDATE ***/
  function calculateAge(birthDate) {
    const today = new Date()
    let age = today.getFullYear() - birthDate.getFullYear()
    const monthDiff = today.getMonth() - birthDate.getMonth()

    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
      age--
    }

    return age
  }

  const fatherDobInput = document.getElementById("id_father_dob")
  const fatherAgeDisplay = document.getElementById("father-age-display")

  if (fatherDobInput && fatherAgeDisplay) {
    fatherDobInput.addEventListener("change", function () {
      if (this.value) {
        const birthDate = new Date(this.value)
        const age = calculateAge(birthDate)
        fatherAgeDisplay.textContent = `Age: ${age}`

        // Hide validation message when filled
        const validation = document.getElementById("father-dob-validation")
        if (validation) {
          validation.style.display = "none"
        }
        this.classList.remove("field-error")
      } else {
        fatherAgeDisplay.textContent = "Age: --"
      }
    })

    // Calculate age on page load if birthdate exists
    if (fatherDobInput.value) {
      fatherDobInput.dispatchEvent(new Event("change"))
    }
  }

  const motherDobInput = document.getElementById("id_mother_dob")
  const motherAgeDisplay = document.getElementById("mother-age-display")

  if (motherDobInput && motherAgeDisplay) {
    motherDobInput.addEventListener("change", function () {
      if (this.value) {
        const birthDate = new Date(this.value)
        const age = calculateAge(birthDate)
        motherAgeDisplay.textContent = `Age: ${age}`

        // Hide validation message when filled
        const validation = document.getElementById("mother-dob-validation")
        if (validation) {
          validation.style.display = "none"
        }
        this.classList.remove("field-error")
      } else {
        motherAgeDisplay.textContent = "Age: --"
      }
    })

    // Calculate age on page load if birthdate exists
    if (motherDobInput.value) {
      motherDobInput.dispatchEvent(new Event("change"))
    }
  }

  const guardianDobInput = document.getElementById("id_guardian_dob")
  const guardianAgeDisplay = document.getElementById("guardian-age-display")

  if (guardianDobInput && guardianAgeDisplay) {
    guardianDobInput.addEventListener("change", function () {
      if (this.value) {
        const birthDate = new Date(this.value)
        const age = calculateAge(birthDate)
        guardianAgeDisplay.textContent = `Age: ${age}`
      } else {
        guardianAgeDisplay.textContent = "Age: --"
      }
    })

    // Calculate age on page load if birthdate exists
    if (guardianDobInput.value) {
      guardianDobInput.dispatchEvent(new Event("change"))
    }
  }

  /*** PARENT PHOTO PREVIEW & VALIDATION ***/
  const parentFileInput = document.getElementById("id_parent_photo")
  const parentPhotoPreview = document.getElementById("parent-photo-preview")
  const parentUploadIcon = document.querySelector(".upload-area .upload-icon-container")
  const parentPhotoValidation = document.getElementById("parent-photo-validation")
  const parentUploadAreaLabel = document.getElementById("parent-upload-area-label")

  // In familyData.js - Update the parent photo preview section
if (parentFileInput) {
    console.log("Parent photo upload input detected.");

    parentFileInput.removeAttribute("required");

    parentFileInput.addEventListener("change", (event) => {
        const file = event.target.files[0];

        if (file) {
            if (parentPhotoValidation) {
                parentPhotoValidation.style.display = "none";
            }
            if (parentUploadAreaLabel) {
                parentUploadAreaLabel.classList.remove("has-error");
            }

            // Preview logic
            if (file.type.startsWith("image/")) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    if (parentPhotoPreview) {
                        parentPhotoPreview.src = e.target.result;
                        parentPhotoPreview.style.display = "block";
                        parentUploadAreaLabel.classList.add("has-preview");
                    }
                    if (parentUploadIcon) {
                        parentUploadIcon.style.display = "none";
                    }
                };
                reader.readAsDataURL(file);
            } else {
                alert("Please select a valid image file (JPG, PNG, etc.).");
                parentFileInput.value = ""; // reset input
                if (parentPhotoPreview) {
                    parentPhotoPreview.style.display = "none";
                    parentUploadAreaLabel.classList.remove("has-preview");
                }
                if (parentUploadIcon) {
                    parentUploadIcon.style.display = "flex";
                }
            }
        }
    });
}

  /*** REAL-TIME FIELD VALIDATION ***/

  // Helper function to add validation listeners
  function addValidationListener(inputId, validationId) {
    const input = document.getElementById(inputId)
    const validation = document.getElementById(validationId)

    if (input && validation) {
      input.addEventListener("input", function () {
        if (this.value.trim() !== "") {
          validation.style.display = "none"
          this.classList.remove("field-error")
        }
      })

      input.addEventListener("blur", function () {
        if (this.value.trim() === "" && this.hasAttribute("required")) {
          validation.style.display = "block"
          this.classList.add("field-error")
        }
      })
    }
  }

  // Father's fields
  addValidationListener("id_father_occupation", "father-occupation-validation")
  addValidationListener("id_father_contact_number", "father-contact-validation")

  // Mother's fields
  addValidationListener("id_mother_occupation", "mother-occupation-validation")
  addValidationListener("id_mother_contact_number", "mother-contact-validation")

  // Email validation with pattern check
  function addEmailValidation(inputId, validationId) {
    const input = document.getElementById(inputId)
    const validation = document.getElementById(validationId)

    if (input && validation) {
      input.addEventListener("blur", function () {
        if (this.value.trim() !== "") {
          const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
          if (!emailPattern.test(this.value)) {
            validation.style.display = "block"
            this.classList.add("field-error")
          } else {
            validation.style.display = "none"
            this.classList.remove("field-error")
          }
        }
      })

      input.addEventListener("input", function () {
        if (this.value.trim() === "") {
          validation.style.display = "none"
          this.classList.remove("field-error")
        }
      })
    }
  }

  addEmailValidation("id_father_email", "father-email-validation")
  addEmailValidation("id_mother_email", "mother-email-validation")

  /*** FORM VALIDATION BEFORE SUBMISSION ***/
  const form = document.getElementById("familyDataForm")

  if (form) {
    form.addEventListener("submit", (event) => {
      let isValid = true
      let firstError = null

      if (parentFileInput && (!parentFileInput.files || parentFileInput.files.length === 0)) {
        if (parentPhotoValidation) {
          parentPhotoValidation.style.display = "block"
          if (!firstError) firstError = parentPhotoValidation
        }
        if (parentUploadAreaLabel) {
          parentUploadAreaLabel.classList.add("has-error")
        }
        isValid = false
      }

      const fatherFields = [
        { id: "id_father_family_name", validation: "father-name-validation", name: "Father's Last Name" },
        { id: "id_father_first_name", validation: "father-name-validation", name: "Father's First Name" },
        { id: "id_father_dob", validation: "father-dob-validation", name: "Father's Date of Birth" },
        { id: "id_father_occupation", validation: "father-occupation-validation", name: "Father's Occupation" },
        { id: "id_father_contact_number", validation: "father-contact-validation", name: "Father's Contact Number" },
      ]

      fatherFields.forEach((field) => {
        const input = document.getElementById(field.id)
        const validation = document.getElementById(field.validation)

        if (input && (!input.value || input.value.trim() === "")) {
          if (validation) {
            validation.style.display = "block"
            if (!firstError) firstError = validation
          }
          input.classList.add("field-error")
          isValid = false
        }
      })

      const motherFields = [
        { id: "id_mother_family_name", validation: "mother-name-validation", name: "Mother's Last Name" },
        { id: "id_mother_first_name", validation: "mother-name-validation", name: "Mother's First Name" },
        { id: "id_mother_dob", validation: "mother-dob-validation", name: "Mother's Date of Birth" },
        { id: "id_mother_occupation", validation: "mother-occupation-validation", name: "Mother's Occupation" },
        { id: "id_mother_contact_number", validation: "mother-contact-validation", name: "Mother's Contact Number" },
      ]

      motherFields.forEach((field) => {
        const input = document.getElementById(field.id)
        const validation = document.getElementById(field.validation)

        if (input && (!input.value || input.value.trim() === "")) {
          if (validation) {
            validation.style.display = "block"
            if (!firstError) firstError = validation
          }
          input.classList.add("field-error")
          isValid = false
        }
      })

      const fatherEmail = document.getElementById("id_father_email")
      const motherEmail = document.getElementById("id_mother_email")
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

      if (fatherEmail && fatherEmail.value.trim() !== "" && !emailPattern.test(fatherEmail.value)) {
        const validation = document.getElementById("father-email-validation")
        if (validation) {
          validation.style.display = "block"
          if (!firstError) firstError = validation
        }
        fatherEmail.classList.add("field-error")
        isValid = false
      }

      if (motherEmail && motherEmail.value.trim() !== "" && !emailPattern.test(motherEmail.value)) {
        const validation = document.getElementById("mother-email-validation")
        if (validation) {
          validation.style.display = "block"
          if (!firstError) firstError = validation
        }
        motherEmail.classList.add("field-error")
        isValid = false
      }

      if (!isValid) {
        event.preventDefault()

        if (firstError) {
          firstError.scrollIntoView({ behavior: "smooth", block: "center" })
        }

        
      }
    })
  }
}) // DOMContentLoaded ends here