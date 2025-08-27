document.addEventListener("DOMContentLoaded", () => {
    // ===== Student photo upload =====
    const studentFileInput = document.getElementById("photo-upload");
    const studentPhotoPreview = document.getElementById("photo-preview");
    const studentUploadIcon = document.querySelector(".upload-icon-container");

    if (studentFileInput) {
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
    }

    // ===== Parent photo upload =====
    const parentFileInput = document.getElementById("parent-photo-upload");
    const parentPhotoPreview = document.getElementById("parent-photo-preview");
    const parentUploadIcon = document.querySelector(".upload-area .upload-icon-container");

    if (parentFileInput) {
        parentFileInput.addEventListener("change", (event) => {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    parentPhotoPreview.src = e.target.result;
                    parentPhotoPreview.style.display = "block";
                    if (parentUploadIcon) parentUploadIcon.style.display = "none";
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // ===== Checkbox logic for enrollment status =====
    const checkboxes = document.querySelectorAll(".option");
    const fourPsCheckbox = document.getElementById("fourPs");

    if (checkboxes.length && fourPsCheckbox) {
        checkboxes.forEach((checkbox) => {
            checkbox.addEventListener("change", () => {
                const checked = Array.from(checkboxes).filter((i) => i.checked);

                if (fourPsCheckbox.checked) {
                    if (checked.length > 2) checkbox.checked = false;
                } else {
                    if (checked.length > 1) checkbox.checked = false;
                }

                if (!fourPsCheckbox.checked && checked.length > 1) {
                    checkbox.checked = false;
                }
            });
        });
    }

    // ===== ToggleInput for SPED and Working Student =====
    function toggleInput(inputId, radioGroupName) {
        const input = document.getElementById(inputId);
        const selected = document.querySelector(`input[name="${radioGroupName}"]:checked`);
        if (input) {
            if (selected && selected.value === "yes") {
                input.disabled = false;
                input.focus();
            } else {
                input.disabled = true;
                input.value = "";
            }
        }
    }

    // Hook up events for SPED
    const spedRadios = document.querySelectorAll('input[name="sped"]');
    spedRadios.forEach((radio) => {
        radio.addEventListener("change", () => toggleInput("additional-info", "sped"));
    });

    // Hook up events for Working Student
    const workingRadios = document.querySelectorAll('input[name="working"]');
    workingRadios.forEach((radio) => {
        radio.addEventListener("change", () => toggleInput("additional-info-working", "working"));
    });

    // ===== Academic form: calculate average, file upload, validation =====
    const subjectInputs = document.querySelectorAll(".subjects-grid input[type='number']");
    const overallAverageInput = document.getElementById("overallAverage");

    function calculateAverage() {
        let total = 0, count = 0;
        subjectInputs.forEach((input) => {
            const value = parseFloat(input.value);
            if (!isNaN(value) && value > 0) {
                total += value;
                count++;
            }
        });
        overallAverageInput.value = count > 0 ? (total / count).toFixed(2) : "";
    }

    if (subjectInputs.length && overallAverageInput) {
        subjectInputs.forEach((input) => input.addEventListener("input", calculateAverage));
    }

    // File upload for report card
    const fileInput = document.getElementById("reportCard");
    const fileButton = document.querySelector(".file-button");
    const fileName = document.querySelector(".file-name");

    if (fileInput && fileButton && fileName) {
        fileButton.addEventListener("click", () => fileInput.click());
        fileInput.addEventListener("change", function () {
            fileName.textContent = this.files.length > 0 ? this.files[0].name : "No file chosen";
        });
    }

    // Academic form submission
    const academicForm = document.getElementById("academicForm2");
    if (academicForm) {
        academicForm.addEventListener("submit", function (e) {
            e.preventDefault();
            let isValid = true;
            const requiredFields = this.querySelectorAll("[required]");

            requiredFields.forEach((field) => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = "#c00";
                } else {
                    field.style.borderColor = "";
                }
            });

            if (isValid) {
                const redirectUrl = "{% url 'student_academic_2' %}";
                window.location.href = redirectUrl;
            } else {
                alert("Please fill in all required fields.");
            }
        });
    }
});

