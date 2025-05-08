// Check authentication
const token = localStorage.getItem('token');
if (!token) {
    window.location.href = '/';
}

// Navigation
const navItems = document.querySelectorAll('.nav-item');
const pages = document.querySelectorAll('.page');

navItems.forEach(item => {
    item.addEventListener('click', () => {
        if (item.classList.contains('logout')) {
            localStorage.removeItem('token');
            window.location.href = '/';
            return;
        }

        const targetPage = item.dataset.page;
        
        // Update active states
        navItems.forEach(navItem => navItem.classList.remove('active'));
        pages.forEach(page => page.classList.remove('active'));
        
        item.classList.add('active');
        document.getElementById(targetPage).classList.add('active');
    });
});

// Add authorization header to all fetch requests
const originalFetch = window.fetch;
window.fetch = function() {
    let [resource, config] = arguments;
    if (!config) {
        config = {};
    }
    if (!config.headers) {
        config.headers = {};
    }

    // Add authorization header for all requests
    if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
    }

    // Add CORS headers
    config.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate';
    config.headers['Pragma'] = 'no-cache';
    config.headers['Expires'] = '0';

    return originalFetch(resource, config);
}; 