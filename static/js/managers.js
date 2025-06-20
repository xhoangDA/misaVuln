// JS for managers.html

// Add Manager
const saveManagerBtn = document.getElementById('saveManager');
if (saveManagerBtn) {
    saveManagerBtn.addEventListener('click', function() {
        const form = document.getElementById('addManagerForm');
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => { data[key] = value; });
        fetch('/managers', {
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
        .catch(err => {
            alert('Error creating manager');
        });
    });
}

// Edit Manager (open modal and populate)
window.editManager = function(id) {
    fetch(`/managers/${id}`)
        .then(res => res.json())
        .then(data => {
            const m = data.manager || data;
            document.getElementById('editManagerId').value = m.id;
            document.getElementById('editManagerEmployeeCode').value = m.employee_code;
            document.getElementById('editManagerName').value = m.name;
            new bootstrap.Modal(document.getElementById('editManagerModal')).show();
        })
        .catch(() => alert('Error loading manager data'));
};

// Update Manager
const updateManagerBtn = document.getElementById('updateManager');
if (updateManagerBtn) {
    updateManagerBtn.addEventListener('click', function() {
        const form = document.getElementById('editManagerForm');
        const formData = new FormData(form);
        const id = formData.get('id');
        const data = {};
        formData.forEach((value, key) => { if (key !== 'id') data[key] = value; });
        fetch(`/managers/${id}`, {
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
        .catch(() => alert('Error updating manager'));
    });
}

// Delete Manager (open modal)
window.deleteManager = function(id, name) {
    document.getElementById('managerNameToDelete').textContent = name;
    window.managerToDeleteId = id;
    new bootstrap.Modal(document.getElementById('deleteManagerModal')).show();
};

// Confirm Delete
const confirmDeleteBtn = document.getElementById('confirmDeleteManager');
if (confirmDeleteBtn) {
    confirmDeleteBtn.addEventListener('click', function() {
        if (!window.managerToDeleteId) return;
        fetch(`/managers/${window.managerToDeleteId}`, {
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
        .catch(() => alert('Error deleting manager'));
    });
}

// Import Managers
const importManagerBtn = document.getElementById('importManager');
if (importManagerBtn) {
    importManagerBtn.addEventListener('click', function() {
        const form = document.getElementById('importManagerForm');
        const formData = new FormData(form);
        if (!formData.get('csv_file')) {
            alert('Please select a CSV file');
            return;
        }
        fetch('/managers/import', {
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
        .catch(() => alert('Error importing managers'));
    });
}
