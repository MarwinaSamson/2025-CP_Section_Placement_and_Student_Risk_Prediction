document.addEventListener("DOMContentLoaded", () => {
  // Existing code for student photo upload
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

  // New code for parent photo upload
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
