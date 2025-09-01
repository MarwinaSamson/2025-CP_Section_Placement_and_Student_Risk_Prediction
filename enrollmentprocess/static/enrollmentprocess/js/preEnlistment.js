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


// StudentAcademic.html

// document.addEventListener('DOMContentLoaded', function () {
//             const subjectInputs = document.querySelectorAll('.subjects-grid input[type="number"]');
//             const overallAverageInput = document.getElementById('overallAverage');

//             function calculateAverage() {
//                 let total = 0;
//                 let count = 0;

//                 subjectInputs.forEach(input => {
//                     const value = parseFloat(input.value);
//                     if (!isNaN(value) && value > 0) {
//                         total += value;
//                         count++;
//                     }
//                 });

//                 if (count > 0) {
//                     const average = (total / count).toFixed(2);
//                     overallAverageInput.value = average;
//                 } else {
//                     overallAverageInput.value = '';
//                 }
//             }

//             subjectInputs.forEach(input => {
//                 input.addEventListener('input', calculateAverage);
//             });

//             const fileInputs = document.querySelectorAll('input[type="file"]');

//             fileInputs.forEach(fileInput => {
//                 const fileButton = fileInput.parentElement.querySelector('.file-button');
//                 const fileName = fileInput.parentElement.querySelector('.file-name');

//                 fileButton.addEventListener('click', () => {
//                     fileInput.click();
//                 });

//                 fileInput.addEventListener('change', function () {
//                     if (this.files.length > 0) {
//                         fileName.textContent = this.files[0].name;
//                     } else {
//                         fileName.textContent = 'No file chosen';
//                     }
//                 });
//             });

//             const dostExamSelect = document.getElementById('dostExam');
//             const dostProofGroup = document.getElementById('dostProofGroup');
//             const dostProofInput = document.getElementById('dostProof');

//             dostExamSelect.addEventListener('change', function () {
//                 if (this.value === 'passed') {
//                     dostProofGroup.style.display = 'block';
//                     dostProofInput.required = true;
//                 } else {
//                     dostProofGroup.style.display = 'none';
//                     dostProofInput.required = false;
//                     dostProofInput.value = '';
//                     dostProofGroup.querySelector('.file-name').textContent = 'No file chosen';
//                 }
//             });

//             const workingStudentSelect = document.getElementById('workingStudent');
//             const workTypeGroup = document.getElementById('workTypeGroup');
//             const workTypeSelect = document.getElementById('workType');

//             workingStudentSelect.addEventListener('change', function () {
//                 if (this.value === 'yes') {
//                     workTypeGroup.style.display = 'block';
//                     workTypeSelect.required = true;
//                 } else {
//                     workTypeGroup.style.display = 'none';
//                     workTypeSelect.required = false;
//                     workTypeSelect.value = '';
//                 }
//             });

//             const disabilitySelect = document.getElementById('disability');
//             const disabilityTypeGroup = document.getElementById('disabilityTypeGroup');
//             const disabilityTypeSelect = document.getElementById('disabilityType');

//             disabilitySelect.addEventListener('change', function () {
//                 if (this.value === 'yes') {
//                     disabilityTypeGroup.style.display = 'block';
//                     disabilityTypeSelect.required = true;
//                 } else {
//                     disabilityTypeGroup.style.display = 'none';
//                     disabilityTypeSelect.required = false;
//                     disabilityTypeSelect.value = '';
//                 }
//             });
//         });
