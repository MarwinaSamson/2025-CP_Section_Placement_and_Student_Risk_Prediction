
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