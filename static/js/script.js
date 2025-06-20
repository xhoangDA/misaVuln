// Initialize GSAP
gsap.registerPlugin(ScrollTrigger);

document.addEventListener('DOMContentLoaded', function() {
    // Animate table rows on scroll
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach((row, index) => {
        gsap.from(row, {
            scrollTrigger: {
                trigger: row,
                start: "top bottom-=50",
                toggleActions: "play none none reverse"
            },
            opacity: 0,
            x: -20,
            duration: 0.4,
            delay: index * 0.1
        });
    });

    // Add hover effect for buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            gsap.to(btn, {
                scale: 1.05,
                duration: 0.3,
                ease: "power2.out"
            });
        });

        btn.addEventListener('mouseleave', () => {
            gsap.to(btn, {
                scale: 1,
                duration: 0.3,
                ease: "power2.out"
            });
        });
    });

    // Add hover effect for cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            gsap.to(card, {
                y: -10,
                duration: 0.3,
                ease: "power2.out",
                boxShadow: "0 10px 20px rgba(0, 228, 255, 0.1)"
            });
        });

        card.addEventListener('mouseleave', () => {
            gsap.to(card, {
                y: 0,
                duration: 0.3,
                ease: "power2.out",
                boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)"
            });
        });
    });

    // Form submission handling with loading animation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                return;
            }
            
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.classList.add('loading');
                gsap.to(submitBtn, {
                    scale: 0.95,
                    duration: 0.2
                });
            }
        });
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Notification system
    window.showNotification = function(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        gsap.fromTo(notification, 
            { opacity: 0, y: 20 },
            { 
                opacity: 1, 
                y: 0, 
                duration: 0.3,
                ease: "power2.out"
            }
        );

        setTimeout(() => {
            gsap.to(notification, {
                opacity: 0,
                y: 20,
                duration: 0.3,
                ease: "power2.in",
                onComplete: () => notification.remove()
            });
        }, 3000);
    };

    // Add scroll to top functionality
    const scrollTopBtn = document.getElementById('scrollToTop');
    if (scrollTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                gsap.to(scrollTopBtn, {
                    opacity: 1,
                    y: 0,
                    duration: 0.3,
                    ease: "power2.out"
                });
            } else {
                gsap.to(scrollTopBtn, {
                    opacity: 0,
                    y: 20,
                    duration: 0.3,
                    ease: "power2.in"
                });
            }
        });

        scrollTopBtn.addEventListener('click', () => {
            gsap.to(window, {
                duration: 1,
                scrollTo: 0,
                ease: "power2.inOut"
            });
        });
    }
});