// Add a timestamp to prevent caching
const timestamp = new Date().getTime();
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    
    // Clear any existing error messages
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }

    // Use the same hostname as the page
    const apiUrl = `${window.location.protocol}//${window.location.host}/auth/login`;
    
    try {
        console.log('Attempting to login with:', email); // Debug log
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            },
            body: JSON.stringify({ email }),
            credentials: 'include'
        });

        console.log('Response status:', response.status); // Debug log

        if (response.ok) {
            const data = await response.json();
            console.log('Login successful:', data); // Debug log
            localStorage.setItem('token', data.access_token);
            window.location.href = '/dashboard';
        } else {
            const errorData = await response.json().catch(() => ({ detail: 'Login failed' }));
            throw new Error(errorData.detail || 'Login failed');
        }
    } catch (error) {
        console.error('Login error details:', error); // Detailed error log
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = error.message || 'An error occurred. Please try again.';
        document.querySelector('.login-form').appendChild(errorDiv);
    }
}); 