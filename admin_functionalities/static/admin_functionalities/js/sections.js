// Sample data for sections
const sectionsData = {
  STE: [
    {
      id: 1,
      name: "AKATSUKI",
      adviser: "Pain",
      location: "Bldg 1 Room 101",
      students: 35,
      maxStudents: 40,
      avatar: "../assets/kakashi.webp",
    },
    {
      id: 2,
      name: "PHANTOM TROUPE",
      adviser: "Chrollo",
      location: "Bldg 1 Room 102",
      students: 38,
      maxStudents: 40,
      avatar: "../assets/secretary.png",
    },
  ],
  SPFL: [
    {
      id: 3,
      name: "KONOHA",
      adviser: "Kakashi",
      location: "Bldg 2 Room 201",
      students: 30,
      maxStudents: 40,
      avatar: "../assets/spongebob.jpg",
    },
  ],
  SPTVE: [
    {
      id: 4,
      name: "UCHIHA",
      adviser: "Itachi",
      location: "Bldg 2 Room 202",
      students: 32,
      maxStudents: 40,
      avatar: "../assets/spongebob.jpg",
    },
  ],
  OHSP: [],
  SNED: [
    {
      id: 7,
      name: "SNED ALPHA",
      adviser: "Senku",
      location: "Bldg 3 Room 302",
      students: 25,
      maxStudents: 30,
      avatar: "../assets/spongebob.jpg",
    },
  ],
  TOP5: [
    {
      id: 5,
      name: "ELITE ALPHA",
      adviser: "Madara",
      location: "Bldg 3 Room 301",
      students: 40,
      maxStudents: 40,
      avatar: "../assets/spongebob.jpg",
    },
  ],
  REGULAR: [
    {
      id: 6,
      name: "REGULAR A",
      adviser: "Naruto",
      location: "Bldg 1 Room 103",
      students: 35,
      maxStudents: 40,
      avatar: "../assets/spongebob.jpg",
    },
  ],
}

let currentProgram = "STE"
let currentSectionForUpdate = null
let currentGradeLevel = "7"

// Initialize the page
document.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search)
  const programParam = urlParams.get("program")

  if (programParam && sectionsData[programParam]) {
    currentProgram = programParam
    console.log("Switching to program from URL:", programParam)

    // Update active tab immediately
    document.querySelectorAll(".tab-btn").forEach((btn) => {
      btn.classList.remove("active")
    })
    const targetTab = document.querySelector(`[data-program="${programParam}"]`)
    if (targetTab) {
      targetTab.classList.add("active")
    }
  }

  loadSections(currentProgram)
  setupEventListeners()
})

function setupEventListeners() {
  // Tab switching
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      const program = this.dataset.program
      switchProgram(program)
    })
  })

  const gradeLevelSelect = document.getElementById("gradeLevel")
  if (gradeLevelSelect) {
    gradeLevelSelect.addEventListener("change", function () {
      currentGradeLevel = this.value
      console.log("Grade level changed to:", currentGradeLevel)
      // You can add logic here to filter sections by grade level if needed
      // For now, just log the change
    })
  }

  // Close modals when clicking outside
  window.addEventListener("click", (event) => {
    if (event.target.classList.contains("modal")) {
      closeAllModals()
    }
  })

  // Form submissions
  document.getElementById("addSectionForm").addEventListener("submit", handleAddSection)
  document.getElementById("updateSectionForm").addEventListener("submit", handleUpdateSection)
}

function switchProgram(program) {
  // Update active tab
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.classList.remove("active")
  })
  document.querySelector(`[data-program="${program}"]`).classList.add("active")

  currentProgram = program
  loadSections(program)

  const newUrl = new URL(window.location)
  newUrl.searchParams.set("program", program)
  window.history.pushState({}, "", newUrl)
}

function loadSections(program) {
  const sectionsGrid = document.getElementById("sectionsGrid")
  const sections = sectionsData[program] || []

  if (sections.length === 0) {
    sectionsGrid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: #666;">
                <i class="fas fa-inbox" style="font-size: 48px; margin-bottom: 15px; display: block;"></i>
                <p>No sections found for ${program} program.</p>
                <p>Click "Add Section" to create a new section.</p>
            </div>
        `
    return
  }

  sectionsGrid.innerHTML = sections
    .map(
      (section) => `
        <div class="section-card">
            <div class="section-header">
                <div class="section-avatar">
                    <img src="${section.avatar}" alt="${section.name}">
                </div>
                <div class="section-info">
                    <h3>Section: ${section.name}</h3>
                    <p>Adviser: ${section.adviser}</p>
                    <p>Location: ${section.location}</p>
                </div>
            </div>
            <div class="section-footer">
                <div class="student-count">${section.students}/${section.maxStudents}</div>
                <div class="section-menu">
                    <button class="menu-btn" onclick="toggleDropdown(${section.id})">
                        <i class="fas fa-ellipsis-v"></i>
                    </button>
                    <div class="dropdown-menu" id="dropdown-${section.id}">
                        <button class="dropdown-item" onclick="assignTeacher(${section.id})">
                            <i class="fas fa-user-plus"></i> Assign Teacher
                        </button>
                        <button class="dropdown-item" onclick="updateSection(${section.id})">
                            <i class="fas fa-edit"></i> Update
                        </button>
                        <button class="dropdown-item" onclick="deleteSection(${section.id})">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `,
    )
    .join("")
}

function toggleDropdown(sectionId) {
  // Close all other dropdowns
  document.querySelectorAll(".dropdown-menu").forEach((menu) => {
    if (menu.id !== `dropdown-${sectionId}`) {
      menu.classList.remove("show")
    }
  })

  // Toggle current dropdown
  const dropdown = document.getElementById(`dropdown-${sectionId}`)
  dropdown.classList.toggle("show")
}

// Close dropdowns when clicking elsewhere
document.addEventListener("click", (event) => {
  if (!event.target.closest(".section-menu")) {
    document.querySelectorAll(".dropdown-menu").forEach((menu) => {
      menu.classList.remove("show")
    })
  }
})

// Modal functions
function openAddSectionModal() {
  document.getElementById("addSectionModal").style.display = "block"
}

function closeAddSectionModal() {
  document.getElementById("addSectionModal").style.display = "none"
  document.getElementById("addSectionForm").reset()
}

function openSubjectTeacherModal(sectionId) {
  const section = findSectionById(sectionId)
  if (section) {
    document.getElementById("currentSection").textContent = section.name
    document.getElementById("currentAdviser").textContent = section.adviser
  }
  document.getElementById("addSubjectTeacherModal").style.display = "block"
}

function closeSubjectTeacherModal() {
  document.getElementById("addSubjectTeacherModal").style.display = "none"
}

function openUpdateSectionModal(sectionId) {
  const section = findSectionById(sectionId)
  if (section) {
    currentSectionForUpdate = section
    document.getElementById("updateSectionName").value = section.name
    document.getElementById("updateAdviserName").value = section.adviser
    document.getElementById("updateLocation").value = section.location
    document.getElementById("updateSectionModal").style.display = "block"
  }
}

function closeUpdateSectionModal() {
  document.getElementById("updateSectionModal").style.display = "none"
  document.getElementById("updateSectionForm").reset()
  currentSectionForUpdate = null
}

function closeAllModals() {
  document.querySelectorAll(".modal").forEach((modal) => {
    modal.style.display = "none"
  })
}

// Action functions
function assignTeacher(sectionId) {
  toggleDropdown(sectionId) // Close dropdown
  openSubjectTeacherModal(sectionId)
}

function updateSection(sectionId) {
  toggleDropdown(sectionId) // Close dropdown
  openUpdateSectionModal(sectionId)
}

function deleteSection(sectionId) {
  toggleDropdown(sectionId) // Close dropdown

  if (confirm("Are you sure you want to delete this section? This action cannot be undone.")) {
    // Remove section from data
    for (const program in sectionsData) {
      sectionsData[program] = sectionsData[program].filter((section) => section.id !== sectionId)
    }

    // Reload current program sections
    loadSections(currentProgram)

    // Show success message
    alert("Section deleted successfully!")
  }
}

// Form handlers
function handleAddSection(event) {
  event.preventDefault()

  const formData = new FormData(event.target)
  const newSection = {
    id: Date.now(), // Simple ID generation
    name: formData.get("sectionName"),
    adviser: formData.get("adviserName"),
    location: `Bldg ${formData.get("buildingNumber")} Room ${formData.get("roomNumber")}`,
    students: 0,
    maxStudents: 40,
    avatar: "../assets/spongebob.jpg",
  }

  // Add to current program
  if (!sectionsData[currentProgram]) {
    sectionsData[currentProgram] = []
  }
  sectionsData[currentProgram].push(newSection)

  // Reload sections and close modal
  loadSections(currentProgram)
  closeAddSectionModal()

  alert("Section added successfully!")
}

function handleUpdateSection(event) {
  event.preventDefault()

  if (!currentSectionForUpdate) return

  const formData = new FormData(event.target)

  // Update section data
  currentSectionForUpdate.name = formData.get("sectionName")
  currentSectionForUpdate.adviser = formData.get("adviserName")
  currentSectionForUpdate.location = formData.get("location")

  // Reload sections and close modal
  loadSections(currentProgram)
  closeUpdateSectionModal()

  alert("Section updated successfully!")
}

function saveSubjectTeachers() {
  // Here you would typically save the subject teacher assignments
  // For now, just show a success message
  alert("Subject teachers assigned successfully!")
  closeSubjectTeacherModal()
}

// Utility functions
function findSectionById(sectionId) {
  for (const program in sectionsData) {
    const section = sectionsData[program].find((s) => s.id === sectionId)
    if (section) return section
  }
  return null
}

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