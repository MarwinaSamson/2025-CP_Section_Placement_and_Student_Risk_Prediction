// document.addEventListener("DOMContentLoaded", () => {
//   // Initialize search functionality
//   initializeSearch()

//   // Initialize export functionality
//   initializeExportButtons()
// })

// // Sample teacher data
// const teachersData = {
//   1: {
//     employeeId: "1234567890",
//     lastName: "Ackerman",
//     firstName: "Mikasa",
//     middleName: "Armin",
//     gender: "Female",
//     dateOfBirth: "June 30, 2000",
//     age: "25",
//     position: "Teacher - I",
//     department: "Science",
//     email: "mikasa.ackerman@deped.gov.ph",
//     phone: "+63 912 345 6789",
//     address: "Eden",
//     photo: "../assets/sakamaru.webp",
//     teachingLoad: [
//       { subject: "Physics", gradeSection: "Grade 9 - St. Anne", students: 45 },
//       { subject: "Science", gradeSection: "Grade 8 - St. John", students: 50 },
//       { subject: "Science", gradeSection: "Grade 8 - St. John", students: 50 },
//     ],
//     changeHistory: [
//       { action: "Record Created", date: "07/09/2025", time: "10:30 pm" },
//       { action: "Updated Profile", date: "07/09/2025", time: "10:30 pm" },
//     ],
//   },
//   2: {
//     employeeId: "0987654321",
//     lastName: "Hatake",
//     firstName: "Kakashi",
//     middleName: "Sensei",
//     gender: "Male",
//     dateOfBirth: "September 15, 1985",
//     age: "39",
//     position: "Teacher - II",
//     department: "Mathematics",
//     email: "kakashi.hatake@deped.gov.ph",
//     phone: "+63 912 345 6788",
//     address: "Konoha Village",
//     photo: "../assets/kakashi.webp",
//     teachingLoad: [
//       { subject: "Mathematics", gradeSection: "Grade 10 - Akatsuki", students: 40 },
//       { subject: "Algebra", gradeSection: "Grade 9 - Phantom", students: 38 },
//     ],
//     changeHistory: [
//       { action: "Record Created", date: "06/15/2025", time: "09:15 am" },
//       { action: "Updated Contact", date: "07/01/2025", time: "02:30 pm" },
//     ],
//   },
// }

// function initializeExportButtons() {
//   const exportPdfBtn = document.getElementById("exportPdf")
//   const exportExcelBtn = document.getElementById("exportExcel")

//   if (exportPdfBtn) {
//     exportPdfBtn.addEventListener("click", exportToPdf)
//   }

//   if (exportExcelBtn) {
//     exportExcelBtn.addEventListener("click", exportToExcel)
//   }
// }

// function exportToPdf() {
//   const { jsPDF } = window.jspdf
//   const doc = new jsPDF()
//   const table = document.getElementById("teachersTable")

//   // Add title
//   doc.setFontSize(18)
//   doc.text("ZNHS West - Teachers List", 14, 20)

//   // Add date
//   doc.setFontSize(10)
//   doc.text(`Generated on: ${new Date().toLocaleDateString()}`, 14, 30)

//   // Get table data
//   const headers = [["Full Name", "Sex", "Age", "Position"]]
//   const data = Array.from(table.querySelectorAll("tbody tr")).map((row) => {
//     const cells = row.querySelectorAll("td")
//     return [
//       cells[0].textContent.trim(),
//       cells[1].textContent.trim(),
//       cells[2].textContent.trim(),
//       cells[3].textContent.trim(),
//     ]
//   })

//   // Generate table
//   doc.autoTable({
//     head: headers,
//     body: data,
//     startY: 40,
//     theme: "grid",
//     headStyles: {
//       fillColor: [196, 30, 58], // School red color
//       textColor: 255,
//       fontStyle: "bold",
//     },
//     styles: {
//       fontSize: 10,
//       cellPadding: 5,
//     },
//   })

//   // Save the PDF
//   doc.save("ZNHS-West-Teachers-List.pdf")
//   console.log("PDF exported successfully")
// }

// function exportToExcel() {
//   const table = document.getElementById("teachersTable")

//   // Create workbook
//   const wb = window.XLSX.utils.book_new()

//   // Convert table to worksheet, excluding the Profile column
//   const tableClone = table.cloneNode(true)

//   // Remove the Profile column (last column) from header and all rows
//   const headerRow = tableClone.querySelector("thead tr")
//   const profileHeaderCell = headerRow.querySelector("th:last-child")
//   if (profileHeaderCell) profileHeaderCell.remove()

//   const bodyRows = tableClone.querySelectorAll("tbody tr")
//   bodyRows.forEach((row) => {
//     const profileCell = row.querySelector("td:last-child")
//     if (profileCell) profileCell.remove()
//   })

//   const ws = window.XLSX.utils.table_to_sheet(tableClone)

//   // Set column widths
//   ws["!cols"] = [
//     { width: 25 }, // Full Name
//     { width: 8 }, // Sex
//     { width: 8 }, // Age
//     { width: 20 }, // Position
//   ]

//   // Add worksheet to workbook
//   window.XLSX.utils.book_append_sheet(wb, ws, "Teachers List")

//   // Save the Excel file
//   window.XLSX.writeFile(wb, "ZNHS-West-Teachers-List.xlsx")
// }

// function viewTeacherProfile(teacherId) {
//   const teacher = teachersData[teacherId] || teachersData[1] // Fallback to first teacher
//   const modal = document.getElementById("teacherProfileModal")

//   // Populate teacher data
//   document.getElementById("employeeId").textContent = teacher.employeeId
//   document.getElementById("lastName").textContent = teacher.lastName
//   document.getElementById("firstName").textContent = teacher.firstName
//   document.getElementById("middleName").textContent = teacher.middleName
//   document.getElementById("gender").textContent = teacher.gender
//   document.getElementById("dateOfBirth").textContent = teacher.dateOfBirth
//   document.getElementById("age").textContent = teacher.age
//   document.getElementById("position").textContent = teacher.position
//   document.getElementById("department").textContent = teacher.department
//   document.getElementById("email").textContent = teacher.email
//   document.getElementById("phone").textContent = teacher.phone
//   document.getElementById("address").textContent = teacher.address
//   document.getElementById("teacherPhoto").src = teacher.photo

//   // Populate teaching load
//   const teachingLoadBody = document.getElementById("teachingLoadBody")
//   teachingLoadBody.innerHTML = ""
//   teacher.teachingLoad.forEach((load) => {
//     const row = document.createElement("tr")
//     row.innerHTML = `
//             <td>${load.subject}</td>
//             <td>${load.gradeSection}</td>
//             <td>${load.students}</td>
//         `
//     teachingLoadBody.appendChild(row)
//   })

//   // Populate change history
//   const changeHistoryBody = document.getElementById("changeHistoryBody")
//   changeHistoryBody.innerHTML = ""
//   teacher.changeHistory.forEach((change) => {
//     const row = document.createElement("tr")
//     row.innerHTML = `
//             <td>${change.action}</td>
//             <td>${change.date}</td>
//             <td>${change.time}</td>
//         `
//     changeHistoryBody.appendChild(row)
//   })

//   // Show modal
//   modal.style.display = "block"

//   console.log(`Viewing profile for teacher ID: ${teacherId}`)
// }

// function closeTeacherProfile() {
//   const modal = document.getElementById("teacherProfileModal")
//   modal.style.display = "none"
// }

// // Close modal when clicking outside
// window.addEventListener("click", (event) => {
//   const modal = document.getElementById("teacherProfileModal")
//   if (event.target === modal) {
//     closeTeacherProfile()
//   }
// })

// function initializeSearch() {
//   const searchInput = document.getElementById("teacherSearch")
//   const tableRows = document.querySelectorAll(".teacher-row")

//   searchInput.addEventListener("input", function () {
//     const searchTerm = this.value.toLowerCase()

//     tableRows.forEach((row) => {
//       const teacherName = row.cells[0].textContent.toLowerCase()
//       const position = row.cells[3].textContent.toLowerCase()

//       if (teacherName.includes(searchTerm) || position.includes(searchTerm)) {
//         row.style.display = ""
//       } else {
//         row.style.display = "none"
//       }
//     })
//   })
// }


// function setupLogoutHandler() {
//   const logoutBtn = document.querySelector(".logout-btn")
//   if (logoutBtn) {
//     logoutBtn.addEventListener("click", (e) => {
//       e.preventDefault()
//       handleLogout()
//     })
//   }
// }

// function handleLogout() {
//   // Clear all session data
//   localStorage.removeItem("isLoggedIn")
//   localStorage.removeItem("username")
//   localStorage.removeItem("loginTime")

//   // Show notification and redirect
//   showNotification("Logging out...", "info")

//   setTimeout(() => {
//     window.location.href = "logout.html"
//   }, 1000)
// }

// function showNotification(message, type) {
//   const container = document.getElementById("notificationContainer")

//   if (!container) return

//   // Create the notification element
//   const notification = document.createElement("div")
//   notification.className = `notification ${type}`
//   notification.innerHTML = `
//           <span>${message}</span>
//           <button class="notification-close">&times;</button>
//       `

//   // Add a click event to the close button
//   notification.querySelector(".notification-close").addEventListener("click", () => {
//     notification.remove()
//   })

//   // Append to the container
//   container.appendChild(notification)

//   // Automatically remove the notification after 4 seconds
//   setTimeout(() => {
//     if (container.contains(notification)) {
//       notification.remove()
//     }
//   }, 4000)
// }

// Teachers Management JavaScript

// Teachers Management JavaScript

// Global teachers data
let teachersData = [];

document.addEventListener("DOMContentLoaded", function() {
    console.log('Initializing teachers functionality...');
    
    // Load teachers data
    const teachersDataElement = document.getElementById('teachers-data');
    if (teachersDataElement) {
        teachersData = JSON.parse(teachersDataElement.textContent);
        console.log('Teachers data loaded:', teachersData);
    } else {
        console.error('Teachers data element not found');
        teachersData = [];
    }
    
    // Initialize all functionality
    initializeSearch();
    initializeExportButtons();
    
    // Add click outside modal handler
    window.addEventListener("click", function(event) {
        const modal = document.getElementById("teacherProfileModal");
        if (event.target === modal) {
            closeTeacherProfile();
        }
    });
});

// View teacher profile
function viewTeacherProfile(teacherId) {
    console.log('Opening profile for teacher ID:', teacherId);
    console.log('Available teachers data:', teachersData);
    
    if (!teachersData || !Array.isArray(teachersData)) {
        console.error('Teachers data not available');
        alert('Teacher data not loaded. Please refresh the page.');
        return;
    }

    // Convert teacherId to number for comparison
    const id = parseInt(teacherId);
    console.log('Looking for teacher with ID:', id);
    
    const teacher = teachersData.find(t => {
        console.log('Checking teacher:', t.id, 'type:', typeof t.id, 'looking for:', id, 'type:', typeof id);
        return t.id === id;
    });
    
    console.log('Found teacher:', teacher);
    
    if (teacher) {
        console.log('Teacher found, populating modal...');
        populateTeacherModal(teacher);
        showModal();
    } else {
        console.error('Teacher not found. Available IDs:', teachersData.map(t => t.id));
        alert('Teacher not found. Available IDs: ' + teachersData.map(t => t.id).join(', '));
    }
}

// Populate modal with teacher data
function populateTeacherModal(teacher) {
    console.log('Populating modal with teacher data:', teacher);
    
    // Teacher Basic Info Section
    const fullName = `${teacher.firstName || ''} ${teacher.middleName || ''} ${teacher.lastName || ''}`.trim();
    document.getElementById('teacherFullName').textContent = fullName || 'Not provided';
    document.getElementById('teacherPosition').textContent = teacher.position || 'Not provided';
    document.getElementById('teacherDepartment').textContent = teacher.department || 'Not provided';
    
    // Basic Details
    document.getElementById('employeeId').textContent = teacher.employeeId || 'Not provided';
    document.getElementById('gender').textContent = teacher.sex || 'Not provided';
    document.getElementById('age').textContent = teacher.age || 'Not provided';
    document.getElementById('dateOfBirth').textContent = teacher.dateOfBirth || 'Not provided';
    
    // Personal Details
    document.getElementById('lastName').textContent = teacher.lastName || 'Not provided';
    document.getElementById('firstName').textContent = teacher.firstName || 'Not provided';
    document.getElementById('middleName').textContent = teacher.middleName || 'Not provided';
    
    // Contact Information
    document.getElementById('email').textContent = teacher.email || 'Not provided';
    document.getElementById('phone').textContent = teacher.phone || 'Not provided';
    document.getElementById('address').textContent = teacher.address || 'Not provided';
    
    // Teacher Photo
    if (teacher.photo) {
        document.getElementById('teacherPhoto').src = teacher.photo;
    }
    
    console.log('Modal populated successfully');
}

// Show modal
function showModal() {
    const modal = document.getElementById('teacherProfileModal');
    if (modal) {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }
}

// Close teacher profile modal
function closeTeacherProfile() {
    const modal = document.getElementById('teacherProfileModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto'; // Restore scrolling
    }
}

// Initialize search functionality
function initializeSearch() {
    const searchInput = document.getElementById('teacherSearch');
    if (!searchInput) return;

    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        const tableRows = document.querySelectorAll('.teacher-row');
        
        tableRows.forEach(row => {
            const cells = row.querySelectorAll('td');
            let matches = false;
            
            // Search through all cells except the last one (button)
            for (let i = 0; i < cells.length - 1; i++) {
                if (cells[i].textContent.toLowerCase().includes(searchTerm)) {
                    matches = true;
                    break;
                }
            }
            
            row.style.display = matches ? '' : 'none';
        });
    });
}

// Initialize export buttons
function initializeExportButtons() {
    // PDF Export
    const exportPdfBtn = document.getElementById('exportPdf');
    if (exportPdfBtn) {
        exportPdfBtn.addEventListener('click', exportToPdf);
    }
    
    // Excel Export
    const exportExcelBtn = document.getElementById('exportExcel');
    if (exportExcelBtn) {
        exportExcelBtn.addEventListener('click', exportToExcel);
    }
}

// Export to PDF
function exportToPdf() {
    try {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        const table = document.getElementById('teachersTable');
        
        // Add title
        doc.setFontSize(18);
        doc.text('ZNHS West - Teachers List', 14, 20);
        
        // Add date
        doc.setFontSize(10);
        doc.text(`Generated on: ${new Date().toLocaleDateString()}`, 14, 30);
        
        // Generate table
        doc.autoTable({
            html: table,
            startY: 40,
            theme: 'grid',
            headStyles: {
                fillColor: [196, 30, 58], // School red color
                textColor: 255,
                fontStyle: 'bold',
            },
            styles: {
                fontSize: 10,
                cellPadding: 5,
            },
        });
        
        // Save the PDF
        doc.save('ZNHS-West-Teachers-List.pdf');
        console.log('PDF exported successfully');
    } catch (error) {
        console.error('Error exporting PDF:', error);
        alert('Error exporting PDF. Please try again.');
    }
}

// Export to Excel
function exportToExcel() {
    try {
        const table = document.getElementById('teachersTable');
        if (!table) {
            throw new Error('Table not found');
        }
        
        const wb = XLSX.utils.book_new();
        const ws = XLSX.utils.table_to_sheet(table);
        
        XLSX.utils.book_append_sheet(wb, ws, 'Teachers List');
        XLSX.writeFile(wb, 'ZNHS-West-Teachers-List.xlsx');
        console.log('Excel exported successfully');
    } catch (error) {
        console.error('Error exporting Excel:', error);
        alert('Error exporting Excel. Please try again.');
    }
}

// Logout handler
function handleLogout() {
    if (confirm('Are you sure you want to logout?')) {
        // Clear any session data if needed
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('username');
        
        // Redirect to logout URL
        window.location.href = "{% url 'enrollmentprocess:logout' %}";
    }
}