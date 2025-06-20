// Modal backdrop fix utility
window.modalUtils = {
    // Safely hide modal and remove backdrop
    hideModal: function(modalId) {
        const modalElement = document.getElementById(modalId);
        if (modalElement) {
            const modal = bootstrap.Modal.getInstance(modalElement);
            if (modal) {
                modal.hide();
            }
            
            // Force remove any remaining backdrops
            setTimeout(() => {
                const backdrops = document.querySelectorAll('.modal-backdrop');
                backdrops.forEach(backdrop => {
                    backdrop.remove();
                });
                
                // Remove modal-open class from body
                document.body.classList.remove('modal-open');
                document.body.style.overflow = '';
                document.body.style.paddingRight = '';
            }, 300);
        }
    },
    
    // Clean up all modal states
    cleanupModals: function() {
        // Remove all backdrops
        const backdrops = document.querySelectorAll('.modal-backdrop');
        backdrops.forEach(backdrop => {
            backdrop.remove();
        });
        
        // Reset body styles
        document.body.classList.remove('modal-open');
        document.body.style.overflow = '';
        document.body.style.paddingRight = '';
        
        // Hide all visible modals
        const visibleModals = document.querySelectorAll('.modal.show');
        visibleModals.forEach(modal => {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) {
                modalInstance.hide();
            }
        });
    }
};

// Add global cleanup on page load
document.addEventListener('DOMContentLoaded', function() {
    // Clean up any remaining modal states
    window.modalUtils.cleanupModals();
    
    // Add event listeners to all modal close buttons
    document.querySelectorAll('[data-bs-dismiss="modal"]').forEach(button => {
        button.addEventListener('click', function() {
            setTimeout(() => {
                window.modalUtils.cleanupModals();
            }, 100);
        });
    });
    
    // Listen for modal events
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('hidden.bs.modal', function() {
            setTimeout(() => {
                window.modalUtils.cleanupModals();
            }, 100);
        });
        
        modal.addEventListener('hide.bs.modal', function() {
            setTimeout(() => {
                window.modalUtils.cleanupModals();
            }, 100);
        });
    });
    
    // Emergency escape key handler
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            setTimeout(() => {
                window.modalUtils.cleanupModals();
            }, 200);
        }
    });
});

// Add a button to manually fix stuck modals (for debugging)
window.addEventListener('load', function() {
    // Add emergency fix button (hidden by default)
    const fixButton = document.createElement('button');
    fixButton.innerHTML = '<i class="fas fa-times"></i> Modal';
    fixButton.className = 'btn btn-sm btn-danger';
    fixButton.style.cssText = `
        position: fixed;
        top: 10px;
        left: 10px;
        z-index: 9999;
        display: none;
    `;
    fixButton.onclick = () => {
        window.modalUtils.cleanupModals();
        fixButton.style.display = 'none';
    };
    document.body.appendChild(fixButton);
    
    // Show fix button if backdrop exists for more than 2 seconds
    setInterval(() => {
        const backdrops = document.querySelectorAll('.modal-backdrop');
        const visibleModals = document.querySelectorAll('.modal.show');
        
        if (backdrops.length > 0 && visibleModals.length === 0) {
            fixButton.style.display = 'block';
        } else {
            fixButton.style.display = 'none';
        }
    }, 2000);
});
