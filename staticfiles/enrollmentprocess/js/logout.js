localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('username');
        localStorage.removeItem('loginTime');

        // Set current date and time
        document.getElementById('currentDateTime').textContent = new Date().toLocaleString();

        // Calculate session duration (mock data)
        const sessionStart = new Date();
        sessionStart.setHours(sessionStart.getHours() - 2); // Mock 2 hours ago
        const sessionEnd = new Date();
        const duration = Math.round((sessionEnd - sessionStart) / (1000 * 60)); // in minutes

        document.getElementById('sessionDuration').textContent = `${Math.floor(duration / 60)}h ${duration % 60}m`;

        console.log("Logout page loaded successfully - session cleared");