document.addEventListener('DOMContentLoaded', function() {
    // Theme switching functionality
    const themeSwitch = document.getElementById('theme-switch');
    const body = document.body;
    
    // Check if there's a saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        body.classList.add('light-theme');
    }
    
    // Theme switch button event listener
    if (themeSwitch) {
        themeSwitch.addEventListener('click', function() {
            body.classList.toggle('light-theme');
            
            // Save theme preference
            if (body.classList.contains('light-theme')) {
                localStorage.setItem('theme', 'light');
            } else {
                localStorage.setItem('theme', 'dark');
            }
        });
    }
    
    // Offline detection
    const offlineAlert = document.getElementById('offline-alert');
    
    function updateOnlineStatus() {
        if (navigator.onLine) {
            if (offlineAlert) {
                offlineAlert.style.display = 'none';
            }
        } else {
            if (offlineAlert) {
                offlineAlert.style.display = 'block';
            }
        }
    }
    
    // Initial check
    updateOnlineStatus();
    
    // Add event listeners for online/offline events
    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);
});