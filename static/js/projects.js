// JS for projects.html (tách từ <script> trong projects.html nếu có)
// Copy toàn bộ code JS từ block <script> trong projects.html vào đây.

// Add Project
const saveProjectBtn = document.getElementById('saveProject');
if (saveProjectBtn) {
    saveProjectBtn.addEventListener('click', function() {
        const form = document.getElementById('addProjectForm');
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => { data[key] = value; });
        fetch('/projects', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(data => {
            if (data.message) {
                location.reload();
            } else if (data.error) {
                alert('Error: ' + data.error);
            }
        })
        .catch(() => alert('Error creating project'));
    });
}

// Edit Project (open modal and populate)
window.editProject = function(id) {
    fetch(`/projects/${id}`)
        .then(res => res.json())
        .then(data => {
            const p = data.project || data;
            document.getElementById('editProjectId').value = p.id;
            document.getElementById('editProjectCode').value = p.project_code;
            document.getElementById('editProjectKey').value = p.key;
            document.getElementById('editProjectName').value = p.project_name;
            document.getElementById('editProjectManager').value = p.manager_id;
            new bootstrap.Modal(document.getElementById('editProjectModal')).show();
        })
        .catch(() => alert('Error loading project data'));
};

// Update Project
const updateProjectBtn = document.getElementById('updateProject');
if (updateProjectBtn) {
    updateProjectBtn.addEventListener('click', function() {
        const form = document.getElementById('editProjectForm');
        const formData = new FormData(form);
        const id = formData.get('id');
        const data = {};
        formData.forEach((value, key) => { if (key !== 'id') data[key] = value; });
        fetch(`/projects/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(data => {
            if (data.message) {
                location.reload();
            } else if (data.error) {
                alert('Error: ' + data.error);
            }
        })
        .catch(() => alert('Error updating project'));
    });
}

// Delete Project (open modal)
window.deleteProject = function(id, name) {
    document.getElementById('projectNameToDelete').textContent = name;
    window.projectToDeleteId = id;
    new bootstrap.Modal(document.getElementById('deleteProjectModal')).show();
};

// Confirm Delete
const confirmDeleteBtn = document.getElementById('confirmDeleteProject');
if (confirmDeleteBtn) {
    confirmDeleteBtn.addEventListener('click', function() {
        if (!window.projectToDeleteId) return;
        fetch(`/projects/${window.projectToDeleteId}`, {
            method: 'DELETE'
        })
        .then(res => res.json())
        .then(data => {
            if (data.message) {
                location.reload();
            } else if (data.error) {
                alert('Error: ' + data.error);
            }
        })
        .catch(() => alert('Error deleting project'));
    });
}

// Import Projects
const importProjectBtn = document.getElementById('importProject');
if (importProjectBtn) {
    importProjectBtn.addEventListener('click', function() {
        const form = document.getElementById('importProjectForm');
        const formData = new FormData(form);
        if (!formData.get('json_file')) {
            alert('Please select a JSON file');
            return;
        }
        fetch('/projects/import', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                location.reload();
            } else if (data.error) {
                alert('Error: ' + data.error);
            }
        })
        .catch(() => alert('Error importing projects'));
    });
}
// ...end of projects.js
