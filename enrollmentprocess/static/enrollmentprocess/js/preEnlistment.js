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

  if (studentFileInput) {
    console.log("Photo upload input detected.");
    studentFileInput.addEventListener("change", (event) => {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          studentPhotoPreview.src = e.target.result;
          studentPhotoPreview.style.display = "block";
          studentUploadIcon.style.display = "none";
        };
        reader.readAsDataURL(file);
      }
    });
  } else {
    console.warn("Photo upload input NOT found!");
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
      if (this.value === "True") {  // Changed from "True" or "yes" to "1"
        inputField.disabled = false;
        inputField.focus(); // 🔥 auto-highlight when enabled
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

const lrnInput = document.getElementById("id_lrn");
        if (lrnInput) {
            lrnInput.setAttribute("maxlength", "12");
            lrnInput.setAttribute("pattern", "\\d{12}");
            lrnInput.setAttribute("title", "LRN must be exactly 12 digits.");
        }

}); // ✅ closes only once


