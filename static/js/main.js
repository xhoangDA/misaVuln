// Initialize GSAP
gsap.registerPlugin(ScrollTrigger);

// Animate elements on page load
document.addEventListener('DOMContentLoaded', function() {
    // Animate navbar items
    gsap.from('.nav-item', {
        opacity: 0,
        y: -20,
        duration: 0.5,
        stagger: 0.1
    });

    // Animate hero section
    gsap.from('.hero-content', {
        opacity: 0,
        y: 50,
        duration: 1
    });

    // Animate cards on scroll
    gsap.utils.toArray('.card').forEach(card => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: "top bottom-=100",
                toggleActions: "play none none reverse"
            },
            opacity: 0,
            y: 50,
            duration: 0.6
        });
    });

    // Table row animations
    gsap.utils.toArray('tbody tr').forEach(row => {
        gsap.from(row, {
            scrollTrigger: {
                trigger: row,
                start: "top bottom-=50",
                toggleActions: "play none none reverse"
            },
            opacity: 0,
            x: -20,
            duration: 0.4
        });
    });

    // Add hover effects for buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', (e) => {
            gsap.to(btn, {
                scale: 1.05,
                duration: 0.3
            });
        });

        btn.addEventListener('mouseleave', (e) => {
            gsap.to(btn, {
                scale: 1,
                duration: 0.3
            });
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                gsap.to(window, {
                    duration: 1,
                    scrollTo: target,
                    ease: "power2.inOut"
                });
            }
        });
    });

    // Add loading animation for form submissions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.classList.add('loading');
                submitBtn.disabled = true;
            }
        });
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add notification system
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
            { opacity: 1, y: 0, duration: 0.3 }
        );

        setTimeout(() => {
            gsap.to(notification, {
                opacity: 0,
                y: 20,
                duration: 0.3,
                onComplete: () => notification.remove()
            });
        }, 3000);
    };

    // Set default dates for scan form if exist
    const endDateInput = document.getElementById('endDate');
    const startDateInput = document.getElementById('startDate');
    if (endDateInput && startDateInput) {
        const today = new Date();
        const thirtyDaysAgo = new Date(today.getTime() - (30 * 24 * 60 * 60 * 1000));
        endDateInput.value = today.toISOString().split('T')[0];
        startDateInput.value = thirtyDaysAgo.toISOString().split('T')[0];
    }

    // Setup scan button
    const scanBtn = document.getElementById('startScanBtn');
    if (scanBtn) {
        scanBtn.onclick = startCVEScan;
    }

    // Setup filter
    const filterInput = document.getElementById('vulnerabilityFilter');
    if (filterInput) {
        filterInput.addEventListener('input', filterVulnerabilities);
    }

    // Load system statistics
    loadSystemStats();

    // Initialize animations
    initializeAnimations();
});

// === CVE Scan Logic ===
let currentScanResults = null;
let scanStartTime = null;
let scanTimer = null;

function startCVEScan() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    if (!startDate || !endDate) {
        showNotification('Please select both start and end dates', 'error');
        return;
    }
    // Show progress
    const progressSection = document.getElementById('scanProgressSection');
    const resultsSection = document.getElementById('scanResultsSection');
    if (progressSection) progressSection.style.display = 'block';
    if (resultsSection) resultsSection.style.display = 'none';
    // Disable button
    const scanBtn = document.getElementById('startScanBtn');
    if (scanBtn) {
        scanBtn.disabled = true;
        scanBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Scanning...';
    }
    // Progress bar
    let progress = 0;
    const progressBar = document.getElementById('scanProgressBar');
    const progressText = document.getElementById('scanProgressText');
    const updateProgress = setInterval(() => {
        if (progress < 95) {
            progress += 1;
            if (progressBar) progressBar.style.width = progress + '%';
            if (progressText) progressText.textContent = progress + '%';
        }
    }, 1000);
    // Start timer
    scanStartTime = Date.now();
    scanTimer = setInterval(() => {
        const elapsed = Math.floor((Date.now() - scanStartTime) / 1000);
        const timerElement = document.getElementById('scanElapsedTime');
        if (timerElement) timerElement.textContent = elapsed + 's';
    }, 1000);
    // Fetch
    fetch('/cve-scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start_date: startDate, end_date: endDate })
    })
    .then(res => res.json())
    .then(data => {
        clearInterval(updateProgress);
        clearInterval(scanTimer);
        if (data.success) {
            handleScanSuccess(data);
        } else {
            handleScanError(data.error || 'Unknown error');
        }
    })
    .catch(err => {
        clearInterval(updateProgress);
        clearInterval(scanTimer);
        handleScanError('Network error: ' + err.message);
    });
}

function handleScanSuccess(data) {
    currentScanResults = data;
    document.getElementById('scanProgressSection').style.display = 'none';
    document.getElementById('scanResultsSection').style.display = 'block';
    
    // Update summary - FIX: Change scan_stats to stats to match backend response
    document.getElementById('criticalCount').textContent = data.stats.critical || 0;
    document.getElementById('highCount').textContent = data.stats.high || 0;
    document.getElementById('mediumCount').textContent = data.stats.medium || 0;
    document.getElementById('lowCount').textContent = data.stats.low || 0;
    
    // Populate table
    populateVulnerabilitiesTable(data.vulnerabilities);
    
    // Enable button
    const scanBtn = document.getElementById('startScanBtn');
    if (scanBtn) {
        scanBtn.disabled = false;
        scanBtn.innerHTML = '<span class="btn-bg"></span><i class="fas fa-search"></i><span>Start CVE Scan</span>';
    }
    
    showNotification(`Scan completed! Found ${data.stats.vulnerabilities_found} vulnerabilities.`, 'success');
}

function handleScanError(error) {
    document.getElementById('scanProgressSection').style.display = 'none';
    document.getElementById('scanResultsSection').style.display = 'block';
    const scanBtn = document.getElementById('startScanBtn');
    if (scanBtn) {
        scanBtn.disabled = false;
        scanBtn.innerHTML = '<span class="btn-bg"></span><i class="fas fa-search"></i><span>Start CVE Scan</span>';
    }
    showNotification('Scan failed: ' + error, 'error');
    // Optionally show error in results section
}

function populateVulnerabilitiesTable(vulnerabilities) {
    const tbody = document.getElementById('vulnerabilitiesTableBody');
    if (!tbody) return;
    tbody.innerHTML = '';
    
    // Group vulnerabilities by CVE ID first
    const cveGroups = {};
    vulnerabilities.forEach(vuln => {
        const cveId = vuln.cve.cve_id;
        if (!cveGroups[cveId]) {
            cveGroups[cveId] = [];
        }
        cveGroups[cveId].push(vuln);
    });
    
    // Create unique vulnerabilities array (1 per CVE)
    const uniqueVulnerabilities = Object.values(cveGroups).map(group => {
        // Choose the vulnerability with highest risk level as representative
        const sortedGroup = group.sort((a, b) => {
            const riskA = getRiskPriority(a.analysis.risk_assessment);
            const riskB = getRiskPriority(b.analysis.risk_assessment);
            return riskB - riskA;
        });
        
        const mainVuln = sortedGroup[0];
        
        // Add affected technologies list to the main vulnerability
        mainVuln.affectedTechnologies = group.map(v => ({
            name: v.technology.name,
            version: v.technology.version,
            project_name: v.technology.project_name,
            manager_name: v.technology.manager_name
        }));
        
        return mainVuln;
    });
    
    // Sort by risk priority
    const sortedVulnerabilities = uniqueVulnerabilities.sort((a, b) => {
        const riskA = getRiskPriority(a.analysis.risk_assessment);
        const riskB = getRiskPriority(b.analysis.risk_assessment);
        return riskB - riskA; // Descending order (highest risk first)
    });
    
    sortedVulnerabilities.forEach((vuln, index) => {
        const row = document.createElement('tr');
        const riskClass = vuln.analysis.risk_assessment.toLowerCase();
        const riskBadge = `<span class="badge bg-${getRiskColor(riskClass)}">${vuln.analysis.risk_assessment}</span>`;
        const confidenceScore = (vuln.analysis.confidence_score * 100).toFixed(0);
        const confidenceBadge = `<span class="badge bg-info">${confidenceScore}%</span>`;
        const publishDate = new Date(vuln.cve.publish_date).toLocaleDateString();
        const cvssScore = vuln.cve.cvss_data.baseScore || 'N/A';
        
        // Show primary technology name + version, with count if multiple
        const primaryTech = vuln.technology;
        const techCount = vuln.affectedTechnologies ? vuln.affectedTechnologies.length : 1;
        const techDisplayName = techCount > 1 ? 
            `${primaryTech.name} (+${techCount - 1} more)` : 
            primaryTech.name;
        
        row.innerHTML = `
            <td><span class="badge bg-primary bg-opacity-10 text-primary border border-primary fw-semibold">${index + 1}</span></td>
            <td>${riskBadge}</td>
            <td><a href="#" onclick="showCVEDetails('${vuln.cve.cve_id}')" class="text-decoration-none"><strong>${vuln.cve.cve_id}</strong></a></td>
            <td>
                <div class="d-flex align-items-center">
                    <div class="avatar-circle me-2">
                        <i class="fas fa-microchip"></i>
                    </div>
                    <div>
                        <strong>${techDisplayName}</strong>
                        ${primaryTech.version ? `<small class="text-muted d-block">v${primaryTech.version}</small>` : ''}
                        ${techCount > 1 ? `<small class="text-info d-block">${techCount} components affected</small>` : ''}
                    </div>
                </div>
            </td>
            <td><span class="badge bg-${getCVSSColor(cvssScore)}">${cvssScore}</span></td>
            <td>${confidenceBadge}</td>
            <td><div class="text-info small"><div><strong>${publishDate}</strong></div></div></td>
            <td><div class="btn-group btn-group-sm"><button class="btn btn-outline-primary" onclick="showCVEDetails('${vuln.cve.cve_id}')"><i class="fas fa-eye"></i></button></div></td>
        `;
        tbody.appendChild(row);
    });
}

// Đảm bảo showCVEDetails có thể gọi từ HTML onclick
function getRiskPriority(risk) {
    const map = { 'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1 };
    return map[risk?.toUpperCase()] || 0;
}

function showCVEDetails(cveId) {
    if (!currentScanResults) return;
    const affectedVulns = currentScanResults.vulnerabilities.filter(v => v.cve.cve_id === cveId);
    if (!affectedVulns.length) return;
    const mainVuln = affectedVulns[0];
    
    // Lấy tên các component bị ảnh hưởng
    const affectedComponentNames = Array.from(new Set(affectedVulns.map(v => v.technology.name)));
    // Gom tất cả các project sử dụng component bị ảnh hưởng từ all_projects
    const componentGroups = {};
    affectedComponentNames.forEach(compName => {
        // Tìm một vulnerability có cùng tên component để lấy all_projects
        const vuln = affectedVulns.find(v => v.technology.name === compName);
        if (vuln && Array.isArray(vuln.all_projects)) {
            componentGroups[compName] = vuln.all_projects;
        } else {
            componentGroups[compName] = [];
        }
    });

    // Tab Information với improved styling
    const infoTab = `
        <div class="modal-section">
            <!-- Description Section với Icon -->
            <div class="info-section mb-4">
                <h4 class="mb-3 d-flex align-items-center">
                    <div class="info-icon-wrapper me-3">
                        <i class="fas fa-file-alt text-info"></i>
                    </div>
                    <span class="text-light">Description</span>
                </h4>
                <div class="info-content p-3 bg-dark bg-opacity-50 rounded border-start border-4 border-info">
                    ${mainVuln.cve.description}
                </div>
            </div>

            <!-- CVSS Information Grid với Icons và Màu sắc -->
            <div class="cvss-info-grid mb-4">
                <div class="cvss-info-card">
                    <div class="card-header-custom">
                        <i class="fas fa-tachometer-alt text-primary me-2"></i>
                        <span>CVSS v3 Metrics</span>
                    </div>
                    <div class="cvss-info-item">
                        <div class="cvss-icon score">
                            <i class="fas fa-gauge-high"></i>
                        </div>
                        <div class="cvss-info-content">
                            <h6>Base Score</h6>
                            <div class="value text-${getCVSSTextColor(mainVuln.cve.cvss_data.baseScore)}">${mainVuln.cve.cvss_data.baseScore}</div>
                        </div>
                    </div>
                    <div class="cvss-info-item">
                        <div class="cvss-icon severity ${getSeverityIconClass(mainVuln.cve.cvss_data.baseSeverity)}">
                            <i class="fas ${getSeverityIcon(mainVuln.cve.cvss_data.baseSeverity)}"></i>
                        </div>
                        <div class="cvss-info-content">
                            <h6>Severity</h6>
                            <div class="value">
                                <span class="badge bg-${getSeverityColor(mainVuln.cve.cvss_data.baseSeverity)} px-3 py-2">
                                    ${mainVuln.cve.cvss_data.baseSeverity}
                                </span>
                            </div>
                        </div>
                    </div>
                    <div class="cvss-info-item">
                        <div class="cvss-icon vector">
                            <i class="fas fa-code"></i>
                        </div>
                        <div class="cvss-info-content">
                            <h6>Attack Vector</h6>
                            <div class="value text-info">${mainVuln.cve.cvss_data.vectorString || 'N/A'}</div>
                        </div>
                    </div>
                </div>

                <div class="cvss-info-card">
                    <div class="card-header-custom">
                        <i class="fas fa-chart-line text-warning me-2"></i>
                        <span>Risk Assessment</span>
                    </div>
                    <div class="cvss-info-item">
                        <div class="cvss-icon assessment ${getRiskIconClass(mainVuln.analysis.risk_assessment)}">
                            <i class="fas ${getRiskIcon(mainVuln.analysis.risk_assessment)}"></i>
                        </div>
                        <div class="cvss-info-content">
                            <h6>Risk Level</h6>
                            <div class="value">
                                <span class="badge bg-${getRiskColor(mainVuln.analysis.risk_assessment.toLowerCase())} px-3 py-2">
                                    ${mainVuln.analysis.risk_assessment}
                                </span>
                            </div>
                        </div>
                    </div>
                    <div class="cvss-info-item">
                        <div class="cvss-icon confidence">
                            <i class="fas fa-percentage"></i>
                        </div>
                        <div class="cvss-info-content">
                            <h6>Confidence</h6>
                            <div class="value">
                                <div class="progress" style="height: 25px;">
                                    <div class="progress-bar bg-success" role="progressbar" 
                                         style="width: ${(mainVuln.analysis.confidence_score * 100).toFixed(0)}%"
                                         aria-valuenow="${(mainVuln.analysis.confidence_score * 100).toFixed(0)}" 
                                         aria-valuemin="0" aria-valuemax="100">
                                        <strong>${(mainVuln.analysis.confidence_score * 100).toFixed(0)}%</strong>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="cvss-info-item">
                        <div class="cvss-icon publish-date">
                            <i class="fas fa-calendar-alt"></i>
                        </div>
                        <div class="cvss-info-content">
                            <h6>Published</h6>
                            <div class="value text-secondary">
                                <i class="fas fa-clock me-1"></i>
                                ${new Date(mainVuln.cve.publish_date).toLocaleDateString('en-US', { 
                                    year: 'numeric', month: 'long', day: 'numeric' 
                                })}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- References Section với styling đẹp -->
            <div class="info-section">
                <h5 class="mt-4 mb-3 d-flex align-items-center">
                    <div class="info-icon-wrapper me-3">
                        <i class="fas fa-external-link-alt text-success"></i>
                    </div>
                    <span class="text-light">References & Resources</span>
                </h5>
                <div class="references-container">
                    ${mainVuln.cve.references.map((ref, index) => `
                        <div class="reference-item mb-2 p-3 bg-dark bg-opacity-25 rounded border-start border-3 border-success">
                            <div class="d-flex align-items-center">
                                <div class="reference-icon me-3">
                                    <i class="fas ${getReferenceIcon(ref)} text-success"></i>
                                </div>
                                <div class="flex-grow-1">
                                    <a href="${ref}" target="_blank" class="text-success text-decoration-none hover-underline">
                                        <strong>${getReferenceName(ref)}</strong>
                                    </a>
                                    <div class="text-muted small mt-1">${ref}</div>
                                </div>
                                <div class="reference-actions">
                                    <a href="${ref}" target="_blank" class="btn btn-sm btn-outline-success">
                                        <i class="fas fa-external-link-alt me-1"></i>
                                        View
                                    </a>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;

    // Tab Affected Components
    const affectedTab = `
        <div class="modal-section">
            <h4 class="mb-3">Affected Components</h4>
            ${affectedComponentNames.map(compName => {
                const projectsUsingComponent = componentGroups[compName] || [];
                return `
                <div class="mb-4">
                    <div class="fw-bold text-accent mb-3 d-flex align-items-center">
                        <i class="fas fa-cube text-primary me-2"></i>
                        <span class="fs-5">${compName}</span>
                    </div>
                    ${projectsUsingComponent.length > 0 ? `
                        <div class="table-responsive">
                            <table class="table table-dark table-striped table-hover">
                                <thead>
                                    <tr class="table-primary">
                                        <th scope="col" class="text-center" style="width: 5%;">
                                            <i class="fas fa-hashtag"></i>
                                        </th>
                                        <th scope="col" style="width: 30%;">
                                            <i class="fas fa-project-diagram me-2"></i>Project
                                        </th>
                                        <th scope="col" style="width: 25%;">
                                            <i class="fas fa-cube me-2"></i>Component
                                        </th>
                                        <th scope="col" class="text-center" style="width: 15%;">
                                            <i class="fas fa-tag me-2"></i>Version
                                        </th>
                                        <th scope="col" style="width: 25%;">
                                            <i class="fas fa-user-tie me-2"></i>Manager
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${projectsUsingComponent.map((proj, index) => {
                                        const versionText = proj.version ? `v${proj.version}` : 'No version';
                                        const versionClass = proj.version ? 'badge bg-info' : 'badge bg-secondary';
                                        return `
                                        <tr>
                                            <td class="text-center">
                                                <span class="badge bg-primary">${index + 1}</span>
                                            </td>
                                            <td>
                                                <div class="d-flex align-items-center">
                                                    <div class="avatar-circle me-2 bg-primary bg-opacity-25" style="width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                                                        <i class="fas fa-folder text-primary"></i>
                                                    </div>
                                                    <span class="fw-semibold text-light">${proj.project_name}</span>
                                                </div>
                                            </td>
                                            <td>
                                                <span class="text-info fw-medium">${proj.component_name}</span>
                                            </td>
                                            <td class="text-center">
                                                <span class="${versionClass}">${versionText}</span>
                                            </td>
                                            <td>
                                                <div class="d-flex align-items-center">
                                                    <div class="avatar-circle me-2 bg-warning bg-opacity-25" style="width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                                                        <i class="fas fa-user text-warning"></i>
                                                    </div>
                                                    <span class="text-warning fw-medium">${proj.manager_name || 'Unknown Manager'}</span>
                                                </div>
                                            </td>
                                        </tr>
                                        `;
                                    }).join('')}
                                </tbody>
                            </table>
                        </div>
                    ` : `
                        <div class="alert alert-info d-flex align-items-center">
                            <i class="fas fa-info-circle me-2"></i>
                            <span>No project information available for this component</span>
                        </div>
                    `}
                </div>
                `;
            }).join('')}
        </div>
    `;

    // Tab Plugins
    const pluginsTab = `
        <div class="modal-section">
            <h4 class="mb-3">Plugins & Tools</h4>
            <div class="alert alert-secondary d-flex align-items-center">
                <i class="fas fa-plug me-2"></i>
                <span>No plugins available for this CVE at this time.</span>
            </div>
        </div>
    `;

    // Render CUSTOM MODAL TABS thay vì Bootstrap tabs
    const modalBody = document.getElementById('cveDetailsBody');
    modalBody.innerHTML = `
        <!-- Custom Modal Tabs -->
        <div class="modal-tabs">
            <button class="modal-tab active" data-tab="info">
                <i class="fas fa-info-circle"></i>
                Information
            </button>
            <button class="modal-tab" data-tab="affected">
                <i class="fas fa-puzzle-piece"></i>
                Affected Components
            </button>
            <button class="modal-tab" data-tab="plugins">
                <i class="fas fa-plug"></i>
                Plugins
            </button>
        </div>

        <!-- Tab Content -->
        <div class="modal-tab-content" data-content="info">
            ${infoTab}
        </div>
        <div class="modal-tab-content d-none" data-content="affected">
            ${affectedTab}
        </div>
        <div class="modal-tab-content d-none" data-content="plugins">
            ${pluginsTab}
        </div>
    `;

    // Add click handlers cho custom tabs
    const tabs = modalBody.querySelectorAll('.modal-tab');
    const contents = modalBody.querySelectorAll('.modal-tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remove active class from all tabs
            tabs.forEach(t => t.classList.remove('active'));
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Hide all content
            contents.forEach(c => c.classList.add('d-none'));
            // Show target content
            const targetContent = modalBody.querySelector(`[data-content="${targetTab}"]`);
            if (targetContent) {
                targetContent.classList.remove('d-none');
            }
        });
    });

    // Update modal title
    const modal = document.getElementById('cveDetailsModal');
    const modalTitle = modal.querySelector('.modal-title');
    modalTitle.innerHTML = `
        <i class="fas fa-shield-alt me-2 pulse-icon"></i>
        ${mainVuln.cve?.cve_id || 'N/A'} - ${mainVuln.analysis?.risk_assessment || 'Unknown'} Risk
    `;

    // Update footer information
    const footerCveId = modal.querySelector('#modalFooterCveId');
    const footerAffectedCount = modal.querySelector('#modalFooterAffectedCount');
    
    if (footerCveId) {
        footerCveId.textContent = mainVuln.cve?.cve_id || 'N/A';
    }
    
    if (footerAffectedCount) {
        footerAffectedCount.textContent = `${mainVuln.technology?.name || 'Unknown'} affected`;
    }

    // Show the modal
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
    
    showNotification(`Displaying details for ${mainVuln.cve?.cve_id || 'N/A'}`, 'info');
}
window.showCVEDetails = showCVEDetails;

function getRiskColor(risk) {
    const colors = { 
        'critical': 'danger',     // Đỏ đậm
        'high': 'danger',         // Đỏ  
        'medium': 'warning',      // Vàng
        'low': 'success'          // Xanh
    };
    return colors[risk] || 'success';
}
function getCVSSColor(score) {
    if (score >= 9.0) return 'danger';
    if (score >= 7.0) return 'warning';
    if (score >= 4.0) return 'info';
    return 'secondary';
}

// Load system statistics
function loadSystemStats() {
    // Simulate loading statistics
    setTimeout(() => {
        document.getElementById('totalTechnologies').textContent = '247';
        document.getElementById('totalProjects').textContent = '89';
    }, 1500);
}

// Initialize animations
function initializeAnimations() {
    // Register GSAP ScrollTrigger
    gsap.registerPlugin(ScrollTrigger);
    
    // Animate model cards on load
    gsap.fromTo('.model-card', 
        { opacity: 0, y: 50, scale: 0.9 },
        { 
            opacity: 1, 
            y: 0, 
            scale: 1, 
            duration: 0.8, 
            stagger: 0.2,
            ease: "back.out(1.7)",
            delay: 0.3
        }
    );
    
    // Animate stats cards
    gsap.fromTo('.stat-card', 
        { opacity: 0, x: -30 },
        { 
            opacity: 1, 
            x: 0, 
            duration: 0.6, 
            stagger: 0.1,
            delay: 0.5
        }
    );
}

// Filter vulnerabilities
function filterVulnerabilities() {
    const filter = document.getElementById('vulnerabilityFilter').value.toLowerCase();
    const rows = document.querySelectorAll('#vulnerabilitiesTableBody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(filter) ? '' : 'none';
    });
}

// Export results functionality
function exportResults() {
    showNotification('Exporting scan results...', 'info');
    
    // Simulate export process
    setTimeout(() => {
        showNotification('Results exported successfully!', 'success');
    }, 2000);
}

// Toggle fullscreen modal
function toggleFullscreen() {
    const modal = document.getElementById('cveDetailsModal');
    const toggleBtn = modal.querySelector('.fa-expand, .fa-compress');
    
    if (modal.classList.contains('fullscreen')) {
        modal.classList.remove('fullscreen');
        toggleBtn.className = 'fas fa-expand';
    } else {
        modal.classList.add('fullscreen');
        toggleBtn.className = 'fas fa-compress';
    }
}

// Mark CVE as reviewed
function markAsReviewed() {
    showNotification('CVE marked as reviewed', 'success');
    
    // Close modal after marking as reviewed
    setTimeout(() => {
        const modal = bootstrap.Modal.getInstance(document.getElementById('cveDetailsModal'));
        if (modal) {
            modal.hide();
        }
    }, 1000);
}

// Enhanced notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    
    const iconMap = {
        info: 'info-circle',
        success: 'check-circle',
        warning: 'exclamation-triangle',
        error: 'times-circle'
    };
    
    notification.innerHTML = `
        <i class="fas fa-${iconMap[type]}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    gsap.fromTo(notification, 
        { x: 350, opacity: 0 },
        { x: 0, opacity: 1, duration: 0.4, ease: "back.out(1.7)" }
    );
    
    // Remove after delay
    setTimeout(() => {
        gsap.to(notification, {
            x: 350,
            opacity: 0,
            duration: 0.3,
            onComplete: () => notification.remove()
        });
    }, 4000);
}

// Helper functions for enhanced CVE modal styling

// Get CVSS score text color
function getCVSSTextColor(score) {
    if (score >= 9.0) return 'danger';
    if (score >= 7.0) return 'warning';
    if (score >= 4.0) return 'info';
    return 'success';
}

// Get severity icon
function getSeverityIcon(severity) {
    const icons = {
        'CRITICAL': 'fa-skull-crossbones',
        'HIGH': 'fa-exclamation-triangle',
        'MEDIUM': 'fa-exclamation-circle',
        'LOW': 'fa-info-circle',
        'UNKNOWN': 'fa-question-circle'
    };
    return icons[severity?.toUpperCase()] || 'fa-question-circle';
}

// Get severity icon class for background color
function getSeverityIconClass(severity) {
    const classes = {
        'CRITICAL': 'severity-critical',
        'HIGH': 'severity-high', 
        'MEDIUM': 'severity-medium',
        'LOW': 'severity-low',
        'UNKNOWN': 'severity-unknown'
    };
    return classes[severity?.toUpperCase()] || 'severity-unknown';
}

// Get severity color for badges - Updated to match requirements
function getSeverityColor(severity) {
    const colors = {
        'CRITICAL': 'danger',      // Đỏ đậm  
        'HIGH': 'danger',          // Đỏ (sẽ dùng CSS để phân biệt với critical)
        'MEDIUM': 'warning',       // Vàng
        'LOW': 'success',          // Xanh
        'UNKNOWN': 'success'       // Xanh (như low)
    };
    return colors[severity?.toUpperCase()] || 'success';
}

// Get risk icon
function getRiskIcon(risk) {
    const icons = {
        'CRITICAL': 'fa-fire',
        'HIGH': 'fa-exclamation-triangle',
        'MEDIUM': 'fa-shield-virus',
        'LOW': 'fa-shield-check'
    };
    return icons[risk?.toUpperCase()] || 'fa-shield';
}

// Get risk icon class for background color
function getRiskIconClass(risk) {
    const classes = {
        'CRITICAL': 'risk-critical',
        'HIGH': 'risk-high',
        'MEDIUM': 'risk-medium', 
        'LOW': 'risk-low'
    };
    return classes[risk?.toUpperCase()] || 'risk-unknown';
}

// Get reference icon based on URL
function getReferenceIcon(url) {
    if (url.includes('github.com')) return 'fa-github';
    if (url.includes('nvd.nist.gov')) return 'fa-shield-alt';
    if (url.includes('cve.mitre.org')) return 'fa-database';
    if (url.includes('security')) return 'fa-lock';
    if (url.includes('advisory') || url.includes('advisories')) return 'fa-bullhorn';
    if (url.includes('commit')) return 'fa-code-branch';
    if (url.includes('issue') || url.includes('issues')) return 'fa-bug';
    if (url.includes('cwe.mitre.org')) return 'fa-list-alt';
    return 'fa-external-link-alt';
}

// Get reference name based on URL
function getReferenceName(url) {
    if (url.includes('github.com/')) {
        if (url.includes('/commit/')) return 'GitHub Commit';
        if (url.includes('/security/advisories/')) return 'GitHub Security Advisory';
        if (url.includes('/issues/')) return 'GitHub Issue';
        if (url.includes('/pull/')) return 'GitHub Pull Request';
        return 'GitHub Repository';
    }
    if (url.includes('nvd.nist.gov')) return 'NVD - National Vulnerability Database';
    if (url.includes('cve.mitre.org')) return 'CVE Details - MITRE';
    if (url.includes('cwe.mitre.org')) return 'CWE - Common Weakness Enumeration';
    if (url.includes('security.snyk.io')) return 'Snyk Security Advisory';
    if (url.includes('vuldb.com')) return 'VulDB Vulnerability Database';
    if (url.includes('exploit-db.com')) return 'Exploit Database';
    
    // Extract domain name as fallback
    try {
        const domain = new URL(url).hostname.replace('www.', '');
        return domain.charAt(0).toUpperCase() + domain.slice(1) + ' Reference';
    } catch (e) {
        return 'External Reference';
    }
}

// Populate real vulnerabilities table
function populateRealVulnerabilitiesTable(vulnerabilities) {
    console.log('DEBUG: populateRealVulnerabilitiesTable called with:', vulnerabilities?.length, 'vulnerabilities');
    
    const tbody = document.getElementById('vulnerabilitiesTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    if (!vulnerabilities || vulnerabilities.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td colspan="8" class="text-center py-4">
                <div class="text-muted">
                    <i class="fas fa-info-circle me-2"></i>
                    No vulnerabilities found for the selected date range
                </div>
            </td>
        `;
        tbody.appendChild(row);
        return;
    }
    
    // Group vulnerabilities by CVE ID first - same logic as populateVulnerabilitiesTable
    const cveGroups = {};
    vulnerabilities.forEach(vuln => {
        const cveId = vuln.cve?.cve_id;
        if (cveId) {
            if (!cveGroups[cveId]) {
                cveGroups[cveId] = [];
            }
            cveGroups[cveId].push(vuln);
        }
    });
    
    // Create unique vulnerabilities array (1 per CVE)
    const uniqueVulnerabilities = Object.values(cveGroups).map(group => {
        // Choose the vulnerability with highest risk level as representative
        const sortedGroup = group.sort((a, b) => {
            const riskA = getRiskPriority(a.analysis?.risk_assessment);
            const riskB = getRiskPriority(b.analysis?.risk_assessment);
            return riskB - riskA;
        });
        
        const mainVuln = sortedGroup[0];
        
        // Add affected technologies list to the main vulnerability
        mainVuln.affectedTechnologies = group.map(v => ({
            name: v.technology?.name,
            version: v.technology?.version,
            project_name: v.technology?.project_name,
            manager_name: v.technology?.manager_name
        }));
        
        return mainVuln;
    });
    
    console.log(`DEBUG: Original count: ${vulnerabilities.length}, Unique count after grouping: ${uniqueVulnerabilities.length}`);
    
    // Show notification about CVE grouping
    if (vulnerabilities.length > uniqueVulnerabilities.length) {
        const duplicateCount = vulnerabilities.length - uniqueVulnerabilities.length;
        showNotification(`Grouped ${duplicateCount} duplicate CVE${duplicateCount > 1 ? 's' : ''}. Showing ${uniqueVulnerabilities.length} unique CVEs.`, 'info');
    }
    
    // Sort by risk priority
    const riskOrder = { 'critical': 4, 'high': 3, 'medium': 2, 'low': 1, 'unknown': 0 };
    uniqueVulnerabilities.sort((a, b) => {
        const riskA = a.analysis?.risk_assessment?.toLowerCase() || 'unknown';
        const riskB = b.analysis?.risk_assessment?.toLowerCase() || 'unknown';
        return riskOrder[riskB] - riskOrder[riskA]; // Sắp xếp từ cao xuống thấp
    });
    
    uniqueVulnerabilities.forEach((vuln, index) => {
        const row = document.createElement('tr');
        const riskClass = vuln.analysis?.risk_assessment?.toLowerCase() || 'unknown';
        const riskBadge = `<span class="badge bg-${getRiskColor(riskClass)}">${vuln.analysis?.risk_assessment || 'Unknown'}</span>`;
        const confidenceScore = vuln.analysis?.confidence_score ? (vuln.analysis.confidence_score * 100).toFixed(0) : '0';
        const confidenceBadge = `<span class="badge bg-info">${confidenceScore}%</span>`;
        const publishDate = vuln.cve?.publish_date ? new Date(vuln.cve.publish_date).toLocaleDateString() : 'N/A';
        const cvssScore = vuln.cve?.cvss_data?.baseScore || 'N/A';
        
        // Show primary technology name + version, with count if multiple
        const primaryTech = vuln.technology;
        const techCount = vuln.affectedTechnologies ? vuln.affectedTechnologies.length : 1;
        const techDisplayName = techCount > 1 ? 
            `${primaryTech?.name || 'Unknown'} (+${techCount - 1} more)` : 
            (primaryTech?.name || 'Unknown');
        
        row.innerHTML = `
            <td><span class="badge bg-primary bg-opacity-10 text-primary border border-primary fw-semibold">${index + 1}</span></td>
            <td>${riskBadge}</td>
            <td><a href="#" onclick="showRealCVEDetails('${vuln.cve?.cve_id || 'N/A'}', ${index})" class="text-decoration-none"><strong>${vuln.cve?.cve_id || 'N/A'}</strong></a></td>
            <td>
                <div class="d-flex align-items-center">
                    <div class="avatar-circle me-2">
                        <i class="fas fa-microchip"></i>
                    </div>
                    <div>
                        <strong>${techDisplayName}</strong>
                        ${primaryTech?.version ? `<small class="text-muted d-block">v${primaryTech.version}</small>` : ''}
                        ${techCount > 1 ? `<small class="text-info d-block">${techCount} components affected</small>` : ''}
                    </div>
                </div>
            </td>
            <td><span class="badge bg-${getCVSSColor(cvssScore)}">${cvssScore}</span></td>
            <td>${confidenceBadge}</td>
            <td>
                <div class="text-info small">
                    <div><strong>${publishDate}</strong></div>
                </div>
            </td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" onclick="showRealCVEDetails('${vuln.cve?.cve_id || 'N/A'}', ${index})">
                        <i class="fas fa-eye"></i>
                    </button>
                </div>
            </td>
        `;
        
        tbody.appendChild(row);
    });
    
    // Update window.lastScanResults với unique vulnerabilities
    window.lastScanResults = { vulnerabilities: uniqueVulnerabilities };
    console.log('DEBUG: Updated window.lastScanResults with', uniqueVulnerabilities.length, 'unique vulnerabilities');
    
    // Summary statistics for debug
    const summary = uniqueVulnerabilities.reduce((acc, vuln) => {
        const risk = vuln.analysis?.risk_assessment?.toLowerCase() || 'unknown';
        acc[risk] = (acc[risk] || 0) + 1;
        return acc;
    }, {});
    console.log('DEBUG: Risk distribution after CVE grouping:', summary);
}

// Đảm bảo showRealCVEDetails có thể gọi từ HTML onclick
function showRealCVEDetails(cveId, index) {
    if (!currentScanResults) return;
    const affectedVulns = currentScanResults.vulnerabilities.filter(v => v.cve.cve_id === cveId);
    if (!affectedVulns.length) return;
    const mainVuln = affectedVulns[0];
    
    // Lấy tên các component bị ảnh hưởng
    const affectedComponentNames = Array.from(new Set(affectedVulns.map(v => v.technology.name)));
    // Gom tất cả các project sử dụng component bị ảnh hưởng từ all_projects
    const componentGroups = {};
    affectedComponentNames.forEach(compName => {
        // Tìm một vulnerability có cùng tên component để lấy all_projects
        const vuln = affectedVulns.find(v => v.technology.name === compName);
        if (vuln && Array.isArray(vuln.all_projects)) {
            componentGroups[compName] = vuln.all_projects;
        } else {
            componentGroups[compName] = [];
        }
    });

    // Tab Information với improved styling
    const infoTab = `
        <div class="modal-section">
            <!-- Description Section với Icon -->
            <div class="info-section mb-4">
                <h4 class="mb-3 d-flex align-items-center">
                    <div class="info-icon-wrapper me-3">
                        <i class="fas fa-file-alt text-info"></i>
                    </div>
                    <span class="text-light">Description</span>
                </h4>
                <div class="info-content p-3 bg-dark bg-opacity-50 rounded border-start border-4 border-info">
                    ${mainVuln.cve.description}
                </div>
            </div>

            <!-- CVSS Information Grid với Icons và Màu sắc -->
            <div class="cvss-info-grid mb-4">
                <div class="cvss-info-card">
                    <div class="card-header-custom">
                        <i class="fas fa-tachometer-alt text-primary me-2"></i>
                        <span>CVSS v3 Metrics</span>
                    </div>
                    <div class="cvss-info-item">
                        <div class="cvss-icon score">
                            <i class="fas fa-gauge-high"></i>
                        </div>
                        <div class="cvss-info-content">
                            <h6>Base Score</h6>
                            <div class="value text-${getCVSSTextColor(mainVuln.cve.cvss_data.baseScore)}">${mainVuln.cve.cvss_data.baseScore}</div>
                        </div>
                    </div>
                    <div class="cvss-info-item">
                        <div class="cvss-icon severity ${getSeverityIconClass(mainVuln.cve.cvss_data.baseSeverity)}">
                            <i class="fas ${getSeverityIcon(mainVuln.cve.cvss_data.baseSeverity)}"></i>
                        </div>
                        <div class="cvss-info-content">
                            <h6>Severity</h6>
                            <div class="value">
                                <span class="badge bg-${getSeverityColor(mainVuln.cve.cvss_data.baseSeverity)} px-3 py-2">
                                    ${mainVuln.cve.cvss_data.baseSeverity}
                                </span>
                            </div>
                        </div>
                    </div>
                    <div class="cvss-info-item">
                        <div class="cvss-icon vector">
                            <i class="fas fa-code"></i>
                        </div>
                        <div class="cvss-info-content">
                            <h6>Attack Vector</h6>
                            <div class="value text-info">${mainVuln.cve.cvss_data.vectorString || 'N/A'}</div>
                        </div>
                    </div>
                </div>

                <div class="cvss-info-card">
                    <div class="card-header-custom">
                        <i class="fas fa-chart-line text-warning me-2"></i>
                        <span>Risk Assessment</span>
                    </div>
                    <div class="cvss-info-item">
                        <div class="cvss-icon assessment ${getRiskIconClass(mainVuln.analysis.risk_assessment)}">
                            <i class="fas ${getRiskIcon(mainVuln.analysis.risk_assessment)}"></i>
                        </div>
                        <div class="cvss-info-content">
                            <h6>Risk Level</h6>
                            <div class="value">
                                <span class="badge bg-${getRiskColor(mainVuln.analysis.risk_assessment.toLowerCase())} px-3 py-2">
                                    ${mainVuln.analysis.risk_assessment}
                                </span>
                            </div>
                        </div>
                    </div>
                    <div class="cvss-info-item">
                        <div class="cvss-icon confidence">
                            <i class="fas fa-percentage"></i>
                        </div>
                        <div class="cvss-info-content">
                            <h6>Confidence</h6>
                            <div class="value">
                                <div class="progress" style="height: 25px;">
                                    <div class="progress-bar bg-success" role="progressbar" 
                                         style="width: ${(mainVuln.analysis.confidence_score * 100).toFixed(0)}%"
                                         aria-valuenow="${(mainVuln.analysis.confidence_score * 100).toFixed(0)}" 
                                         aria-valuemin="0" aria-valuemax="100">
                                        <strong>${(mainVuln.analysis.confidence_score * 100).toFixed(0)}%</strong>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="cvss-info-item">
                        <div class="cvss-icon publish-date">
                            <i class="fas fa-calendar-alt"></i>
                        </div>
                        <div class="cvss-info-content">
                            <h6>Published</h6>
                            <div class="value text-secondary">
                                <i class="fas fa-clock me-1"></i>
                                ${new Date(mainVuln.cve.publish_date).toLocaleDateString('en-US', { 
                                    year: 'numeric', month: 'long', day: 'numeric' 
                                })}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- References Section với styling đẹp -->
            <div class="info-section">
                <h5 class="mt-4 mb-3 d-flex align-items-center">
                    <div class="info-icon-wrapper me-3">
                        <i class="fas fa-external-link-alt text-success"></i>
                    </div>
                    <span class="text-light">References & Resources</span>
                </h5>
                <div class="references-container">
                    ${mainVuln.cve.references.map((ref, index) => `
                        <div class="reference-item mb-2 p-3 bg-dark bg-opacity-25 rounded border-start border-3 border-success">
                            <div class="d-flex align-items-center">
                                <div class="reference-icon me-3">
                                    <i class="fas ${getReferenceIcon(ref)} text-success"></i>
                                </div>
                                <div class="flex-grow-1">
                                    <a href="${ref}" target="_blank" class="text-success text-decoration-none hover-underline">
                                        <strong>${getReferenceName(ref)}</strong>
                                    </a>
                                    <div class="text-muted small mt-1">${ref}</div>
                                </div>
                                <div class="reference-actions">
                                    <a href="${ref}" target="_blank" class="btn btn-sm btn-outline-success">
                                        <i class="fas fa-external-link-alt me-1"></i>
                                        View
                                    </a>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;

    // Tab Affected Components
    const affectedTab = `
        <div class="modal-section">
            <h4 class="mb-3">Affected Components</h4>
            ${affectedComponentNames.map(compName => {
                const projectsUsingComponent = componentGroups[compName] || [];
                return `
                <div class="mb-4">
                    <div class="fw-bold text-accent mb-3 d-flex align-items-center">
                        <i class="fas fa-cube text-primary me-2"></i>
                        <span class="fs-5">${compName}</span>
                    </div>
                    ${projectsUsingComponent.length > 0 ? `
                        <div class="table-responsive">
                            <table class="table table-dark table-striped table-hover">
                                <thead>
                                    <tr class="table-primary">
                                        <th scope="col" class="text-center" style="width: 5%;">
                                            <i class="fas fa-hashtag"></i>
                                        </th>
                                        <th scope="col" style="width: 30%;">
                                            <i class="fas fa-project-diagram me-2"></i>Project
                                        </th>
                                        <th scope="col" style="width: 25%;">
                                            <i class="fas fa-cube me-2"></i>Component
                                        </th>
                                        <th scope="col" class="text-center" style="width: 15%;">
                                            <i class="fas fa-tag me-2"></i>Version
                                        </th>
                                        <th scope="col" style="width: 25%;">
                                            <i class="fas fa-user-tie me-2"></i>Manager
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${projectsUsingComponent.map((proj, index) => {
                                        const versionText = proj.version ? `v${proj.version}` : 'No version';
                                        const versionClass = proj.version ? 'badge bg-info' : 'badge bg-secondary';
                                        return `
                                        <tr>
                                            <td class="text-center">
                                                <span class="badge bg-primary">${index + 1}</span>
                                            </td>
                                            <td>
                                                <div class="d-flex align-items-center">
                                                    <div class="avatar-circle me-2 bg-primary bg-opacity-25" style="width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                                                        <i class="fas fa-folder text-primary"></i>
                                                    </div>
                                                    <span class="fw-semibold text-light">${proj.project_name}</span>
                                                </div>
                                            </td>
                                            <td>
                                                <span class="text-info fw-medium">${proj.component_name}</span>
                                            </td>
                                            <td class="text-center">
                                                <span class="${versionClass}">${versionText}</span>
                                            </td>
                                            <td>
                                                <div class="d-flex align-items-center">
                                                    <div class="avatar-circle me-2 bg-warning bg-opacity-25" style="width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                                                        <i class="fas fa-user text-warning"></i>
                                                    </div>
                                                    <span class="text-warning fw-medium">${proj.manager_name || 'Unknown Manager'}</span>
                                                </div>
                                            </td>
                                        </tr>
                                        `;
                                    }).join('')}
                                </tbody>
                            </table>
                        </div>
                    ` : `
                        <div class="alert alert-info d-flex align-items-center">
                            <i class="fas fa-info-circle me-2"></i>
                            <span>No project information available for this component</span>
                        </div>
                    `}
                </div>
                `;
            }).join('')}
        </div>
    `;

    // Tab Plugins
    const pluginsTab = `
        <div class="modal-section">
            <h4 class="mb-3">Plugins & Tools</h4>
            <div class="alert alert-secondary d-flex align-items-center">
                <i class="fas fa-plug me-2"></i>
                <span>No plugins available for this CVE at this time.</span>
            </div>
        </div>
    `;

    // Render CUSTOM MODAL TABS thay vì Bootstrap tabs
    const modalBody = document.getElementById('cveDetailsBody');
    modalBody.innerHTML = `
        <!-- Custom Modal Tabs -->
        <div class="modal-tabs">
            <button class="modal-tab active" data-tab="info">
                <i class="fas fa-info-circle"></i>
                Information
            </button>
            <button class="modal-tab" data-tab="affected">
                <i class="fas fa-puzzle-piece"></i>
                Affected Components
            </button>
            <button class="modal-tab" data-tab="plugins">
                <i class="fas fa-plug"></i>
                Plugins
            </button>
        </div>

        <!-- Tab Content -->
        <div class="modal-tab-content" data-content="info">
            ${infoTab}
        </div>
        <div class="modal-tab-content d-none" data-content="affected">
            ${affectedTab}
        </div>
        <div class="modal-tab-content d-none" data-content="plugins">
            ${pluginsTab}
        </div>
    `;

    // Add click handlers cho custom tabs
    const tabs = modalBody.querySelectorAll('.modal-tab');
    const contents = modalBody.querySelectorAll('.modal-tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remove active class from all tabs
            tabs.forEach(t => t.classList.remove('active'));
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Hide all content
            contents.forEach(c => c.classList.add('d-none'));
            // Show target content
            const targetContent = modalBody.querySelector(`[data-content="${targetTab}"]`);
            if (targetContent) {
                targetContent.classList.remove('d-none');
            }
        });
    });

    // Update modal title
    const modal = document.getElementById('cveDetailsModal');
    const modalTitle = modal.querySelector('.modal-title');
    modalTitle.innerHTML = `
        <i class="fas fa-shield-alt me-2 pulse-icon"></i>
        ${mainVuln.cve?.cve_id || 'N/A'} - ${mainVuln.analysis?.risk_assessment || 'Unknown'} Risk
    `;

    // Update footer information
    const footerCveId = modal.querySelector('#modalFooterCveId');
    const footerAffectedCount = modal.querySelector('#modalFooterAffectedCount');
    
    if (footerCveId) {
        footerCveId.textContent = mainVuln.cve?.cve_id || 'N/A';
    }
    
    if (footerAffectedCount) {
        footerAffectedCount.textContent = `${mainVuln.technology?.name || 'Unknown'} affected`;
    }

    // Show the modal
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
    
    showNotification(`Displaying details for ${mainVuln.cve?.cve_id || 'N/A'}`, 'info');
}
window.showRealCVEDetails = showRealCVEDetails;