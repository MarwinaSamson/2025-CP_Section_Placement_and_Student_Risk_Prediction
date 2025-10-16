// document.addEventListener("DOMContentLoaded", () => {
//   // Update dashboard date
//   updateDashboardDate();
//   // Handle dropdown changes
//   setupDropdownHandlers();
//   // Setup logout handler
//   setupLogoutHandler();
//   const programRows = document.querySelectorAll(".program-row");
//   programRows.forEach((row) => {
//     row.addEventListener("click", () => {
//       const program = row.getAttribute("data-program");
//       console.log("Clicking program row:", program);
//       window.location.href = `sections.html?program=${program}`;
//     });
//   });
// });

// /**
//  * Updates the dashboard date and school year display.
//  */
// function updateDashboardDate() {
//   const dateElement = document.getElementById("dashboardDate")
//   if (dateElement) {
//     const now = new Date()
//     const options = {
//       year: "numeric",
//       month: "long",
//       day: "numeric",
//     }
//     const formattedDate = now.toLocaleDateString("en-US", options)
//     const schoolYear = "2025-2026" // Simulating a fixed school year
//     dateElement.textContent = `${formattedDate} | ${schoolYear}`
//   }
// }

// /**
//  * Sets up event handlers for the dashboard dropdowns.
//  */
// function setupDropdownHandlers() {
//   const gradeLevel = document.getElementById("gradeLevelFilter")
//   const schoolYear = document.getElementById("schoolYearFilter")

//   if (gradeLevel) {
//     gradeLevel.addEventListener("change", function () {
//       console.log("Grade level changed to:", this.value)
//       // Update statistics based on grade level
//       showNotification(`Statistics updated for Grade ${this.value}`, "success")
//     })
//   }

//   if (schoolYear) {
//     schoolYear.addEventListener("change", function () {
//       console.log("School year changed to:", this.value)
//       // Update data based on school year
//       showNotification(`Data updated for school year ${this.value}`, "success")
//     })
//   }
// }

// /**
//  * Creates and displays a notification element.
//  * @param {string} message - The message to display.
//  * @param {string} type - The type of notification (e.g., 'success', 'info', 'warning').
//  */
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

// function setupLogoutHandler() {
//   const logoutBtn = document.querySelector(".logout-btn");
//   if (logoutBtn) {
//     logoutBtn.addEventListener("click", (e) => {
//       e.preventDefault(); // Prevent default link navigation
//       // Clear session/local storage if you use it
//       localStorage.removeItem("isLoggedIn");
//       localStorage.removeItem("username");
//       localStorage.removeItem("loginTime");
//       // Show logout notification
//       showNotification("Logging out...", "info");
//       // Redirect to logout URL after 1 second
//       setTimeout(() => {
//         window.location.href = logoutUrl; // Use the URL passed from Django template
//       }, 1000);
//     });
//   }
// }


// // Sidebar navigation
// document.querySelectorAll(".nav-link").forEach((link) => {
//   link.addEventListener("click", function (e) {
//     // Remove active class from all nav items
//     document.querySelectorAll(".nav-item").forEach((item) => {
//       item.classList.remove("active")
//     })

//     // Add active class to clicked item
//     this.closest(".nav-item").classList.add("active")

//     const section = this.querySelector("span").textContent
//     console.log("Navigating to:", section)

//     // Allow the default link behavior to proceed
//   })
// })

//   document.querySelectorAll('.has-submenu').forEach(item => {
//       item.addEventListener('click', (e) => {
//           e.preventDefault();
//           item.classList.toggle('active');
//       });
//   });
  
document.addEventListener("DOMContentLoaded", () => {
  // Update dashboard date
  updateDashboardDate();
  // Handle dropdown changes
  setupDropdownHandlers();
  // Setup logout handler (fixed)
  setupLogoutHandler();
  const programRows = document.querySelectorAll(".program-row");
  programRows.forEach((row) => {
    row.addEventListener("click", () => {
      const program = row.getAttribute("data-program");
      console.log("Clicking program row:", program);
      window.location.href = `sections.html?program=${program}`;
    });
  });
});

/**
 * Updates the dashboard date and school year display.
 */
function updateDashboardDate() {
  const dateElement = document.getElementById("dashboardDate")
  if (dateElement) {
    const now = new Date()
    const options = {
      year: "numeric",
      month: "long",
      day: "numeric",
    }
    const formattedDate = now.toLocaleDateString("en-US", options)
    const schoolYear = "2025-2026" // Simulating a fixed school year
    dateElement.textContent = `${formattedDate} | ${schoolYear}`
  }
}

/**
 * Sets up event handlers for the dashboard dropdowns.
 */
function setupDropdownHandlers() {
  const gradeLevel = document.getElementById("gradeLevelFilter")
  const schoolYear = document.getElementById("schoolYearFilter")

  if (gradeLevel) {
    gradeLevel.addEventListener("change", function () {
      console.log("Grade level changed to:", this.value)
      // Update statistics based on grade level
      showNotification(`Statistics updated for Grade ${this.value}`, "success")
    })
  }

  if (schoolYear) {
    schoolYear.addEventListener("change", function () {
      console.log("School year changed to:", this.value)
      // Update data based on school year
      showNotification(`Data updated for school year ${this.value}`, "success")
    })
  }
}

/**
 * Creates and displays a notification element.
 * @param {string} message - The message to display.
 * @param {string} type - The type of notification (e.g., 'success', 'info', 'warning').
 */
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

/**
 * FIXED: Setup logout handler – confirms, shows notification, redirects to /logout/ → /login/
 */
function setupLogoutHandler() {
  const logoutBtn = document.querySelector(".logout-btn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", (e) => {
      e.preventDefault(); // Block default link (we'll handle redirect in JS for UX)

      // Confirmation dialog (prevents accidental logout)
      if (!confirm("Are you sure you want to log out? You will be redirected to the login page.")) {
        console.log("Logout cancelled by user");
        return; // Cancel if no
      }

      // Clear client-side storage (good practice)
      localStorage.removeItem("isLoggedIn");
      localStorage.removeItem("username");
      localStorage.removeItem("loginTime");

      // Show logout notification
      showNotification("Logging out...", "info");

      // Redirect to /logout/ (server clears session and redirects to /login/)
      console.log("Redirecting to:", window.logoutUrl || '/logout/');  // Fallback if not passed
      setTimeout(() => {
        window.location.href = window.logoutUrl || '/logout/';  // Uses Django-passed URL or fallback
      }, 1000);  // 1s delay for notification visibility
    });
  } else {
    console.warn("Logout button (.logout-btn) not found in template");
  }
}

// Sidebar navigation (your existing – kept)
document.querySelectorAll(".nav-link").forEach((link) => {
  link.addEventListener("click", function (e) {
    // Remove active class from all nav items
    document.querySelectorAll(".nav-item").forEach((item) => {
      item.classList.remove("active")
    })

    // Add active class to clicked item
    this.closest(".nav-item").classList.add("active")

    const section = this.querySelector("span").textContent
    console.log("Navigating to:", section)

    // Allow the default link behavior to proceed
  })
});

// Submenu toggle (your existing – kept)
document.querySelectorAll('.has-submenu').forEach(item => {
  item.addEventListener('click', (e) => {
    e.preventDefault();
    item.classList.toggle('active');
  });
});
