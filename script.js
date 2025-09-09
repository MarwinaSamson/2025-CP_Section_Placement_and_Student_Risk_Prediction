// script.js FOR ADVISER LANDING PAGE

// Sidebar toggle for mobile
const sidebar = document.querySelector(".sidebar");
const toggleBtn = document.createElement("button");
toggleBtn.innerHTML = "☰";
toggleBtn.classList.add("toggle-btn");
document.body.appendChild(toggleBtn);

toggleBtn.addEventListener("click", () => {
  sidebar.classList.toggle("open");
});

// Student category view with smooth expand/collapse
const viewBtns = document.querySelectorAll(".view-btn");
const studentView = document.getElementById("student-view");
const studentContent = studentView.querySelector(".student-content");
const placeholder = studentView.querySelector(".placeholder");

const studentData = {
  "probation": `
    <table>
      <thead>
        <tr>
          <th>#</th><th>Learner</th><th>Gender</th><th>Status</th><th>Subject at Risk</th><th>Grade</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>1</td>
          <td>Uchiha, Itachi A</td>
          <td>M</td>
          <td><span class="status-badge probation">On Probation</span></td>
          <td>Filipino</td>
          <td>81</td>
        </tr>
      </tbody>
    </table>
  `,
  "transfer-in": `<p>No students found.</p>`,
  "balik-aral": `<p>No students found.</p>`,
  "repeater": `<p>No students found.</p>`
};

viewBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    const category = btn.dataset.category;
    studentContent.innerHTML = studentData[category] || `<p>No data available.</p>`;
    placeholder.style.display = "none";

    // expand with animation
    studentContent.classList.add("open");
  });
});


// script.js FOR MASTERLIST PAGE

// Search Function - WONT FUNCTION HERE ONLY IN THE HTML FILE :(
    // document.getElementById("search").addEventListener("keyup", function() {
    //   const filter = this.value.toLowerCase();
    //   const rows = document.querySelectorAll("#masterlist tbody tr");
    //   rows.forEach(row => {
    //     row.style.display = row.innerText.toLowerCase().includes(filter) ? "" : "none";
    //   });
    // });

    // Export Functions
    function exportExcel() {
      const table = document.getElementById("masterlist");
      const wb = XLSX.utils.table_to_book(table, { sheet: "Masterlist" });
      XLSX.writeFile(wb, "Masterlist.xlsx");
    }

    function exportCSV() {
      const table = document.getElementById("masterlist");
      const wb = XLSX.utils.table_to_book(table, { sheet: "Masterlist" });
      XLSX.writeFile(wb, "Masterlist.csv");
    }

    function exportPDF() {
      const { jsPDF } = window.jspdf;
      const doc = new jsPDF();
      doc.text("Akatsuki Masterlist", 14, 16);
      doc.autoTable({ html: "#masterlist", startY: 20 });
      doc.save("Masterlist.pdf");
    }

      



// script.js FOR LEARNER PROFILE PAGE
  /**
         * Toggles a section between view and edit modes.
         * @param {string} section - The name of the section (e.g., 'student', 'parents').
         * @param {boolean} isEditing - True to switch to edit mode, false for view mode.
         */
        function toggleEditState(section, isEditing) {
            const viewContainer = document.getElementById(`${section}-view`);
            const formContainer = document.getElementById(`${section}-form`);
            const updateButton = document.querySelector(`#${section}-section .update-btn`);

            if (isEditing) {
                // --- Switch to Edit Mode ---
                const viewSpans = viewContainer.querySelectorAll('span[data-key]');
                viewSpans.forEach(span => {
                    const key = span.dataset.key;
                    const input = formContainer.querySelector(`[name="${key}"]`);
                    if (input) {
                        input.value = span.textContent;
                    }
                });
                
                viewContainer.classList.add('hidden');
                formContainer.classList.remove('hidden');
                updateButton.classList.add('hidden');
            } else {
                // --- Switch to View Mode ---
                formContainer.classList.add('hidden');
                viewContainer.classList.remove('hidden');
                updateButton.classList.remove('hidden');
            }
        }

      


        /**
         * Initiates the edit mode for a specific section.
         */
        function enableEdit(section) {
            toggleEditState(section, true);
        }

        /**
         * Cancels the edit mode and reverts to view mode without saving.
         */
        function cancelEdit(section) {
            toggleEditState(section, false);
        }

        /**
         * Handles the form submission.
         */
        function saveData(event, section) {
            event.preventDefault(); 

            const form = document.getElementById(`${section}-form`);
            const viewContainer = document.getElementById(`${section}-view`);
            const formData = new FormData(form);

            console.log(`Saving data for ${section}:`, Object.fromEntries(formData));

            // Update the view spans with the new values from the form
            formData.forEach((value, key) => {
                const span = viewContainer.querySelector(`span[data-key="${key}"]`);
                if (span) {
                    span.textContent = value;
                }
            });
            
            toggleEditState(section, false);
            showToast('Profile updated successfully!');
        }

        /**
         * Displays a toast notification message.
         */
        function showToast(message) {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
            }, 3000);
        }