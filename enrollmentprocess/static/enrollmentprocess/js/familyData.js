document.addEventListener("DOMContentLoaded", () => {
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
});
