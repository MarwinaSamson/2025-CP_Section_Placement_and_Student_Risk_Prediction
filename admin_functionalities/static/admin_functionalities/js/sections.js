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

    // FIX: Add close button event listeners
    document.querySelectorAll('.close-btn, [onclick*="close"]').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            closeAllModals();
        });
    });

    // FIX: Close modals when clicking outside
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('modal')) {
            closeAllModals();
        }
    });

    // FIX: Close modals with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeAllModals();
        }
    });
}

function updateActiveTab(program) {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active', 'bg-red-700', 'text-white', 'border-red-700');
        btn.classList.add('bg-white', 'text-gray-600', 'border-gray-300');
    });
    const targetTab = document.querySelector(`[data-program="${program}"]`);
    if (targetTab) {
        targetTab.classList.add('active', 'bg-red-700', 'text-white', 'border-red-700');
        targetTab.classList.remove('bg-white', 'text-gray-600', 'border-gray-300');
    }
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
    return fetch(`${BASE_URL}api/buildings-rooms/`)
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

            const filteredTeachers = subjectTeachers.filter(t => t.department && t.department.toLowerCase().includes(department.toLowerCase()));

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
                    <div class="col-span-full text-center py-16">
                        <div class="w-24 h-24 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center mx-auto mb-6">
                            <i class="fas fa-inbox text-3xl text-gray-400"></i>
                        </div>
                        <h3 class="text-xl font-semibold text-gray-600 mb-2">No Sections Found</h3>
                        <p class="text-gray-500 mb-4">No sections available for ${program} program.</p>
                        <button class="gradient-bg text-white px-6 py-3 rounded-xl hover:shadow-lg transform hover:scale-105 transition-all duration-300 font-semibold" onclick="openAddSectionModal()">
                            <i class="fas fa-plus-circle mr-2"></i>Create First Section
                        </button>
                    </div>
                `;
                return;
            }
            
            sectionsGrid.innerHTML = data.sections.map(section => `
                <div class="bg-gradient-to-br from-white to-gray-50 rounded-2xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                    <div class="p-6">
                        <div class="flex items-start justify-between mb-4">
                            <div class="flex items-center gap-4">
                                <div class="w-14 h-14 bg-gradient-to-br from-red-500 to-red-600 rounded-xl flex items-center justify-center shadow-lg">
                                    <i class="fas fa-users text-white text-lg"></i>
                                </div>
                                <div class="flex-1">
                                    <h3 class="text-xl font-bold text-gray-800">${section.name}</h3>
                                    <p class="text-sm text-gray-600 flex items-center gap-1 mt-1">
                                        <i class="fas fa-user-graduate text-red-500"></i>
                                        ${section.adviser}
                                    </p>
                                </div>
                            </div>
                            <div class="relative">
                                <button class="menu-btn w-10 h-10 flex items-center justify-center text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-xl transition-all duration-300" onclick="event.stopPropagation(); toggleDropdown(${section.id})">
                                    <i class="fas fa-ellipsis-v text-lg"></i>
                                </button>
                                <div class="dropdown-menu absolute top-12 right-0 bg-white rounded-xl shadow-2xl border border-gray-200 z-20 min-w-48 py-2 hidden animate-fade-in" id="dropdown-${section.id}">
                                    <button class="dropdown-item w-full text-left px-4 py-3 hover:bg-blue-50 transition-all duration-200 flex items-center gap-3 group" onclick="assignTeacher(${section.id}, event)">
                                        <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center group-hover:bg-blue-200 transition-colors">
                                            <i class="fas fa-user-plus text-blue-600 text-sm"></i>
                                        </div>
                                        <div>
                                            <div class="font-semibold text-gray-700">Assign Teacher</div>
                                            <div class="text-xs text-gray-500">Assign subject teachers</div>
                                        </div>
                                    </button>
                                    <button class="dropdown-item w-full text-left px-4 py-3 hover:bg-green-50 transition-all duration-200 flex items-center gap-3 group" onclick="updateSection(${section.id}, event)">
                                        <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center group-hover:bg-green-200 transition-colors">
                                            <i class="fas fa-edit text-green-600 text-sm"></i>
                                        </div>
                                        <div>
                                            <div class="font-semibold text-gray-700">Update</div>
                                            <div class="text-xs text-gray-500">Edit section details</div>
                                        </div>
                                    </button>
                                    <div class="border-t border-gray-100 my-1"></div>
                                    <button class="dropdown-item w-full text-left px-4 py-3 hover:bg-red-50 transition-all duration-200 flex items-center gap-3 group text-red-600" onclick="deleteSection(${section.id}, event)">
                                        <div class="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center group-hover:bg-red-200 transition-colors">
                                            <i class="fas fa-trash text-red-600 text-sm"></i>
                                        </div>
                                        <div>
                                            <div class="font-semibold">Delete</div>
                                            <div class="text-xs text-red-500">Remove this section</div>
                                        </div>
                                    </button>
                                </div>
                            </div>
                        </div>
                        
                        <div class="space-y-3">
                            <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                <div class="flex items-center gap-2">
                                    <i class="fas fa-map-marker-alt text-gray-400"></i>
                                    <span class="text-sm font-medium text-gray-600">Location</span>
                                </div>
                                <span class="text-sm font-semibold text-gray-800">${section.location}</span>
                            </div>
                            
                            <div class="flex items-center justify-between p-3 bg-gradient-to-r from-red-50 to-pink-50 rounded-lg border border-red-100">
                                <div class="flex items-center gap-2">
                                    <i class="fas fa-users text-red-400"></i>
                                    <span class="text-sm font-medium text-red-600">Students</span>
                                </div>
                                <div class="text-right">
                                    <div class="text-lg font-bold text-red-600">${section.students}/${section.maxStudents}</div>
                                    <div class="w-24 h-2 bg-red-200 rounded-full overflow-hidden">
                                        <div class="h-full bg-red-500 rounded-full" style="width: ${(section.students / section.maxStudents) * 100}%"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-gray-50 px-6 py-3 border-t border-gray-200">
                        <button class="w-full text-center text-sm font-semibold text-gray-600 hover:text-red-600 transition-colors duration-300 flex items-center justify-center gap-2" onclick="openSectionMasterlist(${section.id})">
                            <i class="fas fa-list-alt"></i>
                            View Masterlist
                        </button>
                    </div>
                </div>
            `).join('');
        })
        .catch(error => console.error('Error loading sections:', error));
}

// FIXED MODAL FUNCTIONS
function openAddSectionModal() {
    console.log('Opening Add Section Modal');
    const modal = document.getElementById('addSectionModal');
    modal.style.display = 'flex';
    document.body.classList.add('modal-open');
    populateAdviserSelects();
    populateBuildingSelects();
}

function closeAddSectionModal() {
    const modal = document.getElementById('addSectionModal');
    modal.style.display = 'none';
    document.body.classList.remove('modal-open');
    document.getElementById('addSectionForm').reset();
}

function openSubjectTeacherModal(sectionId) {
    console.log('Opening Subject Teacher Modal for section ID:', sectionId);
    const section = findSectionById(sectionId);
    if (section) {
        document.getElementById('currentSection').textContent = section.name;
        document.getElementById('currentAdviser').textContent = section.adviser;
    }
    
    const modal = document.getElementById('addSubjectTeacherModal');
    modal.style.display = 'flex';
    document.body.classList.add('modal-open');
    populateSubjectTeacherSelects();
}

function closeSubjectTeacherModal() {
    const modal = document.getElementById('addSubjectTeacherModal');
    modal.style.display = 'none';
    document.body.classList.remove('modal-open');
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
    const modal = document.getElementById('updateSectionModal');
    modal.style.display = 'flex';
    document.body.classList.add('modal-open');
}

function closeUpdateSectionModal() {
    const modal = document.getElementById('updateSectionModal');
    modal.style.display = 'none';
    document.body.classList.remove('modal-open');
    document.getElementById('updateSectionForm').reset();
    currentSectionForUpdate = null;
}

function closeAllModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.style.display = 'none';
    });
    document.body.classList.remove('modal-open');
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

// FIXED: Modal opening functions with proper event handling
function assignTeacher(sectionId, event) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    toggleDropdown(sectionId);
    currentSectionForUpdate = findSectionById(sectionId);
    setTimeout(() => {
        openSubjectTeacherModal(sectionId);
    }, 150);
}

function updateSection(sectionId, event) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    toggleDropdown(sectionId);
    setTimeout(() => {
        openUpdateSectionModal(sectionId);
    }, 150);
}

function deleteSection(sectionId, event) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    toggleDropdown(sectionId);
    
    setTimeout(() => {
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
                    showNotification('Section deleted successfully!', 'success');
                    loadSections(currentProgram);
                } else {
                    showNotification(`Error: ${data.message}`, 'error');
                }
            })
            .catch(error => {
                console.error('Error deleting section:', error);
                showNotification('An error occurred while deleting the section.', 'error');
            });
        }
    }, 150);
}

// Notification function
function showNotification(message, type = 'info') {
    alert(message);
}

function openSectionMasterlist(sectionId) {
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
            menu.classList.add('hidden');
            menu.classList.remove('animate-fade-in');
        }
    });
    
    // Toggle current dropdown
    const dropdown = document.getElementById(`dropdown-${sectionId}`);
    if (dropdown) {
        const isHidden = dropdown.classList.contains('hidden');
        
        if (isHidden) {
            dropdown.classList.remove('hidden');
            dropdown.classList.add('animate-fade-in');
        } else {
            dropdown.classList.add('hidden');
            dropdown.classList.remove('animate-fade-in');
        }
    }
}

// Close dropdowns when clicking elsewhere
document.addEventListener('click', function(event) {
    if (!event.target.closest('.relative')) {
        document.querySelectorAll('.dropdown-menu').forEach(menu => {
            menu.classList.add('hidden');
            menu.classList.remove('animate-fade-in');
        });
    }
});

// Add CSS for animations and modal fixes
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-fade-in {
        animation: fadeIn 0.2s ease-out;
    }
    
    /* Modal fixes */
    .modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: none;
        justify-content: center;
        align-items: center;
        z-index: 10000;
    }
    
    .modal-content {
        position: relative;
        background: white;
        border-radius: 8px;
        width: 95%;
        max-width: 900px;
        max-height: 90vh;
        overflow-y: auto;
        margin: auto;
        z-index: 10001;
    }
    
    .subject-teacher-modal {
        max-width: 95% !important;
        width: 95% !important;
    }
    
    body.modal-open {
        overflow: hidden;
    }
    
    .dropdown-menu {
        z-index: 10002;
    }
    
    /* Ensure table is responsive */
    .overflow-x-auto {
        overflow-x: auto;
    }
`;
document.head.appendChild(style);

function handleLogout() {
    if (confirm('Are you sure you want to logout?')) {
        window.location.href = "/logout/";
    }
}

function findSectionById(sectionId) {
    if (sectionsCache[currentProgram]) {
        return sectionsCache[currentProgram].find(section => section.id == sectionId) || null;
    }
    return null;
}