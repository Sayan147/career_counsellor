// Load profile data when page loads
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/api/profile/me', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        
        if (response.ok) {
            const profile = await response.json();
            if (Object.keys(profile).length > 0) {
                document.getElementById('fullName').value = profile.full_name || '';
                document.getElementById('age').value = profile.age || '';
                document.getElementById('skills').value = profile.skills?.join(', ') || '';
                document.getElementById('experience').value = profile.experience || '';
                
                // Load education entries
                if (profile.education && profile.education.length > 0) {
                    profile.education.forEach(edu => {
                        addEducation(edu);
                    });
                } else {
                    addEducation(); // Add one empty education form
                }
            } else {
                addEducation(); // Add one empty education form for new profiles
            }
        }
    } catch (error) {
        console.error('Error loading profile:', error);
    }
});

// Handle form submission
document.getElementById('profileForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        full_name: document.getElementById('fullName').value,
        age: parseInt(document.getElementById('age').value),
        skills: document.getElementById('skills').value.split(',').map(s => s.trim()),
        experience: document.getElementById('experience').value,
        education: getEducationData()
    };
    
    try {
        const response = await fetch('/api/profile/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            window.location.href = '/dashboard';
        } else {
            const error = await response.json();
            alert('Error updating profile: ' + error.detail);
        }
    } catch (error) {
        console.error('Error saving profile:', error);
        alert('Error saving profile. Please try again.');
    }
});

// Add education entry
function addEducation(eduData = null) {
    const container = document.getElementById('educationContainer');
    const eduDiv = document.createElement('div');
    eduDiv.className = 'education-entry border rounded p-3 mb-3';
    
    eduDiv.innerHTML = `
        <div class="row">
            <div class="col-md-3 mb-2">
                <label class="form-label">Level</label>
                <select class="form-control edu-level" required>
                    <option value="">Select Level</option>
                    <option value="secondary">Secondary</option>
                    <option value="higher-secondary">Higher Secondary</option>
                    <option value="diploma">Diploma</option>
                    <option value="graduation">Graduation</option>
                    <option value="post-graduation">Post Graduation</option>
                </select>
            </div>
            <div class="col-md-4 mb-2">
                <label class="form-label">Institution</label>
                <input type="text" class="form-control edu-institution" required>
            </div>
            <div class="col-md-2 mb-2">
                <label class="form-label">Score/CGPA</label>
                <input type="number" step="0.01" class="form-control edu-score" required>
            </div>
            <div class="col-md-2 mb-2">
                <label class="form-label">Year</label>
                <input type="number" class="form-control edu-year" required>
            </div>
            <div class="col-md-1 mb-2 d-flex align-items-end">
                <button type="button" class="btn btn-danger" onclick="this.closest('.education-entry').remove()">×</button>
            </div>
        </div>
    `;
    
    container.appendChild(eduDiv);
    
    // If education data was provided, fill the fields
    if (eduData) {
        const select = eduDiv.querySelector('.edu-level');
        const institution = eduDiv.querySelector('.edu-institution');
        const score = eduDiv.querySelector('.edu-score');
        const year = eduDiv.querySelector('.edu-year');
        
        select.value = eduData.level;
        institution.value = eduData.institution;
        score.value = eduData.score;
        year.value = eduData.year_completed;
    }
}

// Get education data from form
function getEducationData() {
    const educationEntries = document.querySelectorAll('.education-entry');
    return Array.from(educationEntries).map(entry => ({
        level: entry.querySelector('.edu-level').value,
        institution: entry.querySelector('.edu-institution').value,
        score: parseFloat(entry.querySelector('.edu-score').value),
        year_completed: parseInt(entry.querySelector('.edu-year').value)
    }));
} 