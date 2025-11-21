// function togglePassword() {
//   const passwordField = document.getElementById("password")
//   const passwordIcon = document.getElementById("password-icon")

//   if (passwordField.type === "password") {
//     passwordField.type = "text"
//     passwordIcon.textContent = "🙈"
//   } else {
//     passwordField.type = "password"
//     passwordIcon.textContent = "👁️"
//   }
// }

// // Modal functions
// function showModal(title, message, isSuccess = false) {
//   const modal = document.getElementById("loginModal")
//   const modalTitle = document.getElementById("modalTitle")
//   const modalMessage = document.getElementById("modalMessage")

//   modalTitle.textContent = title
//   modalMessage.textContent = message
//   modalMessage.className = isSuccess ? "success-message" : "error-message"

//   modal.style.display = "block"
// }

// function closeModal() {
//   const modal = document.getElementById("loginModal")
//   modal.style.display = "none"
// }

// // Demo credentials (in real app, this would be handled by backend)
// const validCredentials = {
//   "admin@znhs.edu": "admin123",
//   "teacher@znhs.edu": "teacher123",
//   "user@gmail.com": "password123",
// }

// function handleLogin(event) {
//   event.preventDefault()

//   const username = document.getElementById("username").value.trim()
//   const password = document.getElementById("password").value

//   // Simple validation
//   if (!username || !password) {
//     showModal("Login Error", "Please fill in all required fields.", false)
//     return
//   }

//   // Simulate login process with loading
//   showModal("Logging In", "Please wait while we verify your credentials...", false)

//   setTimeout(() => {
//     // Check credentials
//     if (validCredentials[username] && validCredentials[username] === password) {
//       // Store login session (simple localStorage for demo)
//       localStorage.setItem("isLoggedIn", "true")
//       localStorage.setItem("username", username)
//       localStorage.setItem("loginTime", new Date().toISOString())

//       showModal("Login Successful", "Welcome! Redirecting to dashboard...", true)

//       // Redirect after 2 seconds
//       setTimeout(() => {
//         window.location.href = "admin.html"
//       }, 2000)
//     } else {
//       showModal("Login Failed", "Invalid username or password. Please try again.", false)
//     }
//   }, 1500)
// }

// // Modal event listeners
// document.addEventListener("DOMContentLoaded", () => {
//   const modal = document.getElementById("loginModal")
//   const closeBtn = document.querySelector(".close")
//   const okBtn = document.getElementById("modalOkBtn")

//   // Close modal when clicking X or OK button
//   closeBtn.onclick = closeModal
//   okBtn.onclick = closeModal

//   // Close modal when clicking outside
//   window.onclick = (event) => {
//     if (event.target === modal) {
//       closeModal()
//     }
//   }

//   // Check if already logged in
//   if (localStorage.getItem("isLoggedIn") === "true") {
//     showModal("Already Logged In", "You are already logged in. Redirecting to dashboard...", true)
//     setTimeout(() => {
//       window.location.href = "admin.html"
//     }, 2000)
//   }
// })


// Password toggle (your existing – kept as-is)
function togglePassword() {
  const passwordField = document.getElementById("password")
  const passwordIcon = document.getElementById("password-icon")

  if (passwordField.type === "password") {
    passwordField.type = "text"
    passwordIcon.textContent = "🙈"
  } else {
    passwordField.type = "password"
    passwordIcon.textContent = "👁️"
  }
}

// Modal functions (your existing – kept, but added auto-close option)
function showModal(title, message, isSuccess = false, autoCloseDelay = 0) {
  const modal = document.getElementById("loginModal")
  const modalTitle = document.getElementById("modalTitle")
  const modalMessage = document.getElementById("modalMessage")

  modalTitle.textContent = title
  modalMessage.textContent = message
  modalMessage.className = isSuccess ? "success-message" : "error-message"

  modal.style.display = "block"

  // Optional auto-close (for success with redirect)
  if (autoCloseDelay > 0) {
    setTimeout(() => {
      closeModal()
    }, autoCloseDelay)
  }
}

function closeModal() {
  const modal = document.getElementById("loginModal")
  modal.style.display = "none"
}

// NEW: CSRF token helper (for secure POST)
function getCSRFToken() {
  const tokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
  return tokenElement ? tokenElement.value : null;
}

// UPDATED: Real AJAX handleLogin (replaces demo simulation)
function handleLogin(event) {
  event.preventDefault()

  const username = document.getElementById("username").value.trim()
  const password = document.getElementById("password").value

  // Simple validation (your existing)
  if (!username || !password) {
    showModal("Login Error", "Please fill in all required fields.", false)
    return
  }

  // Show loading modal (your existing)
  showModal("Logging In", "Please wait while we verify your credentials...", false)

  // Build FormData for POST
  const formData = new FormData()
  formData.append('username', username)
  formData.append('password', password)

  // Append CSRF token if available (requires {% csrf_token %} in form)
  const csrfToken = getCSRFToken()
  if (csrfToken) {
    formData.append('csrfmiddlewaretoken', csrfToken)
  }

  // AJAX POST to backend
  fetch('/login/', {  // Adjust if prefixed (e.g., '/enrollmentprocess/login/')
    method: 'POST',
    body: formData,
    headers: {
      'X-Requested-With': 'XMLHttpRequest',  // Optional: Marks as AJAX
    },
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`)
    }
    return response.json()
  })
  .then(data => {
    if (data.success) {
      // Success: Show welcome modal, then redirect to role-specific URL
      showModal("Login Successful", data.message, true, 2000)  // Auto-close after 2s
      setTimeout(() => {
        window.location.href = data.redirect  // Role-based: /teacher/ or /admin-functionalities/dashboard/
      }, 2000)
    } else {
      // Error: Show in modal
      showModal("Login Failed", data.error, false)
    }
  })
  .catch(error => {
    console.error('Login AJAX error:', error)
    showModal("Connection Error", "Unable to connect to server. Please check your internet and try again.", false)
  })
}

// Modal event listeners (your existing – kept)
document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("loginModal")
  const closeBtn = document.querySelector(".close")
  const okBtn = document.getElementById("modalOkBtn")

  // Close modal when clicking X or OK button
  closeBtn.onclick = closeModal
  okBtn.onclick = closeModal

  // Close modal when clicking outside
  window.onclick = (event) => {
    if (event.target === modal) {
      closeModal()
    }
  }

  // Check if already logged in (updated: Use Django session via AJAX to view)
  // Note: This now calls the view, which returns JSON redirect if authenticated
  fetch('/login/', {  // GET to view – returns JSON if logged in
    method: 'GET',
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
    },
  })
  .then(response => response.json())
  .then(data => {
    if (data.success && data.message === 'Already logged in.') {
      showModal("Already Logged In", "Redirecting to your dashboard...", true, 2000)
      setTimeout(() => {
        window.location.href = data.redirect
      }, 2000)
    }
  })
  .catch(() => {
    // Not logged in or error – do nothing (show form)
  })
})
