
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
            const formData = new FormData(this);
            const actionUrl = this.action;

            fetch(actionUrl, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then(response => {
                return response.json().then(data => {
                    if (!response.ok) {
                        // Backend returned error or non-200 status
                        throw new Error(data.message || JSON.stringify(data.errors) || "Unknown error");
                    }
                    return data;
                }).catch(() => {
                    throw new Error("Invalid JSON response from server.");
                });
            })

            .then(data => {
                const errorDiv = document.getElementById('addUserErrors');
                if (data.success) {
                    alert(data.message || 'User added successfully!');
                    closeAddUserModal();
                    fetchTables();
                } else if (errorDiv) {
                    errorDiv.innerHTML = formatErrors(data.errors);
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
                alert(`Submission failed: ${error.message}`);
            });

        });
    }

    // Error Formatter
    function formatErrors(errors) {
        let html = '<ul>';
        for (let field in errors) html += `<li>${field}: ${errors[field]}</li>`;
        return html + '</ul>';
    }

    // Table Fetchers
    function fetchTables() {
        fetchUsersTable();
        fetchHistoryTable();
    }

    function fetchUsersTable() {
        fetch('/admin-functionalities/settings/get-users/', {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('usersTableBody');
            if (tableBody && data.users) {
                tableBody.innerHTML = '';
                data.users.forEach(user => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>
                            <div class="user-info">
                                <img src="/static/admin_functionalities/assets/kakashi.jpeg" alt="User" class="user-avatar" />
                                <div>
                                    <div class="user-name">${user.first_name} ${user.last_name}</div>
                                    <div class="user-email">${user.email}</div>
                                </div>
                            </div>
                        </td>
                        <td>
                            ${user.is_superuser ? '<span class="access-badge admin">Admin</span>' : ''}
                            ${user.is_staff_expert ? '<span class="access-badge staff">Staff Expert</span>' : ''}
                            ${user.is_subject_teacher ? '<span class="access-badge teacher">Subject Teacher</span>' : ''}
                            ${user.is_adviser ? '<span class="access-badge adviser">Adviser</span>' : ''}
                        </td>
                        <td>${user.last_login_formatted || user.date_joined_formatted}</td>
                        <td>${user.date_joined_formatted}</td>
                        <td>
                            <div class="actions-dropdown">
                                <button class="actions-btn" onclick="toggleDropdown(this)">
                                    <i class="fas fa-ellipsis-v"></i>
                                </button>
                                <div class="dropdown-menu">
                                    <a href="#" onclick="viewProfile('${user.id}')"><i class="fas fa-eye"></i> View Profile</a>
                                    <a href="#" onclick="editDetails('${user.id}')"><i class="fas fa-edit"></i> Edit Details</a>
                                    <a href="#" onclick="changePermission('${user.id}')"><i class="fas fa-user-cog"></i> Change Permission</a>
                                    <a href="#" onclick="deleteUser('${user.id}')" class="delete-action"><i class="fas fa-trash"></i> Delete User</a>
                                </div>
                            </div>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });
            }
        })
        .catch(error => console.error('Error fetching users:', error));
    }

    function fetchHistoryTable() {
        fetch('/admin-functionalities/settings/get-logs/', {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#history-tab tbody');
            if (tableBody && data.logs) {
                tableBody.innerHTML = '';
                data.logs.forEach(log => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>
                            <div class="user-info">
                                <img src="/static/admin_functionalities/assets/kakashi.jpeg" alt="User" class="user-avatar small" />
                                <div>
                                    <div class="user-name">${log.user_full_name}</div>
                                    <div class="user-role">${log.user_role}</div>
                                </div>
                            </div>
                        </td>
                        <td>${log.action}</td>
                        <td>${log.date_formatted}</td>
                        <td>${log.time_formatted}</td>
                    `;
                    tableBody.appendChild(row);
                });
            }
        })
        .catch(error => console.error('Error fetching logs:', error));
    }

    // === User Management Functions ===
    window.openAddUserModal = function () {
        const modal = document.getElementById("addUserModal");
        if (modal) modal.style.display = "block";
    };

    window.closeAddUserModal = function () {
        const modal = document.getElementById("addUserModal");
        if (modal) {
            modal.style.display = "none";
            const form = document.getElementById("addUserForm");
            if (form) form.reset();
        }
    };

    window.viewProfile = function (userId) {
        console.log("Opening profile for user:", userId);
        document.getElementById("userProfileModal").style.display = "block";
        document.querySelectorAll(".dropdown-menu").forEach(menu => menu.classList.remove("show"));
    };

    window.closeUserProfileModal = function () {
        document.getElementById("userProfileModal").style.display = "none";
    };

    window.editDetails = function (userId) {
        alert(`Edit details for user: ${userId}`);
        document.querySelectorAll(".dropdown-menu").forEach(menu => menu.classList.remove("show"));
    };

    window.changePermission = function (userId) {
        alert(`Change permissions for user: ${userId}`);
        document.querySelectorAll(".dropdown-menu").forEach(menu => menu.classList.remove("show"));
    };

    window.deleteUser = function (userId) {
        if (confirm(`Are you sure you want to delete user: ${userId}?`)) {
            alert(`User ${userId} deleted successfully`);
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
            const userName = row.querySelector(".user-name")?.textContent.toLowerCase() || '';
            const userEmail = row.querySelector(".user-email")?.textContent.toLowerCase() || '';
            row.style.display = (userName.includes(searchTerm.toLowerCase()) || userEmail.includes(searchTerm.toLowerCase())) ? "" : "none";
        });
    };

    window.filterHistory = function (searchTerm) {
        const rows = document.querySelectorAll(".history-table tbody tr");
        rows.forEach((row) => {
            const userName = row.querySelector(".user-name")?.textContent.toLowerCase() || '';
            const activity = row.cells[1]?.textContent.toLowerCase() || '';
            row.style.display = (userName.includes(searchTerm.toLowerCase()) || activity.includes(searchTerm.toLowerCase())) ? "" : "none";
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
