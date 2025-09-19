// Settings Page JavaScript

// Tab Management
document.addEventListener("DOMContentLoaded", () => {
  // Initialize tab functionality
  const tabBtns = document.querySelectorAll(".tab-btn")
  const tabContents = document.querySelectorAll(".tab-content")

  tabBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const tabName = btn.getAttribute("data-tab")

      // Remove active class from all tabs and contents
      tabBtns.forEach((b) => b.classList.remove("active"))
      tabContents.forEach((c) => c.classList.remove("active"))

      // Add active class to clicked tab and corresponding content
      btn.classList.add("active")
      document.getElementById(`${tabName}-tab`).classList.add("active")
    })
  })

  // Content Management sub-tabs
  const contentTabBtns = document.querySelectorAll(".content-tab-btn")
  const contentSections = document.querySelectorAll(".content-section")

  contentTabBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const contentName = btn.getAttribute("data-content")

      // Remove active class from all content tabs and sections
      contentTabBtns.forEach((b) => b.classList.remove("active"))
      contentSections.forEach((s) => s.classList.remove("active"))

      // Add active class to clicked tab and corresponding section
      btn.classList.add("active")
      document.getElementById(`${contentName}-content`).classList.add("active")
    })
  })

  // Search functionality
  const userSearch = document.getElementById("userSearch")
  const historySearch = document.getElementById("historySearch")

  if (userSearch) {
    userSearch.addEventListener("input", function () {
      filterUsers(this.value)
    })
  }

  if (historySearch) {
    historySearch.addEventListener("input", function () {
      filterHistory(this.value)
    })
  }

  // Close dropdowns when clicking outside
  document.addEventListener("click", (e) => {
    if (!e.target.closest(".actions-dropdown")) {
      document.querySelectorAll(".dropdown-menu").forEach((menu) => {
        menu.classList.remove("show")
      })
    }
  })

  // Form submission handler
  const addUserForm = document.getElementById("addUserForm")
  if (addUserForm) {
    addUserForm.addEventListener("submit", (e) => {
      e.preventDefault()

      const firstName = document.getElementById("firstName").value
      const lastName = document.getElementById("lastName").value
      const email = document.getElementById("email").value
      const employeeId = document.getElementById("employeeId").value
      const position = document.getElementById("position").value
      const department = document.getElementById("department").value
      const tempPassword = document.getElementById("tempPassword").value

      const permissions = Array.from(document.querySelectorAll('input[name="permissions"]:checked')).map(
        (cb) => cb.value,
      )

      const userData = {
        firstName,
        lastName,
        email,
        employeeId,
        position,
        department,
        permissions,
        tempPassword,
      }

      console.log("Adding new user:", userData)

      // Simulate API call
      setTimeout(() => {
        alert("User added successfully!")
        closeAddUserModal()
        // Here you would typically refresh the users table
      }, 1000)
    })
  }
})

// Dropdown Management
function toggleDropdown(button) {
  const dropdown = button.nextElementSibling
  const isOpen = dropdown.classList.contains("show")

  // Close all dropdowns first
  document.querySelectorAll(".dropdown-menu").forEach((menu) => {
    menu.classList.remove("show")
  })

  // Toggle current dropdown with animation
  if (!isOpen) {
    dropdown.classList.add("show")
    // Ensure dropdown is visible and positioned correctly
    setTimeout(() => {
      dropdown.style.zIndex = "1001"
    }, 10)
  }
}

// User Management Functions
function openAddUserModal() {
  document.getElementById("addUserModal").style.display = "block"
}

function closeAddUserModal() {
  document.getElementById("addUserModal").style.display = "none"
  document.getElementById("addUserForm").reset()
}

function viewProfile(userId) {
  console.log("Opening profile for user:", userId)
  document.getElementById("userProfileModal").style.display = "block"
  // Close any open dropdowns
  document.querySelectorAll(".dropdown-menu").forEach((menu) => {
    menu.classList.remove("show")
  })
}

function closeUserProfileModal() {
  document.getElementById("userProfileModal").style.display = "none"
}

function editDetails(userId) {
  console.log("Editing details for user:", userId)
  alert(`Edit details for user: ${userId}`)
  // Close dropdown
  document.querySelectorAll(".dropdown-menu").forEach((menu) => {
    menu.classList.remove("show")
  })
}

function changePermission(userId) {
  console.log("Changing permissions for user:", userId)
  alert(`Change permissions for user: ${userId}`)
  // Close dropdown
  document.querySelectorAll(".dropdown-menu").forEach((menu) => {
    menu.classList.remove("show")
  })
}

function deleteUser(userId) {
  console.log("Deleting user:", userId)
  if (confirm(`Are you sure you want to delete user: ${userId}?`)) {
    alert(`User ${userId} deleted successfully`)
  }
  // Close dropdown
  document.querySelectorAll(".dropdown-menu").forEach((menu) => {
    menu.classList.remove("show")
  })
}

// Search and Filter Functions
function filterUsers(searchTerm) {
  const rows = document.querySelectorAll("#usersTableBody tr")

  rows.forEach((row) => {
    const userName = row.querySelector(".user-name").textContent.toLowerCase()
    const userEmail = row.querySelector(".user-email").textContent.toLowerCase()

    if (userName.includes(searchTerm.toLowerCase()) || userEmail.includes(searchTerm.toLowerCase())) {
      row.style.display = ""
    } else {
      row.style.display = "none"
    }
  })
}

function filterHistory(searchTerm) {
  const rows = document.querySelectorAll(".history-table tbody tr")

  rows.forEach((row) => {
    const userName = row.querySelector(".user-name").textContent.toLowerCase()
    const activity = row.cells[1].textContent.toLowerCase()

    if (userName.includes(searchTerm.toLowerCase()) || activity.includes(searchTerm.toLowerCase())) {
      row.style.display = ""
    } else {
      row.style.display = "none"
    }
  })
}

// File Upload Handlers
document.querySelectorAll('.upload-area input[type="file"]').forEach((input) => {
  input.addEventListener("change", function (e) {
    const file = e.target.files[0]
    if (file) {
      console.log("File selected:", file.name)
      const uploadArea = this.parentElement
      uploadArea.innerHTML = `
                <i class="fas fa-check-circle" style="color: #28a745;"></i>
                <p style="color: #28a745;">${file.name}</p>
            `
    }
  })
})

// Text Editor Functionality
document.querySelectorAll(".editor-toolbar button").forEach((button) => {
  button.addEventListener("click", function (e) {
    e.preventDefault()
    const command = this.querySelector("i").classList[1].split("-")[1]

    switch (command) {
      case "bold":
        document.execCommand("bold")
        break
      case "italic":
        document.execCommand("italic")
        break
      case "underline":
        document.execCommand("underline")
        break
      case "ul":
        document.execCommand("insertUnorderedList")
        break
      case "ol":
        document.execCommand("insertOrderedList")
        break
      case "link":
        const url = prompt("Enter URL:")
        if (url) {
          document.execCommand("createLink", false, url)
        }
        break
    }
  })
})

// Cancel button handler
const cancelButtons = document.querySelectorAll(".cancel-btn");
cancelButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
        const modal = btn.closest(".modal");
        if (modal) {
            modal.style.display = "none";
        }
    });
});

// Modal Management (existing code)
window.addEventListener("click", (e) => {
    const modals = document.querySelectorAll(".modal");
    modals.forEach((modal) => {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });
});

// Form submission handler 
const addUserForm = document.getElementById("addUserForm");
if (addUserForm) {
    addUserForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        
        for (let [key, value] of formData.entries()) {
            console.log(`${key}: ${value}`);
        }
        
        //Handle imae upload 
        const userImage = document.getElementById("userImage").files[0];
        if (userImage) {
            console.log("Image uploaded:", userImage.name);
            uploadImage(userImage, formData)
                    .then(response => {
                        if (response.ok) {
                            console.log("Image uploaded successfully");
                            // Proceed with form submission or user creation
                            handleFormSubmission(formData);
                        } else {
                            console.error("Image upload failed:", response.statusText);
                        }
                    })
                    .catch(error => {
                        console.error("Error during upload:", error);
                    });
            } else {
                // No image, proceed directly with form submission
                handleFormSubmission(formData);
        }

        this.reset();
        this.closest(".modal").style.display = "none";
    });
}

// Function to upload image
function uploadImage(file, formData) {
    return new Promise((resolve, reject) => {
        const uploadUrl = "https://your-backend-endpoint/upload"; // Replace with your server URL
        const requestData = new FormData();
        requestData.append("userImage", file); // Add the file to FormData
        // Optionally add other form fields if needed by the backend
        for (let [key, value] of formData.entries()) {
            if (key !== "userImage") { // Avoid duplicating the file input
                requestData.append(key, value);
            }
        }

        fetch(uploadUrl, {
            method: "POST",
            body: requestData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Upload failed");
            }
            return response.json(); // Assuming backend returns JSON (e.g., { url: "path/to/image" })
        })
        .then(data => {
            // Store the image URL or ID in formData if returned by the backend
            if (data.imageUrl) {
                formData.append("imageUrl", data.imageUrl); // For later use
            }
            resolve(response);
        })
        .catch(error => {
            reject(error);
        });
    });
}

// Function to handle form submission after image upload
function handleFormSubmission(formData) {
    for (let [key, value] of formData.entries()) {
        console.log(`${key}: ${value}`);
    }
    
    console.log("User added successfully (simulated)");
    addUserForm.reset();
    addUserForm.closest(".modal").style.display = "none";
}

// Sample data for demonstration
const sampleUsers = [
  {
    id: "kakashi",
    name: "Kakashi Hatake",
    email: "kakashi@znhswest.edu.ph",
    access: ["Admin", "Staff Expert", "Adviser"],
    lastActive: "August 22, 2025",
    dateAdded: "August 22, 2024",
    avatar: "/diverse-user-avatars.png",
  },
  {
    id: "gojo",
    name: "Gojo Satoru",
    email: "gojo@znhswest.edu.ph",
    access: ["Admin", "Staff Expert", "Adviser"],
    lastActive: "August 22, 2025",
    dateAdded: "August 22, 2024",
    avatar: "/diverse-user-avatars.png",
  },
  {
    id: "levi",
    name: "Levi Ackerman",
    email: "levi@znhswest.edu.ph",
    access: ["Staff Expert", "Adviser"],
    lastActive: "August 22, 2025",
    dateAdded: "August 22, 2024",
    avatar: "/diverse-user-avatars.png",
  },
]

const sampleHistory = [
  {
    user: "Kakashi Hatake",
    role: "System Administrator",
    activity: "Created a New User Account",
    date: "August 22, 2025",
    time: "10:29 am",
    avatar: "/diverse-user-avatars.png",
  },
  {
    user: "Sakamaru Nara",
    role: "Subject Teacher",
    activity: "Update Student profile",
    date: "August 22, 2025",
    time: "10:29 am",
    avatar: "/diverse-user-avatars.png",
  },
]

console.log("Settings page loaded successfully")

function setupLogoutHandler() {
  const logoutBtn = document.querySelector(".logout-btn")
  if (logoutBtn) {
    logoutBtn.addEventListener("click", (e) => {
      e.preventDefault()
      handleLogout()
    })
  }
}

function handleLogout() {
  // Clear all session data
  localStorage.removeItem("isLoggedIn")
  localStorage.removeItem("username")
  localStorage.removeItem("loginTime")

  // Show notification and redirect
  showNotification("Logging out...", "info")

  setTimeout(() => {
    window.location.href = "logout.html"
  }, 1000)
}

function showNotification(message, type) {
  const container = document.getElementById("notificationContainer")

  if (!container) return

  // Create the notification element
  const notification = document.createElement("div")
  notification.className = `notification ${type}`
  notification.innerHTML = `
          <span>${message}</span>
          <button class="notification-close">&times;</button>
      `

  // Add a click event to the close button
  notification.querySelector(".notification-close").addEventListener("click", () => {
    notification.remove()
  })

  // Append to the container
  container.appendChild(notification)

  // Automatically remove the notification after 4 seconds
  setTimeout(() => {
    if (container.contains(notification)) {
      notification.remove()
    }
  }, 4000)
}