/**
 * Dynamic E-Class Record JavaScript
 * Integrates with Django backend for full CRUD operations
 * Maintains existing calculation logic while adding API integration
 */

// ============================================================================
// CONFIGURATION & STATE
// ============================================================================

const ClassRecordApp = {
    currentClassRecord: null,
    currentStudents: [],
    unsavedChanges: false,
    saveTimeout: null,
    
    // API endpoints (will be set from Django template)
    endpoints: {
        get: window.API_GET_CLASSRECORD || '/teacher/api/classrecord/get/',
        save: window.API_SAVE_CLASSRECORD || '/teacher/api/classrecord/save/',
        exportPdf: window.API_EXPORT_PDF || '/teacher/api/classrecord/{id}/export/pdf/',
        exportExcel: window.API_EXPORT_EXCEL || '/teacher/api/classrecord/{id}/export/excel/',
        history: window.API_CLASSRECORD_HISTORY || '/teacher/api/classrecord/history/',
    },
    
    // Get CSRF token from Django
    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }
};


// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    initializeClassRecord();
    attachEventListeners();
    loadHistory();
    
    // Warn before leaving with unsaved changes
    window.addEventListener('beforeunload', (e) => {
        if (ClassRecordApp.unsavedChanges) {
            e.preventDefault();
            e.returnValue = 'You have unsaved changes. Are you sure you want to leave?';
            return e.returnValue;
        }
    });
});


function initializeClassRecord() {
    // Check if we have section/subject/quarter pre-selected
    const urlParams = new URLSearchParams(window.location.search);
    const sectionId = urlParams.get('section');
    const subjectId = urlParams.get('subject');
    const quarter = urlParams.get('quarter');
    
    if (sectionId && subjectId && quarter) {
        // Auto-load class record
        loadClassRecord(sectionId, subjectId, quarter);
    }
}


// ============================================================================
// EVENT LISTENERS
// ============================================================================

function attachEventListeners() {
    // Section/Subject/Quarter selection changes
    document.getElementById('section-select')?.addEventListener('change', onSelectionChange);
    document.getElementById('subject-select')?.addEventListener('change', onSelectionChange);
    document.querySelectorAll('.tab-link').forEach(tab => {
        tab.addEventListener('click', (e) => {
            onSelectionChange();
        });
    });
    
    // Save button
    document.getElementById('save-btn')?.addEventListener('click', saveClassRecord);
    
    // Export buttons
    document.getElementById('pdf-btn')?.addEventListener('click', exportToPdf);
    document.getElementById('print-btn')?.addEventListener('click', () => window.print());
    
    // Auto-save on input change (debounced)
    document.querySelector('.main-container')?.addEventListener('input', (e) => {
        if (e.target.matches('.score, .hps, .weight-input')) {
            markUnsaved();
            debouncedAutoSave();
        }
    });
}


function onSelectionChange() {
    const sectionId = document.getElementById('section-select')?.value;
    const subjectSelect = document.getElementById('subject-select');
    const subjectId = subjectSelect?.value;
    
    // Get active quarter from tabs
    const activeTab = document.querySelector('.tab-link.active');
    const quarter = activeTab?.getAttribute('data-quarter') || 'Q1';
    
    if (sectionId && subjectId && quarter) {
        // Update subject dropdown based on section
        updateSubjectDropdown(sectionId);
        
        // Load class record
        loadClassRecord(sectionId, subjectId, quarter);
    }
}


function updateSubjectDropdown(sectionId) {
    // This assumes you have sections_with_subjects data from Django context
    const subjectSelect = document.getElementById('subject-select');
    if (!subjectSelect || !window.SECTIONS_WITH_SUBJECTS) return;
    
    const sectionData = window.SECTIONS_WITH_SUBJECTS[sectionId];
    if (!sectionData) return;
    
    // Clear and repopulate
    subjectSelect.innerHTML = '<option value="">Select Subject</option>';
    sectionData.subjects.forEach(subject => {
        const option = document.createElement('option');
        option.value = subject.code;
        option.textContent = subject.name;
        subjectSelect.appendChild(option);
    });
}


// ============================================================================
// LOAD CLASS RECORD
// ============================================================================

async function loadClassRecord(sectionId, subjectId, quarter) {
    showLoader('Loading class record...');
    
    try {
        const schoolYear = document.getElementById('school-year-select')?.value || '2025-2026';
        
        const response = await fetch(
            `${ClassRecordApp.endpoints.get}?section_id=${sectionId}&subject_id=${subjectId}&quarter=${quarter}&school_year=${schoolYear}`,
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': ClassRecordApp.getCsrfToken()
                }
            }
        );
        
        const data = await response.json();
        
        if (data.success) {
            ClassRecordApp.currentClassRecord = data.class_record;
            ClassRecordApp.currentStudents = data.students;
            
            // Populate the UI
            populateClassRecord(data.class_record, data.students);
            
            // Show success message if newly created
            if (data.created) {
                showNotification('New class record created!', 'success');
            } else {
                showNotification('Class record loaded successfully', 'info');
            }
            
            // Reset unsaved changes flag
            ClassRecordApp.unsavedChanges = false;
        } else {
            showNotification(data.error || 'Failed to load class record', 'error');
        }
    } catch (error) {
        console.error('Error loading class record:', error);
        showNotification('Error loading class record. Please try again.', 'error');
    } finally {
        hideLoader();
    }
}


function populateClassRecord(classRecord, students) {
    // Update header info
    document.getElementById('subject-name').textContent = classRecord.subject;
    const activeQuarter = classRecord.quarter;
    
    // Update grading criteria
    document.getElementById(`${activeQuarter.toLowerCase()}-ww-weight`).value = classRecord.weights.ww;
    document.getElementById(`${activeQuarter.toLowerCase()}-pt-weight`).value = classRecord.weights.pt;
    document.getElementById(`${activeQuarter.toLowerCase()}-qa-weight`).value = classRecord.weights.qa;
    
    // Update HPS values
    classRecord.hps.ww.forEach((hps, idx) => {
        const input = document.getElementById(`${activeQuarter.toLowerCase()}-ww-hps-${idx + 1}`);
        if (input) input.value = hps;
    });
    
    classRecord.hps.pt.forEach((hps, idx) => {
        const input = document.getElementById(`${activeQuarter.toLowerCase()}-pt-hps-${idx + 1}`);
        if (input) input.value = hps;
    });
    
    const qaHpsInput = document.getElementById(`${activeQuarter.toLowerCase()}-qa-hps-1`);
    if (qaHpsInput) qaHpsInput.value = classRecord.hps.qa[0];
    
    // Populate student rows
    const tbody = document.getElementById(`${activeQuarter.toLowerCase()}-body`);
    if (!tbody) return;
    
    tbody.innerHTML = ''; // Clear existing rows
    
    students.forEach((student, idx) => {
        const row = createStudentRow(activeQuarter.toLowerCase(), student, idx + 1);
        tbody.appendChild(row);
    });
    
    // Update calculations
    calculateQuarterHPS(activeQuarter.replace('Q', ''));
    calculateQuarterGrades(activeQuarter.replace('Q', ''));
}


function createStudentRow(quarter, student, number) {
    const row = document.createElement('tr');
    row.id = `${quarter}-student-${student.id}`;
    row.dataset.studentId = student.id;
    row.dataset.gradeId = student.grade_id;
    
    row.innerHTML = `
        <td>${number}</td>
        <td class="student-name">${student.name}</td>
        <td class="student-sex">${student.gender}</td>
        
        ${student.scores.ww.map((score, idx) => 
            `<td><input type="number" class="score ${quarter}-ww" data-item="ww-${idx + 1}" value="${score}" step="0.01"></td>`
        ).join('')}
        <td class="locked ${quarter}-ww-total">${student.computed.ww_total.toFixed(2)}</td>
        <td class="locked ${quarter}-ww-ps">${student.computed.ww_percentage.toFixed(2)}</td>
        <td class="locked ${quarter}-ww-ws">${student.computed.ww_weighted_score.toFixed(2)}</td>
        
        ${student.scores.pt.map((score, idx) => 
            `<td><input type="number" class="score ${quarter}-pt" data-item="pt-${idx + 1}" value="${score}" step="0.01"></td>`
        ).join('')}
        <td class="locked ${quarter}-pt-total">${student.computed.pt_total.toFixed(2)}</td>
        <td class="locked ${quarter}-pt-ps">${student.computed.pt_percentage.toFixed(2)}</td>
        <td class="locked ${quarter}-pt-ws">${student.computed.pt_weighted_score.toFixed(2)}</td>
        
        <td><input type="number" class="score ${quarter}-qa" data-item="qa-1" value="${student.scores.qa[0]}" step="0.01"></td>
        <td class="locked ${quarter}-qa-ps">${student.computed.qa_percentage.toFixed(2)}</td>
        <td class="locked ${quarter}-qa-ws">${student.computed.qa_weighted_score.toFixed(2)}</td>
        
        <td class="locked ${quarter}-initial-grade">${student.computed.initial_grade.toFixed(2)}</td>
        <td class="locked ${quarter}-quarterly-grade">${student.computed.quarterly_grade}</td>
    `;
    
    return row;
}


// ============================================================================
// SAVE CLASS RECORD
// ============================================================================

async function saveClassRecord() {
    if (!ClassRecordApp.currentClassRecord) {
        showNotification('No class record loaded', 'warning');
        return;
    }
    
    showLoader('Saving class record...');
    
    try {
        // Collect current data from UI
        const activeQuarter = document.querySelector('.tab-content[style*="display: block"]')?.id.replace('Q', '');
        const q = `q${activeQuarter}`;
        
        // Collect weights
        const weights = {
            ww: parseInt(document.getElementById(`${q}-ww-weight`).value) || 30,
            pt: parseInt(document.getElementById(`${q}-pt-weight`).value) || 50,
            qa: parseInt(document.getElementById(`${q}-qa-weight`).value) || 20
        };
        
        // Collect HPS
        const hps = {
            ww: [],
            pt: [],
            qa: []
        };
        
        for (let i = 1; i <= 10; i++) {
            const wwHps = document.getElementById(`${q}-ww-hps-${i}`);
            const ptHps = document.getElementById(`${q}-pt-hps-${i}`);
            if (wwHps) hps.ww.push(parseInt(wwHps.value) || 10);
            if (ptHps) hps.pt.push(parseInt(ptHps.value) || 10);
        }
        
        const qaHps = document.getElementById(`${q}-qa-hps-1`);
        if (qaHps) hps.qa.push(parseInt(qaHps.value) || 50);
        
        // Collect student scores
        const students = [];
        const tbody = document.getElementById(`${q}-body`);
        
        if (tbody) {
            tbody.querySelectorAll('tr').forEach(row => {
                const gradeId = row.dataset.gradeId;
                if (!gradeId) return;
                
                const scores = {
                    ww: [],
                    pt: [],
                    qa: []
                };
                
                row.querySelectorAll(`.${q}-ww`).forEach(input => {
                    scores.ww.push(parseFloat(input.value) || 0);
                });
                
                row.querySelectorAll(`.${q}-pt`).forEach(input => {
                    scores.pt.push(parseFloat(input.value) || 0);
                });
                
                row.querySelectorAll(`.${q}-qa`).forEach(input => {
                    scores.qa.push(parseFloat(input.value) || 0);
                });
                
                students.push({
                    grade_id: parseInt(gradeId),
                    scores: scores
                });
            });
        }
        
        // Send to backend
        const response = await fetch(ClassRecordApp.endpoints.save, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': ClassRecordApp.getCsrfToken()
            },
            body: JSON.stringify({
                class_record_id: ClassRecordApp.currentClassRecord.id,
                weights: weights,
                hps: hps,
                students: students
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Class record saved successfully!', 'success');
            ClassRecordApp.unsavedChanges = false;
            
            // Show modal
            const modal = document.getElementById('saveModal');
            if (modal) modal.style.display = 'block';
            
            // Reload history
            loadHistory();
        } else {
            showNotification(data.error || 'Failed to save class record', 'error');
        }
    } catch (error) {
        console.error('Error saving class record:', error);
        showNotification('Error saving class record. Please try again.', 'error');
    } finally {
        hideLoader();
    }
}


// Debounced auto-save
function debouncedAutoSave() {
    if (ClassRecordApp.saveTimeout) {
        clearTimeout(ClassRecordApp.saveTimeout);
    }
    
    ClassRecordApp.saveTimeout = setTimeout(() => {
        // Auto-save in background
        saveClassRecord();
    }, 3000); // 3 seconds after last change
}


function markUnsaved() {
    ClassRecordApp.unsavedChanges = true;
}


// ============================================================================
// EXPORT FUNCTIONS
// ============================================================================

async function exportToPdf() {
    if (!ClassRecordApp.currentClassRecord) {
        showNotification('No class record loaded', 'warning');
        return;
    }
    
    const recordId = ClassRecordApp.currentClassRecord.id;
    const url = ClassRecordApp.endpoints.exportPdf.replace('{id}', recordId);
    
    showLoader('Generating PDF...');
    
    try {
        window.location.href = url;
        showNotification('PDF download started', 'success');
    } catch (error) {
        console.error('Error exporting PDF:', error);
        showNotification('Error exporting PDF. Please try again.', 'error');
    } finally {
        setTimeout(() => hideLoader(), 1000);
    }
}


async function exportToExcel() {
    if (!ClassRecordApp.currentClassRecord) {
        showNotification('No class record loaded', 'warning');
        return;
    }
    
    const recordId = ClassRecordApp.currentClassRecord.id;
    const url = ClassRecordApp.endpoints.exportExcel.replace('{id}', recordId);
    
    showLoader('Generating Excel file...');
    
    try {
        window.location.href = url;
        showNotification('Excel download started', 'success');
    } catch (error) {
        console.error('Error exporting Excel:', error);
        showNotification('Error exporting Excel. Please try again.', 'error');
    } finally {
        setTimeout(() => hideLoader(), 1000);
    }
}


// ============================================================================
// HISTORY
// ============================================================================

async function loadHistory() {
    try {
        const response = await fetch(ClassRecordApp.endpoints.history, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': ClassRecordApp.getCsrfToken()
            }
        });
        
        const data = await response.json();
        
        if (data.success && data.history) {
            displayHistory(data.history);
        }
    } catch (error) {
        console.error('Error loading history:', error);
    }
}


function displayHistory(history) {
    const historyList = document.getElementById('history-list');
    const emptyMsg = document.getElementById('history-list-empty');
    
    if (!historyList) return;
    
    if (history.length === 0) {
        emptyMsg.style.display = 'block';
        return;
    }
    
    emptyMsg.style.display = 'none';
    historyList.innerHTML = '';
    
    history.forEach(log => {
        const item = document.createElement('div');
        item.className = 'history-item';
        item.innerHTML = `
            <strong>${log.action}</strong>
            <span>${log.date} at ${log.time}</span>
        `;
        historyList.appendChild(item);
    });
}


// ============================================================================
// UI HELPERS
// ============================================================================

function showLoader(message = 'Loading...') {
    // You can implement a custom loader or use the existing one
    const loader = document.querySelector('.loader');
    if (loader) {
        loader.style.display = 'block';
        loader.textContent = message;
    }
}


function hideLoader() {
    const loader = document.querySelector('.loader');
    if (loader) {
        loader.style.display = 'none';
    }
}


function showNotification(message, type = 'info') {
    // Simple toast notification
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        z-index: 10000;
        animation: slideIn 0.3s ease;
        ${type === 'success' ? 'background: #10b981;' : ''}
        ${type === 'error' ? 'background: #ef4444;' : ''}
        ${type === 'warning' ? 'background: #f59e0b;' : ''}
        ${type === 'info' ? 'background: #3b82f6;' : ''}
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}


// ============================================================================
// KEEP EXISTING CALCULATION LOGIC
// (Your existing functions from the HTML template)
// ============================================================================

// These functions remain the same as in your original HTML
// calculateQuarterHPS, calculateQuarterGrades, transmute, etc.
// They will work seamlessly with the new dynamic data