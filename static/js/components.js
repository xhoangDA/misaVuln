document.addEventListener('DOMContentLoaded', function() {
    // Cache DOM elements
    const searchInput = document.getElementById('search');
    const categoryFilter = document.getElementById('categoryFilter');
    const projectFilter = document.getElementById('projectFilter');
    const resultsCount = document.getElementById('resultsCount');
    const tableRows = document.querySelectorAll('#componentTableBody tr');
    
    console.log('Total rows found:', tableRows.length);
    
    // Simple filter function without animations
    function filterComponents() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        const selectedCategory = categoryFilter.value;
        const selectedProject = projectFilter.value;
        
        let visibleCount = 0;
        
        tableRows.forEach(row => {
            const nameCell = row.cells[1];
            const categoryCell = row.cells[3];
            const projectCell = row.cells[4];
            
            if (!nameCell || !categoryCell || !projectCell) return;
            
            // Get text content directly
            const name = nameCell.textContent.toLowerCase().trim();
            const category = categoryCell.textContent.trim();
            const project = projectCell.textContent.trim();
            
            let shouldShow = true;
            
            // Search filter
            if (searchTerm && !name.includes(searchTerm)) {
                shouldShow = false;
            }
            
            // Category filter
            if (shouldShow && selectedCategory && !category.includes(selectedCategory)) {
                shouldShow = false;
            }
            
            // Project filter  
            if (shouldShow && selectedProject && !project.includes(selectedProject)) {
                shouldShow = false;
            }
            
            // Show/hide row immediately
            if (shouldShow) {
                row.style.display = 'table-row';
                row.style.opacity = '1';
                row.style.visibility = 'visible';
                visibleCount++;
            } else {
                row.style.display = 'none';
            }
        });
        
        updateResultsCount(visibleCount);
    }
    
    function updateResultsCount(count = null) {
        if (count === null) {
            count = Array.from(tableRows).filter(row => row.style.display !== 'none').length;
        }
        resultsCount.textContent = `Hiển thị ${count} kết quả`;
    }
    
    function resetFilters() {
        searchInput.value = '';
        categoryFilter.value = '';
        projectFilter.value = '';
        
        tableRows.forEach(row => {
            row.style.display = 'table-row';
            row.style.opacity = '1';
            row.style.visibility = 'visible';
        });
        updateResultsCount(tableRows.length);
    }
    
    // Populate filter options
    function populateFilterOptions() {
        const categories = new Set();
        const projects = new Set();
        
        tableRows.forEach(row => {
            const categoryText = row.cells[3] ? row.cells[3].textContent.trim() : '';
            const projectText = row.cells[4] ? row.cells[4].textContent.trim() : '';
            
            if (categoryText && categoryText !== 'N/A' && !categoryText.includes('badge')) {
                // Extract text from badge elements
                const categoryElement = row.cells[3].querySelector('.badge');
                if (categoryElement) {
                    categories.add(categoryElement.textContent.trim());
                }
            }
            if (projectText && projectText !== 'N/A' && projectText !== '-') {
                projects.add(projectText);
            }
        });
        
        categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            categoryFilter.appendChild(option);
        });
        
        projects.forEach(project => {
            const option = document.createElement('option');
            option.value = project;
            option.textContent = project;
            projectFilter.appendChild(option);
        });
    }
    
    // Initialize
    populateFilterOptions();
    updateResultsCount();
    
    // Event listeners - immediate response
    searchInput.addEventListener('input', filterComponents);
    categoryFilter.addEventListener('change', filterComponents);
    projectFilter.addEventListener('change', filterComponents);
    
    // Global reset function
    window.resetFilters = resetFilters;
    
    console.log(`Loaded ${tableRows.length} components successfully`);
});

// --- Make allComponentsList available for modal popup ---
window.allComponentsList = Array.from(document.querySelectorAll('#componentTableBody tr')).map(row => {
    return {
        id: row.getAttribute('data-id'),
        name: row.cells[1]?.textContent.trim() || '',
        version: row.cells[2]?.textContent.trim() || '',
        category: row.cells[3]?.textContent.trim() || '',
        project_name: row.cells[4]?.textContent.trim() || '',
        manager: row.cells[5]?.textContent.trim() || '',
        description: row.cells[6]?.textContent.trim() || ''
    };
});

// Add component management functions
window.editComponent = function(id) {
    fetch(`/components/${id}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('editComponentId').value = data.id;
            document.getElementById('editComponentName').value = data.name;
            document.getElementById('editComponentVersion').value = data.version || '';
            document.getElementById('editComponentCategory').value = data.category || '';
            document.getElementById('editComponentVendor').value = data.vendor || '';
            document.getElementById('editComponentProject').value = data.project_id || '';
            document.getElementById('editComponentManagerName').value = data.manager_name || '';
            document.getElementById('editComponentDescription').value = data.description || '';
            document.getElementById('editComponentNotes').value = data.notes || '';
            
            new bootstrap.Modal(document.getElementById('editComponentModal')).show();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error loading component data');
        });
};

window.deleteComponent = function(id, name) {
    document.getElementById('componentToDelete').textContent = name;
    window.componentToDeleteId = id;
    new bootstrap.Modal(document.getElementById('deleteConfirmModal')).show();
};

// Save component
document.getElementById('saveComponent')?.addEventListener('click', function() {
    const form = document.getElementById('addComponentForm');
    const formData = new FormData(form);
    
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });
    
    fetch('/components', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            location.reload();
        } else if (data.error) {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error creating component');
    });
});

// Update component
document.getElementById('updateComponent')?.addEventListener('click', function() {
    const form = document.getElementById('editComponentForm');
    const formData = new FormData(form);
    const componentId = formData.get('id');
    
    const data = {};
    formData.forEach((value, key) => {
        if (key !== 'id') {
            data[key] = value;
        }
    });
    
    fetch(`/components/${componentId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            location.reload();
        } else if (data.error) {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error updating component');
    });
});

// Confirm delete
document.getElementById('confirmDelete')?.addEventListener('click', function() {
    if (!window.componentToDeleteId) return;
    
    fetch(`/components/${window.componentToDeleteId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            location.reload();
        } else if (data.error) {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error deleting component');
    });
});

// Import components
document.getElementById('importComponents')?.addEventListener('click', function() {
    const form = document.getElementById('importComponentForm');
    const formData = new FormData(form);
    
    if (!formData.get('csv_file')) {
        alert('Please select a CSV file');
        return;
    }
    
    fetch('/components/import_csv', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            location.reload();
        } else if (data.error) {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error importing components');
    });
});

// Project change handler
document.querySelector('select[name="project_id"]')?.addEventListener('change', function() {
    const projectId = this.value;
    const managerField = document.querySelector('input[name="manager_name"]');
    
    if (projectId && managerField) {
        fetch(`/get_project_info?project_id=${projectId}`)
            .then(response => response.json())
            .then(data => {
                managerField.value = data.manager_name || '';
            })
            .catch(error => {
                console.error('Error:', error);
                managerField.value = '';
            });
    } else if (managerField) {
        managerField.value = '';
    }
});

// --- Technology List Modal Logic ---
let currentTechComponentList = [];

function openTechnologyListModal(components, techName) {
    const modal = document.getElementById('technologyListModal');
    const tbody = document.getElementById('technologyListTableBody');
    const title = document.querySelector('.technology-list-modal-title');
    title.textContent = `Technology list: ${techName}`;
    tbody.innerHTML = '';
    currentTechComponentList = components;
    components.forEach((comp, idx) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${idx + 1}</td>
            <td>${comp.name || ''}</td>
            <td>${comp.version || ''}</td>
            <td>${comp.category || ''}</td>
            <td>${comp.project_name || ''}</td>
            <td>${comp.manager || ''}</td>
            <td>${comp.description || ''}</td>
            <td>
                <button class="btn btn-outline-primary btn-sm" onclick="editComponentFromModal(${comp.id})"><i class="fas fa-edit"></i></button>
                <button class="btn btn-outline-danger btn-sm" onclick="deleteComponentFromModal(${comp.id})"><i class="fas fa-trash"></i></button>
            </td>
        `;
        tbody.appendChild(tr);
    });
    modal.classList.add('active');
}

function closeTechnologyListModal() {
    document.getElementById('technologyListModal').classList.remove('active');
}

// These functions should call the same logic as the main table
function editComponentFromModal(id) {
    if (typeof editComponent === 'function') {
        editComponent(id);
        closeTechnologyListModal();
    }
}
function deleteComponentFromModal(id) {
    if (typeof deleteComponent === 'function') {
        deleteComponent(id);
        closeTechnologyListModal();
    }
}

// --- Bind click event for mini-tech-card ---
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.mini-tech-card').forEach(card => {
        card.addEventListener('click', function() {
            const techName = card.getAttribute('data-tech-name') || card.querySelector('.tech-name')?.textContent?.trim() || '';
            // Fetch or filter component list for this technology
            let components = [];
            if (window.allComponentsList && Array.isArray(window.allComponentsList)) {
                components = window.allComponentsList.filter(c => (c.name || '').toLowerCase() === techName.toLowerCase());
            }
            openTechnologyListModal(components, techName);
        });
    });
});
