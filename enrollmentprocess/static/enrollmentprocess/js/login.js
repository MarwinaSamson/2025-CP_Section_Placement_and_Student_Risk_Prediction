// Login functionality
function togglePassword() {
    const passwordField = document.getElementById('password');
    const passwordIcon = document.getElementById('password-icon');
    
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        passwordIcon.textContent = '🙈';
    } else {
        passwordField.type = 'password';
        passwordIcon.textContent = '👁️';
    }
}

function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // Simple validation
    if (!username || !password) {
        alert('Please fill in all required fields.');
        return;
    }
    
    // Simulate login process
    alert('Login functionality would be implemented here. Please contact the system administrator for access.');
}