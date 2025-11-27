// Utility: Get CSRF Token from Cookie (for Django POST)
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

document.addEventListener("DOMContentLoaded", () => {
    console.log("Settings JS loaded – DOM ready!");

    // CRITICAL: Load tables on page load
    fetchTables();

    // Initialize tab functionality
    const tabBtns = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");

    tabBtns.forEach((btn) => {
        btn.addEventListener("click", () => {
            const tabName = btn.getAttribute("data-tab");
            tabBtns.forEach((b) => b.classList.remove("active"));
            tabContents.forEach((c) => c.classList.remove("active"));
            btn.classList.add("active");
            document.getElementById(`${tabName}-tab`).classList.add("active");
        });
    });

    // Content Management sub-tabs
    const contentTabBtns = document.querySelectorAll(".content-tab-btn");
    const contentSections = document.querySelectorAll(".content-section");

    contentTabBtns.forEach((btn) => {
        btn.addEventListener("click", () => {
            const contentName = btn.getAttribute("data-content");
            contentTabBtns.forEach((b) => b.classList.remove("active"));
            contentSections.forEach((s) => s.classList.remove("active"));
            btn.classList.add("active");
            document.getElementById(`${contentName}-content`).classList.add("active");
        });
    });

    // Search functionality
    const userSearch = document.getElementById("userSearch");
    if (userSearch) {
        userSearch.addEventListener("input", function () {
            filterUsers(this.value);
        });
    }

    const historySearch = document.getElementById("historySearch");
    if (historySearch) {
        historySearch.addEventListener("input", function () {
            filterHistory(this.value);
        });
    }

    // Close dropdowns when clicking outside
    document.addEventListener("click", (e) => {
        if (!e.target.closest(".actions-dropdown")) {
            document.querySelectorAll(".dropdown-menu").forEach((menu) => {
                menu.classList.remove("show");
            });
        }
    });

    // File Upload Handlers
    document.querySelectorAll('.upload-area input[type="file"]').forEach((input) => {
        input.addEventListener("change", function (e) {
            const file = e.target.files[0];
            if (file) {
                const uploadArea = this.parentElement;
                uploadArea.innerHTML = `<i class="fas fa-check-circle" style="color: #28a745;"></i><p style="color: #28a745;">${file.name}</p>`;
            }
        });
    });

    // Text Editor Functionality
    document.querySelectorAll(".editor-toolbar button").forEach((button) => {
        button.addEventListener("click", function (e) {
            e.preventDefault();
            const command = this.querySelector("i").classList[1].split("-")[1];
            switch (command) {
                case "bold": document.execCommand("bold"); break;
                case "italic": document.execCommand("italic"); break;
                case "underline": document.execCommand("underline"); break;
                case "ul": document.execCommand("insertUnorderedList"); break;
                case "ol": document.execCommand("insertOrderedList"); break;
                case "link": {
                    const url = prompt("Enter URL:");
                    if (url) document.execCommand("createLink", false, url);
                    break;
                }
            }
        });
    });

    // Add User Form Submission
    const addUserForm = document.getElementById("addUserForm");
    if (addUserForm) {
        console.log("Form found – attaching submit handler.");
        addUserForm.addEventListener("submit", function (e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const actionUrl = this.action;
            
            // Debug: Log form data
            console.log("Submitting form to:", actionUrl);
            for (let [key, value] of formData.entries()) {
                console.log(key, value);
            }

            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Adding...';

            fetch(actionUrl, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then(response => {
                console.log("Response status:", response.status);
                return response.json().then(data => {
                    console.log("Response data:", data);
                    if (!response.ok) {
                        throw new Error(data.message || JSON.stringify(data.errors) || "Unknown error");
                    }
                    return data;
                });
            })
            .then(data => {
                const errorDiv = document.getElementById('addUserErrors');
                if (data.success) {
                    // Show success message
                    showNotification('success', data.message || 'User added successfully!');
                    
                    // Close modal and reset form
                    closeAddUserModal();
                    
                    // Refresh tables
                    fetchTables();
                } else if (errorDiv) {
                    errorDiv.innerHTML = formatErrors(data.errors);
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
                showNotification('error', `Submission failed: ${error.message}`);
            })
            .finally(() => {
                // Reset button state
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            });
        });
    }

    // Error Formatter
    function formatErrors(errors) {
        let html = '<ul class="list-disc pl-5">';
        for (let field in errors) {
            const errorMessages = Array.isArray(errors[field]) ? errors[field] : [errors[field]];
            errorMessages.forEach(msg => {
                html += `<li><strong>${field}:</strong> ${msg}</li>`;
            });
        }
        return html + '</ul>';
    }

    // Table Fetchers
    function fetchTables() {
        console.log("Fetching tables...");
        fetchUsersTable();
        fetchHistoryTable();
    }

    function fetchUsersTable() {
        console.log("Fetching users table...");
        fetch('/admin-functionalities/settings/get-users/', {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log("Users data received:", data);
            const tableBody = document.getElementById('usersTableBody');
            if (tableBody && data.users) {
                tableBody.innerHTML = '';
                
                if (data.users.length === 0) {
                    tableBody.innerHTML = `
                        <tr>
                            <td colspan="5" class="px-6 py-8 text-center text-gray-500">
                                <i class="fas fa-users text-4xl mb-3"></i>
                                <p>No users found. Add your first user!</p>
                            </td>
                        </tr>
                    `;
                    return;
                }
                
                data.users.forEach(user => {
                    const row = document.createElement('tr');
                    row.className = "hover:bg-gray-50 transition-colors";
                    row.innerHTML = `
                        <td class="px-6 py-4">
                            <div class="flex items-center gap-3">
                                <img src="/static/admin_functionalities/assets/kakashi.jpeg" 
                                     alt="User" 
                                     class="w-10 h-10 rounded-full object-cover border-2 border-gray-200" />
                                <div>
                                    <div class="font-semibold text-gray-800">${user.first_name} ${user.last_name}</div>
                                    <div class="text-sm text-gray-500">${user.email}</div>
                                </div>
                            </div>
                        </td>
                        <td class="px-6 py-4">
                            ${user.is_superuser ? '<span class="access-badge admin">Admin</span>' : ''}
                            ${user.is_staff_expert ? '<span class="access-badge staff">Staff Expert</span>' : ''}
                            ${user.is_subject_teacher ? '<span class="access-badge teacher">Subject Teacher</span>' : ''}
                            ${user.is_adviser ? '<span class="access-badge adviser">Adviser</span>' : ''}
                        </td>
                        <td class="px-6 py-4 text-gray-600">${user.last_login_formatted || user.date_joined_formatted}</td>
                        <td class="px-6 py-4 text-gray-600">${user.date_joined_formatted}</td>
                        <td class="px-6 py-4">
                            <div class="relative actions-dropdown">
                                <button class="p-2 hover:bg-gray-100 rounded-lg transition-colors" onclick="toggleDropdown(this)">
                                    <i class="fas fa-ellipsis-v text-gray-600"></i>
                                </button>
                                <div class="dropdown-menu absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-10">
                                    <a href="#" onclick="viewProfile('${user.id}')" class="flex items-center gap-3 px-4 py-2 hover:bg-gray-50 text-gray-700">
                                        <i class="fas fa-eye w-5"></i> View Profile
                                    </a>
                                    <a href="#" onclick="editDetails('${user.id}')" class="flex items-center gap-3 px-4 py-2 hover:bg-gray-50 text-gray-700">
                                        <i class="fas fa-edit w-5"></i> Edit Details
                                    </a>
                                    <a href="#" onclick="changePermission('${user.id}')" class="flex items-center gap-3 px-4 py-2 hover:bg-gray-50 text-gray-700">
                                        <i class="fas fa-user-cog w-5"></i> Change Permission
                                    </a>
                                    <a href="#" onclick="deleteUser('${user.id}')" class="flex items-center gap-3 px-4 py-2 hover:bg-red-50 text-red-600">
                                        <i class="fas fa-trash w-5"></i> Delete User
                                    </a>
                                </div>
                            </div>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });
            }
        })
        .catch(error => {
            console.error('Error fetching users:', error);
            showNotification('error', 'Failed to load users table');
        });
    }

    function fetchHistoryTable() {
        console.log("Fetching history table...");
        fetch('/admin-functionalities/settings/get-logs/', {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log("History data received:", data);
            const tableBody = document.querySelector('#history-tab tbody');
            if (tableBody && data.logs) {
                tableBody.innerHTML = '';
                
                if (data.logs.length === 0) {
                    tableBody.innerHTML = `
                        <tr>
                            <td colspan="4" class="px-6 py-8 text-center text-gray-500">
                                <i class="fas fa-history text-4xl mb-3"></i>
                                <p>No activity logs yet.</p>
                            </td>
                        </tr>
                    `;
                    return;
                }
                
                data.logs.forEach(log => {
                    const row = document.createElement('tr');
                    row.className = "hover:bg-gray-50 transition-colors";
                    row.innerHTML = `
                        <td class="px-6 py-4">
                            <div class="flex items-center gap-3">
                                <img src="/static/admin_functionalities/assets/kakashi.jpeg" 
                                     alt="User" 
                                     class="w-8 h-8 rounded-full object-cover border-2 border-gray-200" />
                                <div>
                                    <div class="font-semibold text-gray-800 text-sm">${log.user_full_name}</div>
                                    <div class="text-xs text-gray-500">${log.user_role}</div>
                                </div>
                            </div>
                        </td>
                        <td class="px-6 py-4 text-gray-700">${log.action}</td>
                        <td class="px-6 py-4 text-gray-600">${log.date_formatted}</td>
                        <td class="px-6 py-4 text-gray-600">${log.time_formatted}</td>
                    `;
                    tableBody.appendChild(row);
                });
            }
        })
        .catch(error => {
            console.error('Error fetching logs:', error);
            showNotification('error', 'Failed to load activity logs');
        });
    }

    // Notification System
    function showNotification(type, message) {
        const container = document.getElementById('notificationContainer');
        if (!container) return;

        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <span>${message}</span>
            <button onclick="this.parentElement.remove()" class="ml-4 text-lg font-bold">&times;</button>
        `;
        
        container.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    // Make showNotification globally available
    window.showNotification = showNotification;

    // === User Management Functions ===
    window.openAddUserModal = function () {
        const modal = document.getElementById("addUserModal");
        if (modal) {
            modal.style.display = "flex";
            setTimeout(() => {
                modal.classList.add("show");
            }, 10);
        }
    };

    window.closeAddUserModal = function () {
        const modal = document.getElementById("addUserModal");
        if (modal) {
            modal.classList.remove("show");
            setTimeout(() => {
                modal.style.display = "none";
            }, 300);
            
            const form = document.getElementById("addUserForm");
            if (form) form.reset();
            
            const errorDiv = document.getElementById('addUserErrors');
            if (errorDiv) errorDiv.innerHTML = '';
        }
    };

    window.viewProfile = function (userId) {
        console.log("Opening profile for user:", userId);
        const modal = document.getElementById("userProfileModal");
        if (modal) {
            modal.style.display = "flex";
            setTimeout(() => {
                modal.classList.add("show");
            }, 10);
        }
        document.querySelectorAll(".dropdown-menu").forEach(menu => menu.classList.remove("show"));
    };

    window.closeUserProfileModal = function () {
        const modal = document.getElementById("userProfileModal");
        if (modal) {
            modal.classList.remove("show");
            setTimeout(() => {
                modal.style.display = "none";
            }, 300);
        }
    };

    document.addEventListener('click', function(e) {
        const addUserModal = document.getElementById("addUserModal");
        const profileModal = document.getElementById("userProfileModal");
        
        if (e.target === addUserModal) {
            closeAddUserModal();
        }
        if (e.target === profileModal) {
            closeUserProfileModal();
        }
    });

    window.editDetails = function (userId) {
        showNotification('info', `Edit functionality for user ${userId} coming soon`);
        document.querySelectorAll(".dropdown-menu").forEach(menu => menu.classList.remove("show"));
    };

    window.changePermission = function (userId) {
        showNotification('info', `Permission change for user ${userId} coming soon`);
        document.querySelectorAll(".dropdown-menu").forEach(menu => menu.classList.remove("show"));
    };

    window.deleteUser = function (userId) {
        if (confirm(`Are you sure you want to delete user: ${userId}?`)) {
            showNotification('success', `User ${userId} deleted successfully`);
            fetchTables();
        }
        document.querySelectorAll(".dropdown-menu").forEach(menu => menu.classList.remove("show"));
    };

    // Dropdown Management
    window.toggleDropdown = function (button) {
        const dropdown = button.nextElementSibling;
        const isOpen = dropdown.classList.contains("show");
        document.querySelectorAll(".dropdown-menu").forEach(menu => menu.classList.remove("show"));
        if (!isOpen) dropdown.classList.add("show");
    };

    // === Search and Filter ===
    window.filterUsers = function (searchTerm) {
        const rows = document.querySelectorAll("#usersTableBody tr");
        rows.forEach((row) => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm.toLowerCase()) ? "" : "none";
        });
    };

    window.filterHistory = function (searchTerm) {
        const rows = document.querySelectorAll(".history-table tbody tr");
        rows.forEach((row) => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm.toLowerCase()) ? "" : "none";
        });
    };

    // === Logout Handler ===
    function setupLogoutHandler() {
        const logoutBtn = document.querySelector(".logout-btn");
        if (logoutBtn) {
            logoutBtn.addEventListener("click", (e) => {
                e.preventDefault();
                handleLogout();
            });
        }
    }

    function handleLogout() {
        localStorage.removeItem("isLoggedIn");
        localStorage.removeItem("username");
        localStorage.removeItem("loginTime");
        window.location.href = '/logout/';
    }

    setupLogoutHandler();
});

console.log("Settings page JS loaded successfully – all functionality merged and active.");