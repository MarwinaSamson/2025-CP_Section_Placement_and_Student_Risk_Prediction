// // Sample data for sections
// const sectionsData = {
//   STE: [
//     {
//       id: 1,
//       name: "AKATSUKI",
//       adviser: "Pain",
//       location: "Bldg 1 Room 101",
//       students: 35,
//       maxStudents: 40,
//       avatar: "{% static 'admin_functionalities/assets/kakashi.webp'%}",
//     },
//     {
//       id: 2,
//       name: "PHANTOM TROUPE",
//       adviser: "Chrollo",
//       location: "Bldg 1 Room 102",
//       students: 38,
//       maxStudents: 40,
//       avatar: "{% static 'admin_functionalities/assets/secretary.png'%}",
//     },
//   ],
//   SPFL: [
//     {
//       id: 3,
//       name: "KONOHA",
//       adviser: "Kakashi",
//       location: "Bldg 2 Room 201",
//       students: 30,
//       maxStudents: 40,
//       avatar: "../assets/spongebob.jpg",
//     },
//   ],
//   SPTVE: [
//     {
//       id: 4,
//       name: "UCHIHA",
//       adviser: "Itachi",
//       location: "Bldg 2 Room 202",
//       students: 32,
//       maxStudents: 40,
//       avatar: "../assets/spongebob.jpg",
//     },
//   ],
//   OHSP: [],
//   SNED: [
//     {
//       id: 7,
//       name: "SNED ALPHA",
//       adviser: "Senku",
//       location: "Bldg 3 Room 302",
//       students: 25,
//       maxStudents: 30,
//       avatar: "../assets/spongebob.jpg",
//     },
//   ],
//   TOP5: [
//     {
//       id: 5,
//       name: "ELITE ALPHA",
//       adviser: "Madara",
//       location: "Bldg 3 Room 301",
//       students: 40,
//       maxStudents: 40,
//       avatar: "../assets/spongebob.jpg",
//     },
//   ],
//   REGULAR: [
//     {
//       id: 6,
//       name: "REGULAR A",
//       adviser: "Naruto",
//       location: "Bldg 1 Room 103",
//       students: 35,
//       maxStudents: 40,
//       avatar: "../assets/spongebob.jpg",
//     },
//   ],
// }

// let currentProgram = "STE"
// let currentSectionForUpdate = null
// let currentGradeLevel = "7"

// // Initialize the page
// document.addEventListener("DOMContentLoaded", () => {
//   const urlParams = new URLSearchParams(window.location.search)
//   const programParam = urlParams.get("program")

//   if (programParam && sectionsData[programParam]) {
//     currentProgram = programParam
//     console.log("Switching to program from URL:", programParam)

//     // Update active tab immediately
//     document.querySelectorAll(".tab-btn").forEach((btn) => {
//       btn.classList.remove("active")
//     })
//     const targetTab = document.querySelector(`[data-program="${programParam}"]`)
//     if (targetTab) {
//       targetTab.classList.add("active")
//     }
//   }

//   loadSections(currentProgram)
//   setupEventListeners()
// })

// function setupEventListeners() {
//   // Tab switching
//   document.querySelectorAll(".tab-btn").forEach((btn) => {
//     btn.addEventListener("click", function () {
//       const program = this.dataset.program
//       switchProgram(program)
//     })
//   })

//   const gradeLevelSelect = document.getElementById("gradeLevel")
//   if (gradeLevelSelect) {
//     gradeLevelSelect.addEventListener("change", function () {
//       currentGradeLevel = this.value
//       console.log("Grade level changed to:", currentGradeLevel)
//       // You can add logic here to filter sections by grade level if needed
//       // For now, just log the change
//     })
//   }

//   // Close modals when clicking outside
//   window.addEventListener("click", (event) => {
//     if (event.target.classList.contains("modal")) {
//       closeAllModals()
//     }
//   })

//   // Form submissions
//   document.getElementById("addSectionForm").addEventListener("submit", handleAddSection)
//   document.getElementById("updateSectionForm").addEventListener("submit", handleUpdateSection)
// }

// function switchProgram(program) {
//   // Update active tab
//   document.querySelectorAll(".tab-btn").forEach((btn) => {
//     btn.classList.remove("active")
//   })
//   document.querySelector(`[data-program="${program}"]`).classList.add("active")

//   currentProgram = program
//   loadSections(program)

//   const newUrl = new URL(window.location)
//   newUrl.searchParams.set("program", program)
//   window.history.pushState({}, "", newUrl)
// }

// function loadSections(program) {
//   const sectionsGrid = document.getElementById("sectionsGrid")
//   const sections = sectionsData[program] || []

//   if (sections.length === 0) {
//     sectionsGrid.innerHTML = `
//             <div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: #666;">
//                 <i class="fas fa-inbox" style="font-size: 48px; margin-bottom: 15px; display: block;"></i>
//                 <p>No sections found for ${program} program.</p>
//                 <p>Click "Add Section" to create a new section.</p>
//             </div>
//         `
//     return
//   }

//   sectionsGrid.innerHTML = sections
//     .map(
//       (section) => `
//         <div class="section-card">
//             <div class="section-header">
//                 <div class="section-avatar">
//                     <img src="${section.avatar}" alt="${section.name}">
//                 </div>
//                 <div class="section-info">
//                     <h3>Section: ${section.name}</h3>
//                     <p>Adviser: ${section.adviser}</p>
//                     <p>Location: ${section.location}</p>
//                 </div>
//             </div>
//             <div class="section-footer">
//                 <div class="student-count">${section.students}/${section.maxStudents}</div>
//                 <div class="section-menu">
//                     <button class="menu-btn" onclick="toggleDropdown(${section.id})">
//                         <i class="fas fa-ellipsis-v"></i>
//                     </button>
//                     <div class="dropdown-menu" id="dropdown-${section.id}">
//                         <button class="dropdown-item" onclick="assignTeacher(${section.id})">
//                             <i class="fas fa-user-plus"></i> Assign Teacher
//                         </button>
//                         <button class="dropdown-item" onclick="updateSection(${section.id})">
//                             <i class="fas fa-edit"></i> Update
//                         </button>
//                         <button class="dropdown-item" onclick="deleteSection(${section.id})">
//                             <i class="fas fa-trash"></i> Delete
//                         </button>
//                     </div>
//                 </div>
//             </div>
//         </div>
//     `,
//     )
//     .join("")
// }

// function toggleDropdown(sectionId) {
//   // Close all other dropdowns
//   document.querySelectorAll(".dropdown-menu").forEach((menu) => {
//     if (menu.id !== `dropdown-${sectionId}`) {
//       menu.classList.remove("show")
//     }
//   })

//   // Toggle current dropdown
//   const dropdown = document.getElementById(`dropdown-${sectionId}`)
//   dropdown.classList.toggle("show")
// }

// // Close dropdowns when clicking elsewhere
// document.addEventListener("click", (event) => {
//   if (!event.target.closest(".section-menu")) {
//     document.querySelectorAll(".dropdown-menu").forEach((menu) => {
//       menu.classList.remove("show")
//     })
//   }
// })

// // Modal functions
// function openAddSectionModal() {
//   document.getElementById("addSectionModal").style.display = "block"
// }

// function closeAddSectionModal() {
//   document.getElementById("addSectionModal").style.display = "none"
//   document.getElementById("addSectionForm").reset()
// }

// function openSubjectTeacherModal(sectionId) {
//   const section = findSectionById(sectionId)
//   if (section) {
//     document.getElementById("currentSection").textContent = section.name
//     document.getElementById("currentAdviser").textContent = section.adviser
//   }
//   document.getElementById("addSubjectTeacherModal").style.display = "block"
// }

// function closeSubjectTeacherModal() {
//   document.getElementById("addSubjectTeacherModal").style.display = "none"
// }

// function openUpdateSectionModal(sectionId) {
//   const section = findSectionById(sectionId)
//   if (section) {
//     currentSectionForUpdate = section
//     document.getElementById("updateSectionName").value = section.name
//     document.getElementById("updateAdviserName").value = section.adviser
//     document.getElementById("updateLocation").value = section.location
//     document.getElementById("updateSectionModal").style.display = "block"
//   }
// }

// function closeUpdateSectionModal() {
//   document.getElementById("updateSectionModal").style.display = "none"
//   document.getElementById("updateSectionForm").reset()
//   currentSectionForUpdate = null
// }

// function closeAllModals() {
//   document.querySelectorAll(".modal").forEach((modal) => {
//     modal.style.display = "none"
//   })
// }

// // Action functions
// function assignTeacher(sectionId) {
//   toggleDropdown(sectionId) // Close dropdown
//   openSubjectTeacherModal(sectionId)
// }

// function updateSection(sectionId) {
//   toggleDropdown(sectionId) // Close dropdown
//   openUpdateSectionModal(sectionId)
// }

// function deleteSection(sectionId) {
//   toggleDropdown(sectionId) // Close dropdown

//   if (confirm("Are you sure you want to delete this section? This action cannot be undone.")) {
//     // Remove section from data
//     for (const program in sectionsData) {
//       sectionsData[program] = sectionsData[program].filter((section) => section.id !== sectionId)
//     }

//     // Reload current program sections
//     loadSections(currentProgram)

//     // Show success message
//     alert("Section deleted successfully!")
//   }
// }

// // Form handlers
// function handleAddSection(event) {
//   event.preventDefault()

//   const formData = new FormData(event.target)
//   const newSection = {
//     id: Date.now(), // Simple ID generation
//     name: formData.get("sectionName"),
//     adviser: formData.get("adviserName"),
//     location: `Bldg ${formData.get("buildingNumber")} Room ${formData.get("roomNumber")}`,
//     students: 0,
//     maxStudents: 40,
//     avatar: "../assets/spongebob.jpg",
//   }

//   // Add to current program
//   if (!sectionsData[currentProgram]) {
//     sectionsData[currentProgram] = []
//   }
//   sectionsData[currentProgram].push(newSection)

//   // Reload sections and close modal
//   loadSections(currentProgram)
//   closeAddSectionModal()

//   alert("Section added successfully!")
// }

// function handleUpdateSection(event) {
//   event.preventDefault()

//   if (!currentSectionForUpdate) return

//   const formData = new FormData(event.target)

//   // Update section data
//   currentSectionForUpdate.name = formData.get("sectionName")
//   currentSectionForUpdate.adviser = formData.get("adviserName")
//   currentSectionForUpdate.location = formData.get("location")

//   // Reload sections and close modal
//   loadSections(currentProgram)
//   closeUpdateSectionModal()

//   alert("Section updated successfully!")
// }

// function saveSubjectTeachers() {
//   // Here you would typically save the subject teacher assignments
//   // For now, just show a success message
//   alert("Subject teachers assigned successfully!")
//   closeSubjectTeacherModal()
// }

// // Utility functions
// function findSectionById(sectionId) {
//   for (const program in sectionsData) {
//     const section = sectionsData[program].find((s) => s.id === sectionId)
//     if (section) return section
//   }
//   return null
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

// Global vars
let currentProgram = 'STE';
let currentSectionForUpdate = null;
let currentGradeLevel = '7';
let advisers = [];
let subjectTeachers = [];
let buildingsRooms = {};
let sectionsCache = {};

// CSRF helper
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
const CSRF_TOKEN = getCookie('csrftoken');
const BASE_URL = '/admin-functionalities/';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded – Initializing sections.js');
    
    const urlParams = new URLSearchParams(window.location.search);
    const programParam = urlParams.get('program');
    if (programParam) {
        currentProgram = programParam;
        updateActiveTab(programParam);
    }

    // Fetch both adviser list and subject-teacher list separately
    Promise.all([
        fetchAdvisers().then(() => console.log('Advisers fetched')),
        fetchTeachers().then(() => console.log('Teachers fetched')),
        fetchBuildingsRooms().then(() => console.log('Buildings/rooms fetched'))
    ]).then(() => {
        console.log('All data fetched successfully');
        loadSections(currentProgram);
        setupEventListeners();
    });
});

function setupEventListeners() {
    console.log('Setting up event listeners');
    
    // Program tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => switchProgram(btn.dataset.program));
    });

    // Grade level
    const gradeSelect = document.getElementById('gradeLevel');
    if (gradeSelect) {
        gradeSelect.addEventListener('change', () => {
            currentGradeLevel = gradeSelect.value;
            console.log('Grade level changed to:', currentGradeLevel);
        });
    }

    // Close modals on outside click
    window.addEventListener('click', (event) => {
        if (event.target.classList.contains('modal')) {
            closeAllModals();
        }
    });

    // Form submissions
    document.getElementById('addSectionForm').addEventListener('submit', handleAddSection);
    document.getElementById('updateSectionForm').addEventListener('submit', handleUpdateSection);
    document.getElementById('addSubjectTeacherForm').addEventListener('submit', handleAssignSubjectTeachers);
    
    // Building change listeners (for add modal)
    const addBuildingSelect = document.getElementById('buildingNumber');
    if (addBuildingSelect) {
        addBuildingSelect.addEventListener('change', function() {
            populateRoomSelectById('roomNumber', this.value);
        });
    }
    
    // Building change listeners (for update modal)
    const updateBuildingSelect = document.getElementById('updateBuilding');
    if (updateBuildingSelect) {
        updateBuildingSelect.addEventListener('change', function() {
            populateRoomSelectById('updateRoom', this.value);
        });
    }
}

function updateActiveTab(program) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    const targetTab = document.querySelector(`[data-program="${program}"]`);
    if (targetTab) targetTab.classList.add('active');
}

function switchProgram(program) {
    console.log(`Switching program to: ${program}`);
    updateActiveTab(program);
    currentProgram = program;
    loadSections(program);
    const newUrl = new URL(window.location);
    newUrl.searchParams.set("program", program);
    window.history.pushState({}, "", newUrl);
}

function fetchTeachers() {
    return fetch(`${BASE_URL}api/get-subject-teachers/`)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            console.log('Fetched subject teachers by department:', data);
            subjectTeachers = data.teachers || [];
            populateSubjectTeacherSelects();
        })
        .catch(error => console.error('Error fetching teachers:', error));
}

function fetchAdvisers() {
    return fetch(`${BASE_URL}api/get-teachers/`)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            console.log('Fetched advisers data:', data);
            advisers = data.advisers || [];
            populateAdviserSelects();
        })
        .catch(error => console.error('Error fetching advisers:', error));
}

function fetchBuildingsRooms() {
    return fetch(`${BASE_URL}api/buildings-rooms/`)  // FIXED: Updated to new API path
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            console.log('Fetched buildings and rooms:', data);
            buildingsRooms = data.rooms || {};
            populateBuildingSelects();
        })
        .catch(error => console.error('Error fetching buildings/rooms:', error));
}

function populateAdviserSelects(currentAdviserId = null) {
    console.log('Populating adviser selects with:', advisers);
    const adviserSelects = [
        document.getElementById('adviserName'),
        document.getElementById('updateAdviserName')
    ];

    adviserSelects.forEach(select => {
        if (select) {
            select.innerHTML = '<option value="">Select Adviser</option>';

            advisers.forEach(adviser => {
                const option = document.createElement('option');
                option.value = adviser.id;
                option.textContent = adviser.name;

                // Disable if already assigned to another section (except current adviser)
                if (adviser.isAssigned && adviser.id != currentAdviserId) {
                    option.disabled = true;
                    option.textContent += ' (Unavailable)';
                }

                select.appendChild(option);
            });
        }
    });
}


function populateSubjectTeacherSelects() {
    console.log('Populating subject teacher selects with department filtering:', subjectTeachers);

    // Map subjects to their required department
    const subjectDepartmentMap = {
        'mathTeacher': 'Mathematics',
        'englishTeacher': 'English',
        'scienceTeacher': 'Science',
        'filipinoTeacher': 'Filipino',
        'arpanTeacher': 'Social Studies',
        'mapehTeacher': 'MAPEH',
        'espTeacher': 'Values Education'
    };

    Object.entries(subjectDepartmentMap).forEach(([selectId, department]) => {
        const select = document.getElementById(selectId);
        if (select) {
            select.innerHTML = '<option value="">Select Teacher</option>';

            const filteredTeachers = subjectTeachers.filter(t =>t.department && t.department.toLowerCase().includes(department.toLowerCase()));


            if (filteredTeachers.length === 0) {
                const opt = document.createElement('option');
                opt.disabled = true;
                opt.textContent = `No ${department} teachers available`;
                select.appendChild(opt);
            } else {
                filteredTeachers.forEach(teacher => {
                    const option = document.createElement('option');
                    option.value = teacher.id;
                    option.textContent = `${teacher.name}`;
                    select.appendChild(option);
                });
            }
        }
    });
}


function populateBuildingSelects() {
    console.log('Populating building selects with:', buildingsRooms);
    const buildingSelects = [
        document.getElementById('buildingNumber'),
        document.getElementById('updateBuilding')
    ];
    
    buildingSelects.forEach(select => {
        if (select) {
            select.innerHTML = '<option value="">Select Building</option>';
            for (const building in buildingsRooms) {
                const option = document.createElement('option');
                option.value = building;
                option.textContent = building.replace('building', 'Building ');
                select.appendChild(option);
            }
        }
    });
}

function populateRoomSelectById(roomSelectId, buildingValue) {
    const roomSelect = document.getElementById(roomSelectId);
    if (roomSelect) {
        roomSelect.innerHTML = '<option value="">Select Room</option>';
        if (buildingsRooms[buildingValue]) {
            buildingsRooms[buildingValue].forEach(room => {
                const option = document.createElement('option');
                option.value = room;
                option.textContent = room;
                roomSelect.appendChild(option);
            });
        }
    }
}

function loadSections(program) {
    console.log(`Loading sections for program: ${program}`);
    fetch(`${BASE_URL}sections/${program}/`)
        .then(response => response.json())
        .then(data => {
            console.log('Sections data received:', data);
            sectionsCache[program] = data.sections;
            const sectionsGrid = document.getElementById('sectionsGrid');
            
            if (data.sections.length === 0) {
                sectionsGrid.innerHTML = `
                    <div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: #666;">
                        <i class="fas fa-inbox" style="font-size: 48px; margin-bottom: 15px; display: block;"></i>
                        <p>No sections found for ${program} program.</p>
                        <p>Click "Add Section" to create a new section.</p>
                    </div>
                `;
                return;
            }
            
            sectionsGrid.innerHTML = data.sections.map(section => `
                <div class="section-card" >
                    <div class="section-header" onclick="openSectionMasterlist(${section.id})">
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
                            <div class="dropdown-menu" id="dropdown-${section.id}" style="display: none;">
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
            `).join('');
        })
        .catch(error => console.error('Error loading sections:', error));
}

function openAddSectionModal() {
    console.log('Opening Add Section Modal');
    document.getElementById('addSectionModal').style.display = 'block';
    populateAdviserSelects();
    populateBuildingSelects();
}

function closeAddSectionModal() {
    document.getElementById('addSectionModal').style.display = 'none';
    document.getElementById('addSectionForm').reset();
}

function openSubjectTeacherModal(sectionId) {
    console.log('Opening Subject Teacher Modal for section ID:', sectionId);
    const section = findSectionById(sectionId);
    if (section) {
        document.getElementById('currentSection').textContent = section.name;
        document.getElementById('currentAdviser').textContent = section.adviser;
    }
    document.getElementById('addSubjectTeacherModal').style.display = 'block';
    populateSubjectTeacherSelects();
}

function closeSubjectTeacherModal() {
    document.getElementById('addSubjectTeacherModal').style.display = 'none';
    document.getElementById('addSubjectTeacherForm').reset();
}

function openUpdateSectionModal(sectionId) {
    console.log('Opening Update Section Modal for section ID:', sectionId);
    const section = findSectionById(sectionId);
    if (!section) return;

    currentSectionForUpdate = section;

    // Populate selects first
    populateAdviserSelects(section.adviserId);
    populateBuildingSelects();

    // Fill form fields
    document.getElementById('updateSectionName').value = section.name;
    document.getElementById('updateAdviserName').value = section.adviserId || '';
    document.getElementById('updateMaxStudents').value = section.maxStudents;

    // Parse and set building + room
    const locationMatch = section.location.match(/Bldg (\d+) Room (.+)/);
    if (locationMatch) {
        const building = `building${locationMatch[1]}`;
        const room = locationMatch[2];
        document.getElementById('updateBuilding').value = building;
        populateRoomSelectById('updateRoom', building);
        setTimeout(() => {
            document.getElementById('updateRoom').value = room;
        }, 50);
    }

    // Open modal
    document.getElementById('updateSectionModal').style.display = 'block';
}

function closeUpdateSectionModal() {
    document.getElementById('updateSectionModal').style.display = 'none';
    document.getElementById('updateSectionForm').reset();
    currentSectionForUpdate = null;
}

function closeAllModals() {
    document.querySelectorAll('.modal').forEach(modal => modal.style.display = 'none');
}

function handleAddSection(event) {
    event.preventDefault();
    const formData = new FormData(event.target);

    fetch(`${BASE_URL}sections/add/${currentProgram}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Add section response:', data);
        if (data.success) {
            alert(data.message);
            loadSections(currentProgram);
            closeAddSectionModal();
        } else {
            alert(`Error: ${data.message}\nDetails: ${JSON.stringify(data.errors)}`);
        }
    })
    .catch(error => {
        console.error('Error adding section:', error);
        alert('An error occurred while adding the section.');
    });
}

function handleUpdateSection(event) {
    event.preventDefault();
    if (!currentSectionForUpdate) return;

    const formData = new FormData(event.target);

    fetch(`${BASE_URL}sections/update/${currentSectionForUpdate.id}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Update section response:', data);
        if (data.success) {
            alert(data.message);
            loadSections(currentProgram);
            closeUpdateSectionModal();
        } else {
            alert(`Error: ${data.message}\nDetails: ${JSON.stringify(data.errors)}`);
        }
    })
    .catch(error => {
        console.error('Error updating section:', error);
        alert('An error occurred while updating the section.');
    });
}

function assignTeacher(sectionId) {
    currentSectionForUpdate = findSectionById(sectionId);
    openSubjectTeacherModal(sectionId);
}

function updateSection(sectionId) {
    openUpdateSectionModal(sectionId);
}

function deleteSection(sectionId) {
    if (confirm("Are you sure you want to delete this section? This action cannot be undone.")) {
        fetch(`${BASE_URL}sections/delete/${sectionId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': CSRF_TOKEN
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Delete section response:', data);
            if (data.success) {
                alert(data.message);
                loadSections(currentProgram);
            } else {
                alert(`Error: ${data.message}`);
            }
        })
        .catch(error => {
            console.error('Error deleting section:', error);
            alert('An error occurred while deleting the section.');
        });
    }
}

function openSectionMasterlist(sectionId) {
    // Simply redirect to Django-rendered masterlist page
    window.location.href = `${BASE_URL}sections/${sectionId}/masterlist/`;
}

function handleAssignSubjectTeachers(event) {
    event.preventDefault();
    
    if (!currentSectionForUpdate) {
        alert('No section selected. Please try again.');
        return;
    }
    
    const assignments = [];
    const subjectMapping = {
        'math': 'MATHEMATICS',
        'english': 'ENGLISH',
        'science': 'SCIENCE',
        'filipino': 'FILIPINO',
        'arpan': 'ARALING_PANLIPUNAN',
        'mapeh': 'MAPEH',
        'esp': 'EDUKASYON_SA_PAGPAPAKATAO'
    };
    
    for (const [prefix, subjectName] of Object.entries(subjectMapping)) {
        const teacherSelect = document.getElementById(`${prefix}Teacher`);
        const daySelect = document.getElementById(`${prefix}Day`);
        const startTime = document.getElementById(`${prefix}Time`);
        const endTime = document.getElementById(`${prefix}TimeEnd`);
        
        if (teacherSelect && daySelect && startTime && endTime && teacherSelect.value) {
            assignments.push({
                subject: subjectName,
                teacher_id: teacherSelect.value,
                day: daySelect.value,
                start_time: startTime.value,
                end_time: endTime.value
            });
        }
    }

    if (assignments.length === 0) {
        alert('No assignments to save. Please select at least one teacher.');
        return;
    }

    fetch(`${BASE_URL}sections/assign-subjects/${currentSectionForUpdate.id}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN
        },
        body: JSON.stringify({assignments})
    })
    .then(response => response.json())
    .then(data => {
        console.log('Assign subject teachers response:', data);
        if (data.success) {
            alert(data.message);
            closeSubjectTeacherModal();
            loadSections(currentProgram);
        } else {
            alert(`Error: ${data.message}\nDetails: ${JSON.stringify(data.errors)}`);
        }
    })
    .catch(error => {
        console.error('Error assigning subject teachers:', error);
        alert('An error occurred while assigning teachers.');
    });
}

function toggleDropdown(sectionId) {
    // Close all other dropdowns first
    document.querySelectorAll('.dropdown-menu').forEach(menu => {
        if (menu.id !== `dropdown-${sectionId}`) {
            menu.style.display = 'none';
        }
    });
    
    // Toggle current dropdown
    const dropdown = document.getElementById(`dropdown-${sectionId}`);
    if (dropdown) {
        const isHidden = dropdown.style.display === 'none' || dropdown.style.display === '';
        dropdown.style.display = isHidden ? 'block' : 'none';
    }
}

function handleLogout() {
    if (confirm('Are you sure you want to logout?')) {
        window.location.href = "/logout/";  // Adjust to your logout URL
    }
}

function findSectionById(sectionId) {
    if (sectionsCache[currentProgram]) {
        return sectionsCache[currentProgram].find(section => section.id == sectionId) || null;
    }
    return null;
}

// Close dropdowns when clicking outside
document.addEventListener('click', function(event) {
    if (!event.target.closest('.section-menu')) {
        document.querySelectorAll('.dropdown-menu').forEach(menu => {
            menu.style.display = 'none';
        });
    }
});

// Search functionality (optional enhancement)
const searchInput = document.querySelector('.search-input');
if (searchInput) {
    searchInput.addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        const sectionCards = document.querySelectorAll('.section-card');
        
        sectionCards.forEach(card => {
            const sectionName = card.querySelector('.section-info h3').textContent.toLowerCase();
            const adviserName = card.querySelector('.section-info p:nth-child(2)').textContent.toLowerCase();
            
            if (sectionName.includes(searchTerm) || adviserName.includes(searchTerm)) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    });
}