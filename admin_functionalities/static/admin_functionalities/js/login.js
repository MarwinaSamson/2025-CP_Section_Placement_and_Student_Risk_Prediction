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
