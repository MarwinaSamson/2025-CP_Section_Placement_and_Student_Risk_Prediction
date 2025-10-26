// // Settings Page JavaScript

// // Tab Management
// document.addEventListener("DOMContentLoaded", () => {
//   // Initialize tab functionality
//   const tabBtns = document.querySelectorAll(".tab-btn")
//   const tabContents = document.querySelectorAll(".tab-content")

//   tabBtns.forEach((btn) => {
//     btn.addEventListener("click", () => {
//       const tabName = btn.getAttribute("data-tab")

//       // Remove active class from all tabs and contents
//       tabBtns.forEach((b) => b.classList.remove("active"))
//       tabContents.forEach((c) => c.classList.remove("active"))

//       // Add active class to clicked tab and corresponding content
//       btn.classList.add("active")
//       document.getElementById(`${tabName}-tab`).classList.add("active")
//     })
//   })

//   // Content Management sub-tabs
//   const contentTabBtns = document.querySelectorAll(".content-tab-btn")
//   const contentSections = document.querySelectorAll(".content-section")

//   contentTabBtns.forEach((btn) => {
//     btn.addEventListener("click", () => {
//       const contentName = btn.getAttribute("data-content")

//       // Remove active class from all content tabs and sections
//       contentTabBtns.forEach((b) => b.classList.remove("active"))
//       contentSections.forEach((s) => s.classList.remove("active"))

//       // Add active class to clicked tab and corresponding section
//       btn.classList.add("active")
//       document.getElementById(`${contentName}-content`).classList.add("active")
//     })
//   })

//   // Search functionality
//   const userSearch = document.getElementById("userSearch")
//   const historySearch = document.getElementById("historySearch")

//   if (userSearch) {
//     userSearch.addEventListener("input", function () {
//       filterUsers(this.value)
//     })
//   }

//   if (historySearch) {
//     historySearch.addEventListener("input", function () {
//       filterHistory(this.value)
//     })
//   }

//   // Close dropdowns when clicking outside
//   document.addEventListener("click", (e) => {
//     if (!e.target.closest(".actions-dropdown")) {
//       document.querySelectorAll(".dropdown-menu").forEach((menu) => {
//         menu.classList.remove("show")
//       })
//     }
//   })

//   // Form submission handler
//   const addUserForm = document.getElementById("addUserForm")
//   if (addUserForm) {
//     addUserForm.addEventListener("submit", (e) => {
//       e.preventDefault()

//       const firstName = document.getElementById("firstName").value
//       const lastName = document.getElementById("lastName").value
//       const email = document.getElementById("email").value
//       const employeeId = document.getElementById("employeeId").value
//       const position = document.getElementById("position").value
//       const department = document.getElementById("department").value
//       const tempPassword = document.getElementById("tempPassword").value

//       const permissions = Array.from(document.querySelectorAll('input[name="permissions"]:checked')).map(
//         (cb) => cb.value,
//       )

//       const userData = {
//         firstName,
//         lastName,
//         email,
//         employeeId,
//         position,
//         department,
//         permissions,
//         tempPassword,
//       }

//       console.log("Adding new user:", userData)

//       // Simulate API call
//       setTimeout(() => {
//         alert("User added successfully!")
//         closeAddUserModal()
//         // Here you would typically refresh the users table
//       }, 1000)
//     })
//   }
// })

// // Dropdown Management
// function toggleDropdown(button) {
//   const dropdown = button.nextElementSibling
//   const isOpen = dropdown.classList.contains("show")

//   // Close all dropdowns first
//   document.querySelectorAll(".dropdown-menu").forEach((menu) => {
//     menu.classList.remove("show")
//   })

//   // Toggle current dropdown with animation
//   if (!isOpen) {
//     dropdown.classList.add("show")
//     // Ensure dropdown is visible and positioned correctly
//     setTimeout(() => {
//       dropdown.style.zIndex = "1001"
//     }, 10)
//   }
// }

// // User Management Functions
// function openAddUserModal() {
//   document.getElementById("addUserModal").style.display = "block"
// }

// function closeAddUserModal() {
//   document.getElementById("addUserModal").style.display = "none"
//   document.getElementById("addUserForm").reset()
// }

// function viewProfile(userId) {
//   console.log("Opening profile for user:", userId)
//   document.getElementById("userProfileModal").style.display = "block"
//   // Close any open dropdowns
//   document.querySelectorAll(".dropdown-menu").forEach((menu) => {
//     menu.classList.remove("show")
//   })
// }

// function closeUserProfileModal() {
//   document.getElementById("userProfileModal").style.display = "none"
// }

// function editDetails(userId) {
//   console.log("Editing details for user:", userId)
//   alert(`Edit details for user: ${userId}`)
//   // Close dropdown
//   document.querySelectorAll(".dropdown-menu").forEach((menu) => {
//     menu.classList.remove("show")
//   })
// }

// function changePermission(userId) {
//   console.log("Changing permissions for user:", userId)
//   alert(`Change permissions for user: ${userId}`)
//   // Close dropdown
//   document.querySelectorAll(".dropdown-menu").forEach((menu) => {
//     menu.classList.remove("show")
//   })
// }

// function deleteUser(userId) {
//   console.log("Deleting user:", userId)
//   if (confirm(`Are you sure you want to delete user: ${userId}?`)) {
//     alert(`User ${userId} deleted successfully`)
//   }
//   // Close dropdown
//   document.querySelectorAll(".dropdown-menu").forEach((menu) => {
//     menu.classList.remove("show")
//   })
// }

// // Search and Filter Functions
// function filterUsers(searchTerm) {
//   const rows = document.querySelectorAll("#usersTableBody tr")

//   rows.forEach((row) => {
//     const userName = row.querySelector(".user-name").textContent.toLowerCase()
//     const userEmail = row.querySelector(".user-email").textContent.toLowerCase()

//     if (userName.includes(searchTerm.toLowerCase()) || userEmail.includes(searchTerm.toLowerCase())) {
//       row.style.display = ""
//     } else {
//       row.style.display = "none"
//     }
//   })
// }

// function filterHistory(searchTerm) {
//   const rows = document.querySelectorAll(".history-table tbody tr")

//   rows.forEach((row) => {
//     const userName = row.querySelector(".user-name").textContent.toLowerCase()
//     const activity = row.cells[1].textContent.toLowerCase()

//     if (userName.includes(searchTerm.toLowerCase()) || activity.includes(searchTerm.toLowerCase())) {
//       row.style.display = ""
//     } else {
//       row.style.display = "none"
//     }
//   })
// }

// // File Upload Handlers
// document.querySelectorAll('.upload-area input[type="file"]').forEach((input) => {
//   input.addEventListener("change", function (e) {
//     const file = e.target.files[0]
//     if (file) {
//       console.log("File selected:", file.name)
//       const uploadArea = this.parentElement
//       uploadArea.innerHTML = `
//                 <i class="fas fa-check-circle" style="color: #28a745;"></i>
//                 <p style="color: #28a745;">${file.name}</p>
//             `
//     }
//   })
// })

// // Text Editor Functionality
// document.querySelectorAll(".editor-toolbar button").forEach((button) => {
//   button.addEventListener("click", function (e) {
//     e.preventDefault()
//     const command = this.querySelector("i").classList[1].split("-")[1]

//     switch (command) {
//       case "bold":
//         document.execCommand("bold")
//         break
//       case "italic":
//         document.execCommand("italic")
//         break
//       case "underline":
//         document.execCommand("underline")
//         break
//       case "ul":
//         document.execCommand("insertUnorderedList")
//         break
//       case "ol":
//         document.execCommand("insertOrderedList")
//         break
//       case "link":
//         const url = prompt("Enter URL:")
//         if (url) {
//           document.execCommand("createLink", false, url)
//         }
//         break
//     }
//   })
// })

// // Cancel button handler
// const cancelButtons = document.querySelectorAll(".cancel-btn");
// cancelButtons.forEach((btn) => {
//     btn.addEventListener("click", () => {
//         const modal = btn.closest(".modal");
//         if (modal) {
//             modal.style.display = "none";
//         }
//     });
// });

// // Modal Management (existing code)
// window.addEventListener("click", (e) => {
//     const modals = document.querySelectorAll(".modal");
//     modals.forEach((modal) => {
//         if (e.target === modal) {
//             modal.style.display = "none";
//         }
//     });
// });

// // Form submission handler 
// const addUserForm = document.getElementById("addUserForm");
// if (addUserForm) {
//     addUserForm.addEventListener("submit", function (e) {
//         e.preventDefault();
//         const formData = new FormData(this);
        
//         for (let [key, value] of formData.entries()) {
//             console.log(`${key}: ${value}`);
//         }
        
//         //Handle imae upload 
//         const userImage = document.getElementById("userImage").files[0];
//         if (userImage) {
//             console.log("Image uploaded:", userImage.name);
//             uploadImage(userImage, formData)
//                     .then(response => {
//                         if (response.ok) {
//                             console.log("Image uploaded successfully");
//                             // Proceed with form submission or user creation
//                             handleFormSubmission(formData);
//                         } else {
//                             console.error("Image upload failed:", response.statusText);
//                         }
//                     })
//                     .catch(error => {
//                         console.error("Error during upload:", error);
//                     });
//             } else {
//                 // No image, proceed directly with form submission
//                 handleFormSubmission(formData);
//         }

//         this.reset();
//         this.closest(".modal").style.display = "none";
//     });
// }

// // Function to upload image
// function uploadImage(file, formData) {
//     return new Promise((resolve, reject) => {
//         const uploadUrl = "https://your-backend-endpoint/upload"; // Replace with your server URL
//         const requestData = new FormData();
//         requestData.append("userImage", file); // Add the file to FormData
//         // Optionally add other form fields if needed by the backend
//         for (let [key, value] of formData.entries()) {
//             if (key !== "userImage") { // Avoid duplicating the file input
//                 requestData.append(key, value);
//             }
//         }

//         fetch(uploadUrl, {
//             method: "POST",
//             body: requestData,
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error("Upload failed");
//             }
//             return response.json(); // Assuming backend returns JSON (e.g., { url: "path/to/image" })
//         })
//         .then(data => {
//             // Store the image URL or ID in formData if returned by the backend
//             if (data.imageUrl) {
//                 formData.append("imageUrl", data.imageUrl); // For later use
//             }
//             resolve(response);
//         })
//         .catch(error => {
//             reject(error);
//         });
//     });
// }

// // Function to handle form submission after image upload
// function handleFormSubmission(formData) {
//     for (let [key, value] of formData.entries()) {
//         console.log(`${key}: ${value}`);
//     }
    
//     console.log("User added successfully (simulated)");
//     addUserForm.reset();
//     addUserForm.closest(".modal").style.display = "none";
// }

// // Sample data for demonstration
// const sampleUsers = [
//   {
//     id: "kakashi",
//     name: "Kakashi Hatake",
//     email: "kakashi@znhswest.edu.ph",
//     access: ["Admin", "Staff Expert", "Adviser"],
//     lastActive: "August 22, 2025",
//     dateAdded: "August 22, 2024",
//     avatar: "/diverse-user-avatars.png",
//   },
//   {
//     id: "gojo",
//     name: "Gojo Satoru",
//     email: "gojo@znhswest.edu.ph",
//     access: ["Admin", "Staff Expert", "Adviser"],
//     lastActive: "August 22, 2025",
//     dateAdded: "August 22, 2024",
//     avatar: "/diverse-user-avatars.png",
//   },
//   {
//     id: "levi",
//     name: "Levi Ackerman",
//     email: "levi@znhswest.edu.ph",
//     access: ["Staff Expert", "Adviser"],
//     lastActive: "August 22, 2025",
//     dateAdded: "August 22, 2024",
//     avatar: "/diverse-user-avatars.png",
//   },
// ]

// const sampleHistory = [
//   {
//     user: "Kakashi Hatake",
//     role: "System Administrator",
//     activity: "Created a New User Account",
//     date: "August 22, 2025",
//     time: "10:29 am",
//     avatar: "/diverse-user-avatars.png",
//   },
//   {
//     user: "Sakamaru Nara",
//     role: "Subject Teacher",
//     activity: "Update Student profile",
//     date: "August 22, 2025",
//     time: "10:29 am",
//     avatar: "/diverse-user-avatars.png",
//   },
// ]

// console.log("Settings page loaded successfully")

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

// Settings Page JavaScript

// Utility: Get CSRF Token from Cookie (for Django POST)
// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

// // Tab Management
// document.addEventListener("DOMContentLoaded", () => {
//     console.log("Settings JS loaded – DOM ready!");

//     // Initialize tab functionality
//     const tabBtns = document.querySelectorAll(".tab-btn");
//     const tabContents = document.querySelectorAll(".tab-content");

//     tabBtns.forEach((btn) => {
//         btn.addEventListener("click", () => {
//             const tabName = btn.getAttribute("data-tab");

//             // Remove active class from all tabs and contents
//             tabBtns.forEach((b) => b.classList.remove("active"));
//             tabContents.forEach((c) => c.classList.remove("active"));

//             // Add active class to clicked tab and corresponding content
//             btn.classList.add("active");
//             document.getElementById(`${tabName}-tab`).classList.add("active");
//         });
//     });

//     // Content Management sub-tabs
//     const contentTabBtns = document.querySelectorAll(".content-tab-btn");
//     const contentSections = document.querySelectorAll(".content-section");

//     contentTabBtns.forEach((btn) => {
//         btn.addEventListener("click", () => {
//             const contentName = btn.getAttribute("data-content");

//             // Remove active class from all content tabs and sections
//             contentTabBtns.forEach((b) => b.classList.remove("active"));
//             contentSections.forEach((s) => s.classList.remove("active"));

//             // Add active class to clicked tab and corresponding section
//             btn.classList.add("active");
//             document.getElementById(`${contentName}-content`).classList.add("active");
//         });
//     });

//     // Search functionality
//     const userSearch = document.getElementById("userSearch");
//     const historySearch = document.getElementById("historySearch");

//     if (userSearch) {
//         userSearch.addEventListener("input", function () {
//             filterUsers(this.value);
//         });
//     }

//     if (historySearch) {
//         historySearch.addEventListener("input", function () {
//             filterHistory(this.value);
//         });
//     }

//     // Close dropdowns when clicking outside
//     document.addEventListener("click", (e) => {
//         if (!e.target.closest(".actions-dropdown")) {
//             document.querySelectorAll(".dropdown-menu").forEach((menu) => {
//                 menu.classList.remove("show");
//             });
//         }
//     });

//     // File Upload Handlers (Previews) – Merged here
//     document.querySelectorAll('.upload-area input[type="file"]').forEach((input) => {
//         input.addEventListener("change", function (e) {
//             const file = e.target.files[0];
//             if (file) {
//                 console.log("File selected:", file.name);
//                 const uploadArea = this.parentElement;
//                 uploadArea.innerHTML = `
//                     <i class="fas fa-check-circle" style="color: #28a745;"></i>
//                     <p style="color: #28a745;">${file.name}</p>
//                 `;
//             }
//         });
//     });

//     // Text Editor Functionality – Merged here
//     document.querySelectorAll(".editor-toolbar button").forEach((button) => {
//         button.addEventListener("click", function (e) {
//             e.preventDefault();
//             const command = this.querySelector("i").classList[1].split("-")[1];

//             switch (command) {
//                 case "bold":
//                     document.execCommand("bold");
//                     break;
//                 case "italic":
//                     document.execCommand("italic");
//                     break;
//                 case "underline":
//                     document.execCommand("underline");
//                     break;
//                 case "ul":
//                     document.execCommand("insertUnorderedList");
//                     break;
//                 case "ol":
//                     document.execCommand("insertOrderedList");
//                     break;
//                 case "link":
//                     const url = prompt("Enter URL:");
//                     if (url) {
//                         document.execCommand("createLink", false, url);
//                     }
//                     break;
//             }
//         });
//     });

//     // Add User Form Submission (Real AJAX to Backend – No Simulation!)
//     // Add User Form Submission

// // Add User Form Submission
// const addUserForm = document.getElementById("addUserForm");
// if (addUserForm) {
//     console.log("Form found – attaching submit handler.");
//     addUserForm.addEventListener("submit", function (e) {
//         e.preventDefault();
//         console.log("=== Real Form Submission Started (AJAX to Backend) ===");

//         const formData = new FormData(this);
//         const actionUrl = this.action; // Use the action from the form for robustness!

//         fetch(actionUrl, { // <--- Use the form's action URL
//             method: 'POST',
//             body: formData,
//             headers: {
//                 'X-CSRFToken': getCookie('csrftoken'),
//                 'X-Requested-With': 'XMLHttpRequest', // Important for Django view
//             },
//         })
//         .then(response => {
//             console.log("Response status:", response.status);
//             if (response.ok) { // Check if status is 200-299
//                 return response.json();
//             }
//             // For 400 or 500 errors, still try to parse JSON for error messages
//             return response.json().then(errorData => {
//                 throw new Error(JSON.stringify(errorData.errors || errorData.message || "Unknown error occurred"));
//             });
//         })
//         .then(data => {
//             console.log("Response data:", data);
            
//             if (data.success) {
//                 // 1. Show success message (using alert for simplicity)
//                 alert(data.message || 'User added successfully!');
                
//                 // 2. Close the modal
//                 closeAddUserModal(); 
                
//                 // 3. Dynamically update the tables
//                 fetchTables(); // <--- Call a combined function to refresh both users and logs
//             } else {
//                 // This path should ideally be caught by the response.ok check above, 
//                 // but kept for robustness.
//                  console.error('Submission failed with server-side logic error:', data.message, data.errors);
//                  alert('Form Errors: ' + JSON.stringify(data.errors));
//             }
//         })
//         .catch(error => {
//             console.error('Fetch error:', error);
//             try {
//                 const errorObj = JSON.parse(error.message);
//                 // Display specific error messages from Django (e.g., 'email' already exists)
//                 const errorString = Object.keys(errorObj).map(key => `${key}: ${errorObj[key]}`).join('\n');
//                 alert(`Submission failed: \n${errorString}`);
//             } catch (e) {
//                 alert(`Submission failed: ${error.message}`);
//             }
//         });
//     });
// }


// // NEW FUNCTION: Combines user and log fetching for complete refresh
// function fetchTables() {
//     fetchUsersTable();
//     fetchHistoryTable(); // NEW: Refresh history log
// }


// // NEW/FIXED Function: Fetch and Update Users Table Dynamically
// // NOTE: You need a new Django URL/View to return the full HTML or JSON for the user table.
// // I'll assume a new endpoint '/settings/get-all-data/' is created in views.py
// function fetchUsersTable() {
//     // You must create a new Django view at this URL that returns the *rendered HTML* // for the table body, OR returns JSON data for the whole user list.
//     // Given your current setup, returning JSON for the user list is better (like the stub).
    
//     // NOTE: This URL '/settings/get-users/' is NOT in your current urls.py!
//     // You MUST add: path('settings/get-users/', views.get_users_data, name='get_users_data'),
//     // And implement `get_users_data` in views.py.
//     fetch('/admin-functionalities/settings/get-users/', { 
//         method: 'GET',
//         headers: {
//             'X-CSRFToken': getCookie('csrftoken'),
//             'X-Requested-With': 'XMLHttpRequest',
//         },
//     })
//     .then(response => {
//         if (!response.ok) throw new Error('Failed to fetch user list.');
//         return response.json();
//     })
//     .then(data => {
//         const tableBody = document.getElementById('usersTableBody');
//         if (tableBody && data.users) { // Assuming data.users is the list of users
//             tableBody.innerHTML = '';  // Clear existing rows
//             data.users.forEach(user => { 
//                 const row = document.createElement('tr');
//                 row.innerHTML = `
//                     <td>
//                         <div class="user-info">
//                             <img src="/static/admin_functionalities/assets/kakashi.jpeg" alt="User" class="user-avatar" />
//                             <div>
//                                 <div class="user-name">${user.first_name} ${user.last_name}</div>
//                                 <div class="user-email">${user.email}</div>
//                             </div>
//                         </div>
//                     </td>
//                     <td>
//                         ${user.is_superuser ? '<span class="access-badge admin">Admin</span>' : ''}
//                         ${user.is_staff_expert ? '<span class="access-badge staff">Staff Expert</span>' : ''}
//                         ${user.is_subject_teacher ? '<span class="access-badge teacher">Subject Teacher</span>' : ''}
//                         ${user.is_adviser ? '<span class="access-badge adviser">Adviser</span>' : ''}
//                     </td>
//                     <td>${user.last_login_formatted || user.date_joined_formatted}</td>
//                     <td>${user.date_joined_formatted}</td>
//                     <td>
//                         <div class="actions-dropdown">
//                             <button class="actions-btn" onclick="toggleDropdown(this)">
//                                 <i class="fas fa-ellipsis-v"></i>
//                             </button>
//                             <div class="dropdown-menu">
//                                 <a href="#" onclick="viewProfile('${user.id}')"><i class="fas fa-eye"></i> View Profile</a>
//                                 <a href="#" onclick="editDetails('${user.id}')"><i class="fas fa-edit"></i> Edit Details</a>
//                                 <a href="#" onclick="changePermission('${user.id}')"><i class="fas fa-user-cog"></i> Change Permission</a>
//                                 <a href="#" onclick="deleteUser ('${user.id}')" class="delete-action"><i class="fas fa-trash"></i> Delete User</a>
//                             </div>
//                         </div>
//                     </td>
//                 `;
//                 tableBody.appendChild(row);
//             });
//         }
//     })
//     .catch(error => console.error('Error fetching users:', error));
// }


// // NEW FUNCTION: Fetch and Update History Table Dynamically
// // NOTE: You must also create a view for this!
// function fetchHistoryTable() {
//     // You MUST add: path('settings/get-logs/', views.get_logs_data, name='get_logs_data'),
//     // And implement `get_logs_data` in views.py.
//     fetch('/admin-functionalities/settings/get-logs/', { 
//         method: 'GET',
//         headers: {
//             'X-CSRFToken': getCookie('csrftoken'),
//             'X-Requested-With': 'XMLHttpRequest',
//         },
//     })
//     .then(response => {
//         if (!response.ok) throw new Error('Failed to fetch history logs.');
//         return response.json();
//     })
//     .then(data => {
//         const tableBody = document.getElementById('history-tab').querySelector('tbody');
//         if (tableBody && data.logs) {
//             tableBody.innerHTML = ''; // Clear existing rows
//             data.logs.forEach(log => {
//                 const row = document.createElement('tr');
//                 row.innerHTML = `
//                     <td>
//                         <div class="user-info">
//                             <img src="/static/admin_functionalities/assets/kakashi.jpeg" alt="User" class="user-avatar small" />
//                             <div>
//                                 <div class="user-name">${log.user_full_name}</div>
//                                 <div class="user-role">${log.user_role}</div>
//                             </div>
//                         </div>
//                     </td>
//                     <td>${log.action}</td>
//                     <td>${log.date_formatted}</td>
//                     <td>${log.time_formatted}</td>
//                 `;
//                 tableBody.appendChild(row);
//             });
//         }
//     })
//     .catch(error => console.error('Error fetching history logs:', error));
// }


//     // Cancel button handler
//     const cancelButtons = document.querySelectorAll(".cancel-btn");
//     cancelButtons.forEach((btn) => {
//         btn.addEventListener("click", () => {
//             const modal = btn.closest(".modal");
//             if (modal) {
//                 modal.style.display = "none";
//             }
//         });
//     });

//     // Modal close on outside click
//     window.addEventListener("click", (e) => {
//         const modals = document.querySelectorAll(".modal");
//         modals.forEach((modal) => {
//             if (e.target === modal) {
//                 modal.style.display = "none";
//             }
//         });
//     });
// });

// // Dropdown Management
// function toggleDropdown(button) {
//     const dropdown = button.nextElementSibling;
//     const isOpen = dropdown.classList.contains("show");

//     // Close all dropdowns first
//     document.querySelectorAll(".dropdown-menu").forEach((menu) => {
//         menu.classList.remove("show");
//     });

//     // Toggle current dropdown with animation
//     if (!isOpen) {
//         dropdown.classList.add("show");
//         // Ensure dropdown is visible and positioned correctly
//         setTimeout(() => {
//             dropdown.style.zIndex = "1001";
//         }, 10);
//     }
// }

// // User Management Functions – FIXED: No spaces in IDs
// function openAddUserModal() {
//     const modal = document.getElementById("addUserModal");  // No space
//     if (modal) {
//         modal.style.display = "block";
//         console.log("Add User Modal opened.");
//     } else {
//         console.error("Modal not found! Check ID='addUser Modal' in HTML.");
//     }
// }

// function closeAddUserModal() {
//     const modal = document.getElementById("addUserModal");  // No space
//     if (modal) {
//         modal.style.display = "none";
//         const form = document.getElementById("addUserForm");  // No space
//         if (form) form.reset();
//         console.log("Add User Modal closed and form reset.");
//     } else {
//         console.error("Modal not found for close!");
//     }
// }

// function viewProfile(userId) {
//     console.log("Opening profile for user:", userId);
//     document.getElementById("userProfileModal").style.display = "block";
//     // Close any open dropdowns
//     document.querySelectorAll(".dropdown-menu").forEach((menu) => {
//         menu.classList.remove("show");
//     });
// }

// function closeUserProfileModal() {
//     document.getElementById("userProfileModal").style.display = "none";
// }

// function editDetails(userId) {
//     console.log("Editing details for user:", userId);
//     alert(`Edit details for user: ${userId}`);
//     // Close dropdown
//     document.querySelectorAll(".dropdown-menu").forEach((menu) => {
//         menu.classList.remove("show");
//     });
// }

// function changePermission(userId) {
//     console.log("Changing permissions for user:", userId);
//     alert(`Change permissions for user: ${userId}`);
//     // Close dropdown
//     document.querySelectorAll(".dropdown-menu").forEach((menu) => {
//         menu.classList.remove("show");
//     });
// }

// function deleteUser (userId) {
//     console.log("Deleting user:", userId);
//     if (confirm(`Are you sure you want to delete user: ${userId}?`)) {
//         alert(`User  ${userId} deleted successfully`);
//     }
//     // Close dropdown
//     document.querySelectorAll(".dropdown-menu").forEach((menu) => {
//         menu.classList.remove("show");
//     });
// }

// // Search and Filter Functions
// function filterUsers(searchTerm) {
//     const rows = document.querySelectorAll("#usersTableBody tr");

//     rows.forEach((row) => {
//         const userName = row.querySelector(".user-name") ? row.querySelector(".user-name").textContent.toLowerCase() : '';
//         const userEmail = row.querySelector(".user-email") ? row.querySelector(".user-email").textContent.toLowerCase() : '';

//         if (userName.includes(searchTerm.toLowerCase()) || userEmail.includes(searchTerm.toLowerCase())) {
//             row.style.display = "";
//         } else {
//             row.style.display = "none";
//         }
//     });
// }

// function filterHistory(searchTerm) {
//     const rows = document.querySelectorAll(".history-table tbody tr");

//     rows.forEach((row) => {
//         const userName = row.querySelector(".user-name") ? row.querySelector(".user-name").textContent.toLowerCase() : '';
//         const activity = row.cells[1] ? row.cells[1].textContent.toLowerCase() : '';

//         if (userName.includes(searchTerm.toLowerCase()) || activity.includes(searchTerm.toLowerCase())) {
//             row.style.display = "";
//         } else {
//             row.style.display = "none";
//         }
//     });
// }

// // Logout Handler (Stub – Customize as Needed)
// function setupLogoutHandler() {
//     const logoutBtn = document.querySelector(".logout-btn");
//     if (logoutBtn) {
//         logoutBtn.addEventListener("click", (e) => {
//             e.preventDefault();
//             handleLogout();
//         });
//     }
// }

// function handleLogout() {
//     // Clear session data
//     localStorage.removeItem("isLoggedIn");
//     localStorage.removeItem("username");
//     localStorage.removeItem("loginTime");

//     // Redirect (use your logout URL)
//     window.location.href = '/admin-functionalities/logout/';
// }

// setupLogoutHandler();  // Init on load

// console.log("Settings page JS loaded successfully – Real AJAX enabled! IDs fixed (no spaces).");


// Utility: Get CSRF Token from Cookie (for Django POST)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", () => {
    console.log("Settings JS loaded – DOM ready!");

    // Initialize tab functionality
    const tabBtns = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");

    tabBtns.forEach((btn) => {
        btn.addEventListener("click", () => {
            const tabName = btn.getAttribute("data-tab");
            tabBtns.forEach((b) => b.classList.remove("active"));
            tabContents.forEach((c) => c.classList.remove("active"));
            btn.classList.add("active");
            document.getElementById(`${tabName}-tab`).classList.add("active");
        });
    });

    // Content Management sub-tabs
    const contentTabBtns = document.querySelectorAll(".content-tab-btn");
    const contentSections = document.querySelectorAll(".content-section");

    contentTabBtns.forEach((btn) => {
        btn.addEventListener("click", () => {
            const contentName = btn.getAttribute("data-content");
            contentTabBtns.forEach((b) => b.classList.remove("active"));
            contentSections.forEach((s) => s.classList.remove("active"));
            btn.classList.add("active");
            document.getElementById(`${contentName}-content`).classList.add("active");
        });
    });

    // Search functionality
    const userSearch = document.getElementById("userSearch");
    if (userSearch) {
        userSearch.addEventListener("input", function () {
            filterUsers(this.value);
        });
    }

    const historySearch = document.getElementById("historySearch");
    if (historySearch) {
        historySearch.addEventListener("input", function () {
            filterHistory(this.value);
        });
    }

    // Close dropdowns when clicking outside
    document.addEventListener("click", (e) => {
        if (!e.target.closest(".actions-dropdown")) {
            document.querySelectorAll(".dropdown-menu").forEach((menu) => {
                menu.classList.remove("show");
            });
        }
    });

    // File Upload Handlers
    document.querySelectorAll('.upload-area input[type="file"]').forEach((input) => {
        input.addEventListener("change", function (e) {
            const file = e.target.files[0];
            if (file) {
                const uploadArea = this.parentElement;
                uploadArea.innerHTML = `<i class="fas fa-check-circle" style="color: #28a745;"></i><p style="color: #28a745;">${file.name}</p>`;
            }
        });
    });

    // Text Editor Functionality
    document.querySelectorAll(".editor-toolbar button").forEach((button) => {
        button.addEventListener("click", function (e) {
            e.preventDefault();
            const command = this.querySelector("i").classList[1].split("-")[1];
            switch (command) {
                case "bold": document.execCommand("bold"); break;
                case "italic": document.execCommand("italic"); break;
                case "underline": document.execCommand("underline"); break;
                case "ul": document.execCommand("insertUnorderedList"); break;
                case "ol": document.execCommand("insertOrderedList"); break;
                case "link": {
                    const url = prompt("Enter URL:");
                    if (url) document.execCommand("createLink", false, url);
                    break;
                }
            }
        });
    });

    // Add User Form Submission
    const addUserForm = document.getElementById("addUserForm");
    if (addUserForm) {
        console.log("Form found – attaching submit handler.");
        addUserForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const formData = new FormData(this);
            const actionUrl = this.action;

            fetch(actionUrl, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then(response => {
                return response.json().then(data => {
                    if (!response.ok) {
                        // Backend returned error or non-200 status
                        throw new Error(data.message || JSON.stringify(data.errors) || "Unknown error");
                    }
                    return data;
                }).catch(() => {
                    throw new Error("Invalid JSON response from server.");
                });
            })

            .then(data => {
                const errorDiv = document.getElementById('addUserErrors');
                if (data.success) {
                    alert(data.message || 'User added successfully!');
                    closeAddUserModal();
                    fetchTables();
                } else if (errorDiv) {
                    errorDiv.innerHTML = formatErrors(data.errors);
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
                alert(`Submission failed: ${error.message}`);
            });

        });
    }

    // Error Formatter
    function formatErrors(errors) {
        let html = '<ul>';
        for (let field in errors) html += `<li>${field}: ${errors[field]}</li>`;
        return html + '</ul>';
    }

    // Table Fetchers
    function fetchTables() {
        fetchUsersTable();
        fetchHistoryTable();
    }

    function fetchUsersTable() {
        fetch('/admin-functionalities/settings/get-users/', {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('usersTableBody');
            if (tableBody && data.users) {
                tableBody.innerHTML = '';
                data.users.forEach(user => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>
                            <div class="user-info">
                                <img src="/static/admin_functionalities/assets/kakashi.jpeg" alt="User" class="user-avatar" />
                                <div>
                                    <div class="user-name">${user.first_name} ${user.last_name}</div>
                                    <div class="user-email">${user.email}</div>
                                </div>
                            </div>
                        </td>
                        <td>
                            ${user.is_superuser ? '<span class="access-badge admin">Admin</span>' : ''}
                            ${user.is_staff_expert ? '<span class="access-badge staff">Staff Expert</span>' : ''}
                            ${user.is_subject_teacher ? '<span class="access-badge teacher">Subject Teacher</span>' : ''}
                            ${user.is_adviser ? '<span class="access-badge adviser">Adviser</span>' : ''}
                        </td>
                        <td>${user.last_login_formatted || user.date_joined_formatted}</td>
                        <td>${user.date_joined_formatted}</td>
                        <td>
                            <div class="actions-dropdown">
                                <button class="actions-btn" onclick="toggleDropdown(this)">
                                    <i class="fas fa-ellipsis-v"></i>
                                </button>
                                <div class="dropdown-menu">
                                    <a href="#" onclick="viewProfile('${user.id}')"><i class="fas fa-eye"></i> View Profile</a>
                                    <a href="#" onclick="editDetails('${user.id}')"><i class="fas fa-edit"></i> Edit Details</a>
                                    <a href="#" onclick="changePermission('${user.id}')"><i class="fas fa-user-cog"></i> Change Permission</a>
                                    <a href="#" onclick="deleteUser('${user.id}')" class="delete-action"><i class="fas fa-trash"></i> Delete User</a>
                                </div>
                            </div>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });
            }
        })
        .catch(error => console.error('Error fetching users:', error));
    }

    function fetchHistoryTable() {
        fetch('/admin-functionalities/settings/get-logs/', {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#history-tab tbody');
            if (tableBody && data.logs) {
                tableBody.innerHTML = '';
                data.logs.forEach(log => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>
                            <div class="user-info">
                                <img src="/static/admin_functionalities/assets/kakashi.jpeg" alt="User" class="user-avatar small" />
                                <div>
                                    <div class="user-name">${log.user_full_name}</div>
                                    <div class="user-role">${log.user_role}</div>
                                </div>
                            </div>
                        </td>
                        <td>${log.action}</td>
                        <td>${log.date_formatted}</td>
                        <td>${log.time_formatted}</td>
                    `;
                    tableBody.appendChild(row);
                });
            }
        })
        .catch(error => console.error('Error fetching logs:', error));
    }

    // === User Management Functions ===
    window.openAddUserModal = function () {
        const modal = document.getElementById("addUserModal");
        if (modal) modal.style.display = "block";
    };

    window.closeAddUserModal = function () {
        const modal = document.getElementById("addUserModal");
        if (modal) {
            modal.style.display = "none";
            const form = document.getElementById("addUserForm");
            if (form) form.reset();
        }
    };

    window.viewProfile = function (userId) {
        console.log("Opening profile for user:", userId);
        document.getElementById("userProfileModal").style.display = "block";
        document.querySelectorAll(".dropdown-menu").forEach(menu => menu.classList.remove("show"));
    };

    window.closeUserProfileModal = function () {
        document.getElementById("userProfileModal").style.display = "none";
    };

    window.editDetails = function (userId) {
        alert(`Edit details for user: ${userId}`);
        document.querySelectorAll(".dropdown-menu").forEach(menu => menu.classList.remove("show"));
    };

    window.changePermission = function (userId) {
        alert(`Change permissions for user: ${userId}`);
        document.querySelectorAll(".dropdown-menu").forEach(menu => menu.classList.remove("show"));
    };

    window.deleteUser = function (userId) {
        if (confirm(`Are you sure you want to delete user: ${userId}?`)) {
            alert(`User ${userId} deleted successfully`);
        }
        document.querySelectorAll(".dropdown-menu").forEach(menu => menu.classList.remove("show"));
    };

    // Dropdown Management
    window.toggleDropdown = function (button) {
        const dropdown = button.nextElementSibling;
        const isOpen = dropdown.classList.contains("show");
        document.querySelectorAll(".dropdown-menu").forEach(menu => menu.classList.remove("show"));
        if (!isOpen) dropdown.classList.add("show");
    };

    // === Search and Filter ===
    window.filterUsers = function (searchTerm) {
        const rows = document.querySelectorAll("#usersTableBody tr");
        rows.forEach((row) => {
            const userName = row.querySelector(".user-name")?.textContent.toLowerCase() || '';
            const userEmail = row.querySelector(".user-email")?.textContent.toLowerCase() || '';
            row.style.display = (userName.includes(searchTerm.toLowerCase()) || userEmail.includes(searchTerm.toLowerCase())) ? "" : "none";
        });
    };

    window.filterHistory = function (searchTerm) {
        const rows = document.querySelectorAll(".history-table tbody tr");
        rows.forEach((row) => {
            const userName = row.querySelector(".user-name")?.textContent.toLowerCase() || '';
            const activity = row.cells[1]?.textContent.toLowerCase() || '';
            row.style.display = (userName.includes(searchTerm.toLowerCase()) || activity.includes(searchTerm.toLowerCase())) ? "" : "none";
        });
    };


    // === Logout Handler ===
    function setupLogoutHandler() {
        const logoutBtn = document.querySelector(".logout-btn");
        if (logoutBtn) {
            logoutBtn.addEventListener("click", (e) => {
                e.preventDefault();
                handleLogout();
            });
        }
    }

    function handleLogout() {
        localStorage.removeItem("isLoggedIn");
        localStorage.removeItem("username");
        localStorage.removeItem("loginTime");
        window.location.href = '/logout/';
    }

    setupLogoutHandler();
});



console.log("Settings page JS loaded successfully – all functionality merged and active.");
