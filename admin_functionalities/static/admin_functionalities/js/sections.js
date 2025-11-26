
// Global vars
let currentProgram = 'STE';
let currentSectionForUpdate = null;
let currentGradeLevel = '7';
let advisers = [];
let subjectTeachers = [];
let buildingsRooms = {};
let sectionsCache = {};
let currentSubjectProgram = 'STE';
let subjectsByProgram = {};
let currentEditingSubject = null;
let programsCache = [];
let currentEditingProgram = null;
let schoolYears = [];

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
        fetchBuildingsRooms().then(() => console.log('Buildings/rooms fetched')),
        loadAllProgramSubjects().then(() => console.log('Subjects loaded'))
    ]).then(() => {
        console.log('All data fetched successfully');
        loadSections(currentProgram);
        setupEventListeners();
    });
     // Load school years for program form
    loadSchoolYears();
    
    // Setup program form submission
    const programForm = document.getElementById('programForm');
    if (programForm) {
        programForm.addEventListener('submit', handleProgramFormSubmit);
    }
});

function loadSchoolYears() {
    fetch(`${BASE_URL}api/school-years/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                schoolYears = data.school_years || [];
                populateSchoolYearSelect();
            }
        })
        .catch(error => console.error('Error loading school years:', error));
}

function populateSchoolYearSelect() {
    const select = document.getElementById('programSchoolYear');
    if (select) {
        select.innerHTML = '<option value="">Select School Year</option>';
        schoolYears.forEach(sy => {
            const option = document.createElement('option');
            option.value = sy.id;
            option.textContent = sy.name;
            if (sy.is_active) {
                option.selected = true;
            }
            select.appendChild(option);
        });
    }
}

// Open Manage Programs Modal
function openManageProgramsModal() {
    console.log('Opening Manage Programs Modal');
    const modal = document.getElementById('manageProgramsModal');
    modal.style.display = 'flex';
    document.body.classList.add('modal-open');
    
    loadAllPrograms();
    cancelProgramForm();
}

// Close Manage Programs Modal
function closeManageProgramsModal() {
    const modal = document.getElementById('manageProgramsModal');
    modal.style.display = 'none';
    document.body.classList.remove('modal-open');
    cancelProgramForm();
}

// Load All Programs
function loadAllPrograms() {
    console.log('Loading all programs');
    
    fetch(`${BASE_URL}api/programs/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                programsCache = data.programs || [];
                renderProgramsTable(data.programs || []);
            } else {
                console.error('Failed to load programs:', data.error);
                renderProgramsTable([]);
            }
        })
        .catch(error => {
            console.error('Error loading programs:', error);
            renderProgramsTable([]);
        });
}

// Render Programs Table
function renderProgramsTable(programs) {
    const tableBody = document.getElementById('programsTableBody');
    
    if (programs.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center py-8">
                    <div class="flex flex-col items-center gap-3">
                        <i class="fas fa-inbox text-4xl text-gray-300"></i>
                        <p class="text-gray-500 font-medium">No programs found</p>
                        <button class="gradient-bg text-white px-4 py-2 rounded-lg text-sm" onclick="openAddProgramForm()">
                            <i class="fas fa-plus mr-2"></i>Add First Program
                        </button>
                    </div>
                </td>
            </tr>
        `;
        return;
    }
    
    tableBody.innerHTML = programs.map((program, index) => `
        <tr>
            <td class="text-center font-semibold text-gray-600">${index + 1}</td>
            <td class="subject-name">${program.name}</td>
            <td class="text-gray-600 text-sm">${program.description || '<em class="text-gray-400">No description</em>'}</td>
            <td class="font-medium text-gray-700">${program.school_year.name}</td>
            <td class="text-center">
                <span class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-semibold">
                    ${program.section_count}
                </span>
            </td>
            <td class="text-center">
                ${program.is_active 
                    ? '<span class="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-semibold">Active</span>'
                    : '<span class="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-semibold">Inactive</span>'
                }
            </td>
            <td>
                <div class="flex gap-2 justify-center">
                    <button 
                        class="px-3 py-2 ${program.is_active ? 'bg-yellow-100 text-yellow-600 hover:bg-yellow-200' : 'bg-green-100 text-green-600 hover:bg-green-200'} rounded-lg transition-all duration-200 flex items-center gap-2"
                        onclick="toggleProgramStatus(${program.id})"
                        title="${program.is_active ? 'Deactivate' : 'Activate'} Program">
                        <i class="fas fa-${program.is_active ? 'ban' : 'check-circle'}"></i>
                    </button>
                    <button 
                        class="px-3 py-2 bg-blue-100 text-blue-600 rounded-lg hover:bg-blue-200 transition-all duration-200 flex items-center gap-2"
                        onclick="editProgram(${program.id})"
                        title="Edit Program">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button 
                        class="px-3 py-2 bg-red-100 text-red-600 rounded-lg hover:bg-red-200 transition-all duration-200 flex items-center gap-2"
                        onclick="deleteProgram(${program.id})"
                        title="Delete Program">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

// Open Add Program Form
function openAddProgramForm() {
    console.log('Opening Add Program Form');
    document.getElementById('programFormContainer').style.display = 'block';
    document.getElementById('programFormTitle').textContent = 'Add New Program';
    document.getElementById('programForm').reset();
    document.getElementById('programId').value = '';
    document.getElementById('programIsActive').checked = true;
    currentEditingProgram = null;
    
    populateSchoolYearSelect();
    
    document.getElementById('programFormContainer').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'nearest' 
    });
}

// Edit Program
function editProgram(programId) {
    console.log(`Editing program with ID: ${programId}`);
    
    const program = programsCache.find(p => p.id === programId);
    
    if (!program) {
        alert('Program not found!');
        return;
    }
    
    currentEditingProgram = program;
    
    document.getElementById('programFormContainer').style.display = 'block';
    document.getElementById('programFormTitle').textContent = 'Edit Program';
    document.getElementById('programId').value = program.id;
    document.getElementById('programName').value = program.name;
    document.getElementById('programDescription').value = program.description || '';
    document.getElementById('programIsActive').checked = program.is_active;
    
    populateSchoolYearSelect();
    setTimeout(() => {
        document.getElementById('programSchoolYear').value = program.school_year.id;
    }, 100);
    
    document.getElementById('programFormContainer').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'nearest' 
    });
}

// Delete Program
function deleteProgram(programId) {
    console.log(`Deleting program with ID: ${programId}`);
    
    const program = programsCache.find(p => p.id === programId);
    
    if (!program) {
        alert('Program not found!');
        return;
    }
    
    if (!confirm(`Are you sure you want to delete the program "${program.name}"? This action cannot be undone.`)) {
        return;
    }
    
    fetch(`${BASE_URL}api/programs/delete/${programId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            loadAllPrograms();
            
            // Reload program tabs if we're on sections page
            if (typeof loadSections === 'function') {
                location.reload(); // Reload page to update program tabs
            }
        } else {
            alert(`Error: ${data.message}`);
        }
    })
    .catch(error => {
        console.error('Error deleting program:', error);
        alert('An error occurred while deleting the program.');
    });
}

// Toggle Program Status
function toggleProgramStatus(programId) {
    console.log(`Toggling status for program ID: ${programId}`);
    
    const program = programsCache.find(p => p.id === programId);
    
    if (!program) {
        alert('Program not found!');
        return;
    }
    
    const action = program.is_active ? 'deactivate' : 'activate';
    const confirmMsg = program.is_active 
        ? `Deactivating "${program.name}" will hide it from the system. Continue?`
        : `Activate program "${program.name}"?`;
    
    if (!confirm(confirmMsg)) {
        return;
    }
    
    fetch(`${BASE_URL}api/programs/toggle/${programId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            loadAllPrograms();
            
            // Reload page to update program tabs
            location.reload();
        } else {
            alert(`Error: ${data.message}`);
        }
    })
    .catch(error => {
        console.error('Error toggling program status:', error);
        alert('An error occurred while updating the program status.');
    });
}

// Cancel Program Form
function cancelProgramForm() {
    document.getElementById('programFormContainer').style.display = 'none';
    document.getElementById('programForm').reset();
    currentEditingProgram = null;
}

// Handle Program Form Submit
function handleProgramFormSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const programId = formData.get('program_id');
    const isUpdate = !!programId;
    
    const url = isUpdate 
        ? `${BASE_URL}api/programs/update/${programId}/`
        : `${BASE_URL}api/programs/add/`;
    
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            loadAllPrograms();
            cancelProgramForm();
            
            // Reload page to update program tabs
            if (isUpdate || !isUpdate) {
                location.reload();
            }
        } else {
            alert(`Error: ${data.message}\nDetails: ${JSON.stringify(data.errors)}`);
        }
    })
    .catch(error => {
        console.error('Error saving program:', error);
        alert('An error occurred while saving the program.');
    });
}

// Initialize mock subjects data
function loadAllProgramSubjects() {
    const programs = ['STE', 'SPFL', 'SPTVE', 'OHSP', 'SNED', 'TOP5', 'HETERO'];
    
    return Promise.all(
        programs.map(program => 
            fetch(`${BASE_URL}api/subjects/${program}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        subjectsByProgram[program] = data.subjects || [];
                    }
                })
                .catch(error => console.error(`Error loading subjects for ${program}:`, error))
        )
    );
}

// Manage Subjects Modal Functions
function openManageSubjectsModal() {
    console.log('Opening Manage Subjects Modal');
    const modal = document.getElementById('manageSubjectsModal');
    modal.style.display = 'flex';
    document.body.classList.add('modal-open');
    
    // Set first tab as active
    currentSubjectProgram = 'STE';
    updateSubjectProgramTabs('STE');
    loadSubjectsForProgram('STE');
}


function closeManageSubjectsModal() {
    const modal = document.getElementById('manageSubjectsModal');
    modal.style.display = 'none';
    document.body.classList.remove('modal-open');
    cancelSubjectForm();
}

function switchSubjectProgram(program) {
    console.log(`Switching subject program to: ${program}`);
    currentSubjectProgram = program;
    updateSubjectProgramTabs(program);
    loadSubjectsForProgram(program);
    cancelSubjectForm();
}

function updateSubjectProgramTabs(program) {
    document.querySelectorAll('.subject-tab-btn').forEach(btn => {
        btn.classList.remove('active', 'gradient-bg', 'text-white', 'border-red-700', 'shadow-lg');
        btn.classList.add('bg-white', 'text-gray-600', 'border-gray-200');
    });
    
    const targetTab = document.querySelector(`.subject-tab-btn[data-subject-program="${program}"]`);
    if (targetTab) {
        targetTab.classList.add('active', 'gradient-bg', 'text-white', 'border-red-700', 'shadow-lg');
        targetTab.classList.remove('bg-white', 'text-gray-600', 'border-gray-200');
    }
}

function loadSubjectsForProgram(program) {
    console.log(`Loading subjects for program: ${program}`);
    
    fetch(`${BASE_URL}api/subjects/${program}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                subjectsByProgram[program] = data.subjects || [];
                renderSubjectsTable(data.subjects || []);
            } else {
                console.error('Failed to load subjects:', data.error);
                renderSubjectsTable([]);
            }
        })
        .catch(error => {
            console.error('Error loading subjects:', error);
            renderSubjectsTable([]);
        });
}

function renderSubjectsTable(subjects) {
    const tableBody = document.getElementById('subjectsTableBody');
    
    if (subjects.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center py-8">
                    <div class="flex flex-col items-center gap-3">
                        <i class="fas fa-inbox text-4xl text-gray-300"></i>
                        <p class="text-gray-500 font-medium">No subjects found for ${currentSubjectProgram}</p>
                        <button class="gradient-bg text-white px-4 py-2 rounded-lg text-sm" onclick="openAddSubjectForm()">
                            <i class="fas fa-plus mr-2"></i>Add First Subject
                        </button>
                    </div>
                </td>
            </tr>
        `;
        return;
    }
    
    tableBody.innerHTML = subjects.map((subject, index) => `
        <tr>
            <td class="text-center font-semibold text-gray-600">${index + 1}</td>
            <td class="subject-name">${subject.name}</td>
            <td class="font-medium text-gray-600">${subject.code}</td>
            <td>
                <div class="flex gap-2 justify-center">
                    <button 
                        class="px-3 py-2 bg-blue-100 text-blue-600 rounded-lg hover:bg-blue-200 transition-all duration-200 flex items-center gap-2"
                        onclick="editSubject(${subject.id})"
                        title="Edit Subject">
                        <i class="fas fa-edit"></i>
                        <span class="text-sm font-medium">Edit</span>
                    </button>
                    <button 
                        class="px-3 py-2 bg-red-100 text-red-600 rounded-lg hover:bg-red-200 transition-all duration-200 flex items-center gap-2"
                        onclick="deleteSubject(${subject.id})"
                        title="Delete Subject">
                        <i class="fas fa-trash"></i>
                        <span class="text-sm font-medium">Delete</span>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

function openAddSubjectForm() {
    console.log('Opening Add Subject Form');
    document.getElementById('subjectFormContainer').style.display = 'block';
    document.getElementById('subjectFormTitle').textContent = 'Add New Subject';
    document.getElementById('subjectForm').reset();
    document.getElementById('subjectId').value = '';
    document.getElementById('subjectProgramInput').value = currentSubjectProgram;
    currentEditingSubject = null;
    
    document.getElementById('subjectFormContainer').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'nearest' 
    });
}

function editSubject(subjectId) {
    console.log(`Editing subject with ID: ${subjectId}`);
    
    let subject = null;
    for (const program in subjectsByProgram) {
        subject = subjectsByProgram[program].find(s => s.id === subjectId);
        if (subject) break;
    }
    
    if (!subject) {
        alert('Subject not found!');
        return;
    }
    
    currentEditingSubject = subject;
    
    document.getElementById('subjectFormContainer').style.display = 'block';
    document.getElementById('subjectFormTitle').textContent = 'Edit Subject';
    document.getElementById('subjectId').value = subject.id;
    document.getElementById('subjectProgramInput').value = subject.program;
    document.getElementById('subjectName').value = subject.name;
    document.getElementById('subjectCode').value = subject.code;
    
    document.getElementById('subjectFormContainer').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'nearest' 
    });
}

function deleteSubject(subjectId) {
    console.log(`Deleting subject with ID: ${subjectId}`);
    
    if (!confirm('Are you sure you want to delete this subject? This action cannot be undone.')) {
        return;
    }
    
    fetch(`${BASE_URL}api/subjects/delete/${subjectId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            loadSubjectsForProgram(currentSubjectProgram);
        } else {
            alert(`Error: ${data.message}`);
        }
    })
    .catch(error => {
        console.error('Error deleting subject:', error);
        alert('An error occurred while deleting the subject.');
    });
}


function cancelSubjectForm() {
    document.getElementById('subjectFormContainer').style.display = 'none';
    document.getElementById('subjectForm').reset();
    currentEditingSubject = null;
}

// Add event listener for subject form submission
document.addEventListener('DOMContentLoaded', () => {
    const subjectForm = document.getElementById('subjectForm');
    if (subjectForm) {
        subjectForm.addEventListener('submit', handleSubjectFormSubmit);
    }
});

function handleSubjectFormSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const subjectId = formData.get('subject_id');
    const isUpdate = !!subjectId;
    
    // FIX: Don't set program in formData - let the backend handle it via URL
    // Remove this line if it exists:
    // formData.set('program', currentSubjectProgram);
    
    const url = isUpdate 
        ? `${BASE_URL}api/subjects/update/${subjectId}/`
        : `${BASE_URL}api/subjects/add/${currentSubjectProgram}/`;
    
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': CSRF_TOKEN
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            loadSubjectsForProgram(currentSubjectProgram);
            cancelSubjectForm();
        } else {
            alert(`Error: ${data.message}\nDetails: ${JSON.stringify(data.errors)}`);
        }
    })
    .catch(error => {
        console.error('Error saving subject:', error);
        alert('An error occurred while saving the subject.');
    });
}


// Update the openSubjectTeacherModal function to load subjects dynamically
function openSubjectTeacherModal(sectionId) {
    console.log('Opening Subject Teacher Modal for section ID:', sectionId);
    const section = findSectionById(sectionId);
    
    if (section) {
        document.getElementById('currentSection').textContent = section.name;
        document.getElementById('currentAdviser').textContent = section.adviser;
        
        // Fetch and load subjects for this section's program
        loadSubjectsForSection(sectionId);
    }
    
    const modal = document.getElementById('addSubjectTeacherModal');
    modal.style.display = 'flex';
    document.body.classList.add('modal-open');
}

function loadSubjectsForSection(sectionId) {
    fetch(`${BASE_URL}api/sections/${sectionId}/subjects/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                renderSectionSubjectsTable(data.subjects);
                populateSubjectTeacherSelects();
            } else {
                console.error('Failed to load subjects:', data.error);
            }
        })
        .catch(error => {
            console.error('Error loading subjects:', error);
        });
}

function renderSectionSubjectsTable(subjects) {
    const tableBody = document.querySelector('#addSubjectTeacherModal .subject-table tbody');

    if (subjects.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center py-8">
                    <p class="text-gray-500">No subjects available for this program.</p>
                    <button class="text-red-600 hover:underline mt-2" onclick="closeSubjectTeacherModal(); openManageSubjectsModal();">
                        <i class="fas fa-plus mr-1"></i>Add subjects first
                    </button>
                </td>
            </tr>
        `;
        return;
    }
    
    tableBody.innerHTML = subjects.map(subject => `
        <tr>
            <td class="subject-name">${subject.name}</td>
            <td>
                <select id="teacher_${subject.id}" name="teacher_${subject.id}" class="form-select" data-subject-id="${subject.id}">
                    <option value="">Select Teacher</option>
                </select>
            </td>
            <td>
                <select id="day_${subject.id}" name="day_${subject.id}" class="form-select">
                    <option value="DAILY">Daily</option>
                    <option value="MWF">MWF</option>
                    <option value="TTH">TTH</option>
                </select>
            </td>
            <td>
                <div class="time-inputs">
                    <input type="time" id="time_${subject.id}" name="time_${subject.id}" class="form-input">
                    <span class="time-separator">-</span>
                    <input type="time" id="timeEnd_${subject.id}" name="timeEnd_${subject.id}" class="form-input">
                </div>
            </td>
        </tr>
    `).join('');
}

function loadSubjectsInAssignModal(program) {
    console.log(`Loading subjects in assign modal for program: ${program}`);
    const subjects = subjectsByProgram[program] || [];
    const tableBody = document.querySelector('#addSubjectTeacherModal .subject-table tbody');
    
    if (subjects.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center py-8">
                    <p class="text-gray-500">No subjects available for ${program} program.</p>
                    <button class="text-red-600 hover:underline mt-2" onclick="closeSubjectTeacherModal(); openManageSubjectsModal();">
                        <i class="fas fa-plus mr-1"></i>Add subjects first
                    </button>
                </td>
            </tr>
        `;
        return;
    }
    
    // Generate table rows for each subject
    tableBody.innerHTML = subjects.map(subject => {
        const subjectKey = subject.code.toLowerCase().replace(/[^a-z0-9]/g, '');
        return `
            <tr>
                <td class="subject-name">${subject.name}</td>
                <td>
                    <select id="${subjectKey}Teacher" name="${subjectKey}Teacher" class="form-select">
                        <option value="">Select Teacher</option>
                    </select>
                </td>
                <td>
                    <select id="${subjectKey}Day" name="${subjectKey}Day" class="form-select">
                        <option value="DAILY">Daily</option>
                        <option value="MWF">MWF</option>
                        <option value="TTH">TTH</option>
                    </select>
                </td>
                <td>
                    <div class="time-inputs">
                        <input type="time" id="${subjectKey}Time" name="${subjectKey}Time" class="form-input">
                        <span class="time-separator">-</span>
                        <input type="time" id="${subjectKey}TimeEnd" name="${subjectKey}TimeEnd" class="form-input">
                    </div>
                </td>
            </tr>
        `;
    }).join('');
    
    // Populate teacher dropdowns after creating the rows
    setTimeout(() => populateSubjectTeacherSelects(), 100);
}

// Add CSS for the subject tab buttons
const subjectTabStyle = document.createElement('style');
subjectTabStyle.textContent = `
    .subject-tab-btn.active {
        background: linear-gradient(135deg, #c41e3a 0%, #a01729 100%);
        color: white;
        border-color: #c41e3a;
        box-shadow: 0 4px 12px rgba(196, 30, 58, 0.3);
    }
    
    .subject-program-tabs {
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 20px;
    }
`;
document.head.appendChild(subjectTabStyle);

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
    const teacherSelects = document.querySelectorAll('[data-subject-id]');

    teacherSelects.forEach(select => {
        const subjectId = select.dataset.subjectId;
        const teacherId = select.value;

        if (teacherId) {
            const day = document.getElementById(`day_${subjectId}`).value;
            const startTime = document.getElementById(`time_${subjectId}`).value;
            const endTime = document.getElementById(`timeEnd_${subjectId}`).value;

            if (day && startTime && endTime) {
                assignments.push({
                    subject_id: subjectId,
                    teacher_id: teacherId,
                    day: day,
                    start_time: startTime,
                    end_time: endTime
                });
            }
        }
    });

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
        body: JSON.stringify({ assignments })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            closeSubjectTeacherModal();
            loadSections(currentProgram);
        } else {
            alert(`Error: ${data.message}`);
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


