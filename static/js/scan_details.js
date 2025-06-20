// === SCAN DETAILS PAGE - COMPLETE CONFLICT RESOLUTION ===
console.log('🔧 SCAN DETAILS: Starting conflict resolution...');

// Store vulnerabilities data for modal access
let vulnerabilitiesData = [];
let groupedVulnerabilities = [];

// === MODAL UTILITIES (Integrated from modal-fix.js) ===
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

// 1. BACKUP BASE FUNCTIONS to prevent conflicts
window.baseShowNotification = window.showNotification || function() {};
window.baseInitializeTooltips = window.initializeTooltips || function() {};

// 2. OVERRIDE CONFLICTING FUNCTIONS with scan-details specific versions
window.showNotification = function(message, type = 'info') {
    console.log('📢 SCAN DETAILS Notification:', message, type);
    
    // Remove existing notifications
    document.querySelectorAll('.scan-notification').forEach(n => n.remove());
    
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed scan-notification`;
    notification.style.cssText = `
        top: 20px; right: 20px; z-index: 10001;
        min-width: 300px; max-width: 400px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 2px solid ${getNotificationBorderColor(type)};
        border-radius: 12px; backdrop-filter: blur(10px);
        background: ${getNotificationBgColor(type)};
    `;
    
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-${getNotificationIcon(type)} me-2" style="font-size: 18px;"></i>
            <span style="font-weight: 600;">${message}</span>
        </div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" style="filter: brightness(0) invert(1);"></button>
    `;
    
    document.body.appendChild(notification);
    setTimeout(() => notification.parentNode && notification.remove(), 4000);
};

// 3. DISABLE BASE TOOLTIP INITIALIZATION for modal elements
window.initializeTooltips = function() {
    console.log('🔧 SCAN DETAILS: Custom tooltip initialization...');
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        // Only init tooltips NOT in modal
        const tooltipElements = document.querySelectorAll('[data-bs-toggle="tooltip"]:not(#cveDetailsModal [data-bs-toggle="tooltip"])');
        tooltipElements.forEach(el => new bootstrap.Tooltip(el));
    }
};

// 4. PREVENT GSAP CONFLICTS by namespacing
const scanDetailsGSAP = window.gsap;
if (scanDetailsGSAP) {
    // Disable base GSAP animations for modal elements
    scanDetailsGSAP.set('#cveDetailsModal', { clearProps: 'all' });
    scanDetailsGSAP.set('#cveDetailsModal *', { clearProps: 'all' });
}

// 5. MODAL-SPECIFIC EVENT HANDLING
function setupModalEventHandling() {
    const modal = document.getElementById('cveDetailsModal');
    if (!modal) return;
    
    // Prevent event bubbling from modal
    modal.addEventListener('click', function(e) {
        e.stopPropagation();
    });
    
    // Disable base event handlers for modal
    modal.addEventListener('mouseenter', function(e) {
        e.stopImmediatePropagation();
    });
    
    // Override tooltip behavior for modal buttons
    const modalButtons = modal.querySelectorAll('[data-bs-toggle="tooltip"]');
    modalButtons.forEach(btn => {
        btn.removeAttribute('data-bs-toggle');
        btn.removeAttribute('title');
    });
}

// 6. ENHANCED MODAL FUNCTIONS with conflict prevention
function showCVEDetails(cveId, vulnIndex) {
    console.log('🔍 SCAN DETAILS showCVEDetails:', { cveId, vulnIndex });
    
    // PREVENT BASE CONFLICTS
    const modal = document.getElementById('cveDetailsModal');
    if (!modal) {
        console.error('❌ Modal not found');
        return;
    }
    
    if (typeof bootstrap === 'undefined') {
        console.error('❌ Bootstrap not loaded');
        return;
    }
    
    // USE GROUPED VULNERABILITIES instead of original data
    if (!window.groupedVulnerabilities || !window.groupedVulnerabilities[vulnIndex]) {
        console.error('❌ No grouped vulnerability data for index:', vulnIndex);
        console.log('Available grouped data:', window.groupedVulnerabilities);
        return;
    }
    
    const vuln = window.groupedVulnerabilities[vulnIndex];
    console.log('✅ Processing grouped vulnerability:', vuln);
    
    // DISABLE BASE ANIMATIONS temporarily
    if (window.gsap) {
        window.gsap.globalTimeline.pause();
    }
    
    try {
        // Update modal content
        updateModalContent(modal, vuln);
        
        // Reset to first tab
        switchModalTab(0);
        
        // Create and show modal with conflict prevention
        const bsModal = new bootstrap.Modal(modal, {
            backdrop: 'static',
            keyboard: true,
            focus: true
        });
        
        // Prevent base event interference
        modal.addEventListener('shown.bs.modal', function(e) {
            e.stopImmediatePropagation();
            console.log('✅ Modal shown successfully');
            if (window.gsap) window.gsap.globalTimeline.resume();
        });
        
        modal.addEventListener('hidden.bs.modal', function(e) {
            e.stopImmediatePropagation();
            if (window.gsap) window.gsap.globalTimeline.resume();
        });
        
        bsModal.show();
        
        showNotification(`Displaying details for ${vuln.cve?.cve_id || 'N/A'}`, 'info');
        
    } catch (error) {
        console.error('❌ Modal show error:', error);
        if (window.gsap) window.gsap.globalTimeline.resume();
        showNotification('Failed to open modal: ' + error.message, 'error');
    }
}

function updateModalContent(modal, vuln) {
    // Update title
    const modalTitle = modal.querySelector('.modal-title');
    modalTitle.innerHTML = `
        <i class="fas fa-shield-alt me-2"></i>
        ${vuln.cve?.cve_id || 'N/A'} - ${vuln.analysis?.risk_assessment || 'Unknown'} Risk
    `;
    
    // Update content elements
    const updates = {
        'cveDescription': vuln.cve?.description || 'No description available',
        'cvssBaseScore': vuln.cve?.cvss_data?.baseScore || 'N/A',
        'cvssSeverity': vuln.cve?.cvss_data?.baseSeverity || 'Unknown',
        'cvssVector': vuln.cve?.cvss_data?.vectorString || 'N/A',
        'riskAssessment': vuln.analysis?.risk_assessment || 'Unknown',
        'confidenceScore': vuln.analysis?.confidence_score ? 
            `${(vuln.analysis.confidence_score * 100).toFixed(0)}%` : '0%'
    };
    
    Object.entries(updates).forEach(([id, value]) => {
        const el = document.getElementById(id);
        if (el) el.textContent = value;
    });
    
    // Update references
    const referencesContainer = document.getElementById('cveReferences');
    if (referencesContainer) {
        if (vuln.cve?.references && vuln.cve.references.length > 0) {
            const referencesList = vuln.cve.references.map(ref => 
                `<li><a href="${ref}" target="_blank" style="color: #10b981;">${ref}</a></li>`
            ).join('');
            referencesContainer.innerHTML = `<ul>${referencesList}</ul>`;
        } else {
            referencesContainer.innerHTML = '<p class="text-muted">No references available</p>';
        }
    }
    
    // Update affected projects tab
    updateAffectedProjectsTab(vuln);
    
    // Update plugins tab
    updatePluginsTab(vuln);
    
    // Update footer
    updateModalFooter(vuln);
}

function updateAffectedProjectsTab(vuln) {
    const container = document.getElementById('affectedProjects');
    if (!container) return;
    
    // Get all affected technologies from this CVE
    const affectedTechnologies = vuln.affectedTechnologies || [vuln.technology];
    
    console.log('Affected technologies for CVE:', vuln.cve?.cve_id, affectedTechnologies);
    
    // Group by component name to show unique components
    const componentGroups = {};
    affectedTechnologies.forEach(tech => {
        const componentName = tech?.name || 'Unknown';
        if (!componentGroups[componentName]) {
            componentGroups[componentName] = [];
        }
        componentGroups[componentName].push(tech);
    });
    
    // Create table HTML
    let tableHTML = `
        <div class="affected-components-header mb-3">
            <div class="d-flex align-items-center">
                <div class="component-icon me-3" style="width: 40px; height: 40px; border-radius: 50%; background: rgba(16, 185, 129, 0.1); display: flex; align-items: center; justify-content: center; color: #10b981;">
                    <i class="fas fa-cubes"></i>
                </div>
                <div>
                    <h6 class="mb-1" style="color: #10b981; font-weight: 700;">${new Set(affectedTechnologies.map(t => t?.project_name || 'Unknown')).size} Project${new Set(affectedTechnologies.map(t => t?.project_name || 'Unknown')).size > 1 ? 's' : ''} Affected</h6>
                    <small style="color: #ffffff;">Components using ${vuln.cve?.cve_id}</small>
                </div>
            </div>
        </div>
        
        <div class="affected-components-table" style="background: #1f2937; border: 1px solid #374151; border-radius: 12px; overflow: hidden;">
            <table class="table table-dark table-hover mb-0" style="background: transparent;">
                <thead style="background: rgba(16, 185, 129, 0.1); border-bottom: 2px solid rgba(16, 185, 129, 0.3);">
                    <tr>
                        <th style="color: #10b981; font-weight: 700; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; padding: 12px;">#</th>
                        <th style="color: #10b981; font-weight: 700; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; padding: 12px;">
                            <i class="fas fa-project-diagram me-2"></i>Project
                        </th>
                        <th style="color: #10b981; font-weight: 700; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; padding: 12px;">
                            <i class="fas fa-puzzle-piece me-2"></i>Component
                        </th>
                        <th style="color: #10b981; font-weight: 700; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; padding: 12px;">
                            <i class="fas fa-tag me-2"></i>Version
                        </th>
                        <th style="color: #10b981; font-weight: 700; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; padding: 12px;">
                            <i class="fas fa-user me-2"></i>Manager
                        </th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    let rowIndex = 1;
    Object.entries(componentGroups).forEach(([componentName, techs]) => {
        // Group by project to avoid duplicate projects for same component
        const projectGroups = {};
        techs.forEach(tech => {
            const projectKey = `${tech?.project_name || 'Unknown Project'}-${tech?.manager_name || 'N/A'}`;
            if (!projectGroups[projectKey]) {
                projectGroups[projectKey] = tech;
            }
        });
        
        Object.values(projectGroups).forEach(tech => {
            const versionText = tech?.version ? tech.version : 'No version';
            const versionBadge = tech?.version ? 
                `<span class="badge bg-info" style="font-size: 11px;">${tech.version}</span>` : 
                `<span class="badge bg-secondary" style="font-size: 11px;">No version</span>`;
            
            tableHTML += `
                <tr style="border-bottom: 1px solid #374151;">
                    <td style="padding: 12px; color: #ffffff;">
                        <span class="badge bg-primary" style="font-size: 11px; font-weight: 600; background: linear-gradient(135deg, #10b981, #059669) !important; color: white !important;">
                            ${rowIndex}
                        </span>
                    </td>
                    <td style="padding: 12px;">
                        <div class="d-flex align-items-center">
                            <div class="project-icon me-2" style="width: 30px; height: 30px; border-radius: 50%; background: rgba(59, 130, 246, 0.1); display: flex; align-items: center; justify-content: center;">
                                <i class="fas fa-folder" style="color: #3b82f6; font-size: 12px;"></i>
                            </div>
                            <div>
                                <div style="color: #ffffff; font-weight: 600; font-size: 14px;">${tech?.project_name || 'Unknown Project'}</div>
                            </div>
                        </div>
                    </td>
                    <td style="padding: 12px;">
                        <div class="d-flex align-items-center">
                            <div class="component-icon me-2" style="width: 30px; height: 30px; border-radius: 6px; background: rgba(16, 185, 129, 0.1); display: flex; align-items: center; justify-content: center;">
                                <i class="fas fa-cube" style="color: #10b981; font-size: 12px;"></i>
                            </div>
                            <div>
                                <div style="color: #10b981; font-weight: 600; font-size: 14px;">${componentName}</div>
                            </div>
                        </div>
                    </td>
                    <td style="padding: 12px;">
                        ${versionBadge}
                    </td>
                    <td style="padding: 12px;">
                        <div class="d-flex align-items-center">
                            <div class="manager-icon me-2" style="width: 30px; height: 30px; border-radius: 50%; background: rgba(245, 158, 11, 0.1); display: flex; align-items: center; justify-content: center;">
                                <i class="fas fa-user" style="color: #f59e0b; font-size: 12px;"></i>
                            </div>
                            <div>
                                <div style="color: #f59e0b; font-weight: 600; font-size: 14px;">${tech?.manager_name || 'N/A'}</div>
                            </div>
                        </div>
                    </td>
                </tr>
            `;
            rowIndex++;
        });
    });
    
    tableHTML += `
                </tbody>
            </table>
        </div>
        
        <div class="affected-summary mt-3" style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 15px;">
            <div class="row">
                <div class="col-md-4">
                    <div class="text-center">
                        <div style="color: #10b981; font-size: 18px; font-weight: 700;">${Object.keys(componentGroups).length}</div>
                        <div style="color: #9ca3af; font-size: 12px; text-transform: uppercase;">Components</div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="text-center">
                        <div style="color: #3b82f6; font-size: 18px; font-weight: 700;">${affectedTechnologies.length}</div>
                        <div style="color: #9ca3af; font-size: 12px; text-transform: uppercase;">Instances</div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="text-center">
                        <div style="color: #f59e0b; font-size: 18px; font-weight: 700;">${new Set(affectedTechnologies.map(t => t?.project_name || 'Unknown')).size}</div>
                        <div style="color: #9ca3af; font-size: 12px; text-transform: uppercase;">Projects</div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = tableHTML;
}

function updatePluginsTab(vuln) {
    const container = document.getElementById('detectionPlugins');
    if (!container) return;
    
    const cveId = vuln.cve?.cve_id || 'N/A';
    const cveDescription = vuln.cve?.description || '';
    
    container.innerHTML = `
        <div class="plugins-container">
            <!-- Detection Engine Plugin -->
            <div class="plugin-card mb-4" style="background: #1f2937; border: 1px solid #374151; border-radius: 12px; padding: 20px;">
                <div class="d-flex align-items-center mb-3">
                    <div class="plugin-icon me-3" style="width: 40px; height: 40px; border-radius: 50%; background: rgba(16, 185, 129, 0.1); display: flex; align-items: center; justify-content: center; color: #10b981;">
                        <i class="fas fa-cogs"></i>
                    </div>
                    <div>
                        <h6 class="mb-1" style="color: #ffffff;">CVE Prime Analysis Engine</h6>
                        <small class="text-muted">Advanced vulnerability detection</small>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <span class="modal-label">Confidence</span>
                        <div class="modal-section-content">
                            <span class="badge bg-info">${vuln.analysis?.confidence_score ? 
                                `${(vuln.analysis.confidence_score * 100).toFixed(0)}%` : '0%'}</span>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <span class="modal-label">Match Type</span>
                        <div class="modal-section-content">${vuln.analysis?.match_type || 'Pattern Match'}</div>
                    </div>
                </div>
            </div>

            <!-- Grok AI Analysis Plugin -->
            <div class="plugin-card grok-ai-plugin" style="background: #1f2937; border: 1px solid #374151; border-radius: 12px; padding: 20px;">
                <div class="d-flex align-items-center justify-content-between mb-3">
                    <div class="d-flex align-items-center">
                        <div class="plugin-icon me-3" style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #8b5cf6, #7c3aed); display: flex; align-items: center; justify-content: center; color: white;">
                            <i class="fas fa-brain"></i>
                        </div>
                        <div>
                            <h6 class="mb-1" style="color: #ffffff;">Grok AI Analysis</h6>
                            <small class="text-muted">AI-powered vulnerability analysis</small>
                        </div>
                    </div>
                    <button class="btn btn-sm btn-outline-primary grok-analyze-btn" onclick="analyzeWithGrok('${cveId}', '${encodeURIComponent(cveDescription)}')">
                        <i class="fas fa-magic me-1"></i>
                        Analyze
                    </button>
                </div>
                
                <!-- Loading indicator -->
                <div id="grokLoading-${cveId.replace(/[^a-zA-Z0-9]/g, '')}" class="d-none text-center py-3">
                    <div class="spinner-border spinner-border-sm text-primary me-2" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <span class="text-muted">Analyzing with Grok AI...</span>
                </div>
                
                <!-- AI Analysis Results -->
                <div id="grokAnalysis-${cveId.replace(/[^a-zA-Z0-9]/g, '')}" class="grok-analysis-container" style="display: none;">
                    <div class="grok-analysis-content">
                        <!-- AI analysis will be populated here -->
                    </div>
                    <div class="mt-2 text-end">
                        <small class="text-muted">
                            <i class="fas fa-brain me-1"></i>
                            Analysis powered by Grok AI
                        </small>
                    </div>
                </div>
                
                <!-- Default message -->
                <div id="grokDefault-${cveId.replace(/[^a-zA-Z0-9]/g, '')}" class="text-center py-3">
                    <i class="fas fa-robot text-muted mb-2" style="font-size: 24px;"></i>
                    <p class="text-muted mb-0">Click "Analyze" to get AI-powered insights about this vulnerability</p>
                </div>
            </div>
        </div>
    `;
}

// Add Grok AI analysis function
function analyzeWithGrok(cveId, description) {
    console.log('🤖 Starting Grok AI analysis for:', cveId);
    
    const cleanCveId = cveId.replace(/[^a-zA-Z0-9]/g, '');
    const loadingEl = document.getElementById(`grokLoading-${cleanCveId}`);
    const analysisEl = document.getElementById(`grokAnalysis-${cleanCveId}`);
    const defaultEl = document.getElementById(`grokDefault-${cleanCveId}`);
    const analyzeBtn = event.target.closest('button');
    
    // PREVENT MODAL SHRINKING - Store original modal state
    const modal = document.getElementById('cveDetailsModal');
    const modalDialog = modal?.querySelector('.modal-dialog');
    const modalContent = modal?.querySelector('.modal-content');
    const modalBody = modal?.querySelector('.modal-body');
    
    // Force maintain modal size during and after analysis
    if (modalDialog) {
        modalDialog.style.cssText += 'max-width: 95vw !important; width: 95vw !important; height: calc(100vh - 2rem) !important;';
    }
    if (modalContent) {
        modalContent.style.cssText += 'height: 100% !important; display: flex !important; flex-direction: column !important;';
    }
    if (modalBody) {
        modalBody.style.cssText += 'flex: 1 !important; overflow-y: auto !important;';
    }
    
    // Show loading state
    if (loadingEl) loadingEl.classList.remove('d-none');
    if (defaultEl) defaultEl.style.display = 'none';
    if (analysisEl) analysisEl.style.display = 'none';
    if (analyzeBtn) {
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Analyzing...';
    }
    
    // Make POST API call to Grok with extended timeout
    const apiUrl = `/api/grok-cve-analysis/${encodeURIComponent(cveId)}`;
    
    // Create AbortController for manual timeout control
    const controller = new AbortController();
    const timeoutId = setTimeout(() => {
        controller.abort();
    }, 120000); // 2 minutes timeout
    
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            description: description
        }),
        signal: controller.signal
    })
        .then(response => {
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            return response.json();
        })
        .then(data => {
            console.log('🤖 Grok AI response:', data);
            
            // Hide loading
            if (loadingEl) loadingEl.classList.add('d-none');
            
            // FORCE MAINTAIN MODAL SIZE AFTER CONTENT UPDATE
            setTimeout(() => {
                if (modalDialog) {
                    modalDialog.style.cssText += 'max-width: 95vw !important; width: 95vw !important; height: calc(100vh - 2rem) !important;';
                }
                if (modalContent) {
                    modalContent.style.cssText += 'height: 100% !important; display: flex !important; flex-direction: column !important;';
                }
                if (modalBody) {
                    modalBody.style.cssText += 'flex: 1 !important; overflow-y: auto !important;';
                }
                
                // Force all containers to maintain width
                const pluginsContainer = document.querySelector('.plugins-container');
                const detectionPlugins = document.getElementById('detectionPlugins');
                const grokAnalysisContainer = document.querySelector('.grok-analysis-container');
                
                if (pluginsContainer) {
                    pluginsContainer.style.cssText += 'width: 100% !important; min-width: 100% !important;';
                }
                if (detectionPlugins) {
                    detectionPlugins.style.cssText += 'width: 100% !important; min-width: 100% !important;';
                }
                if (grokAnalysisContainer) {
                    grokAnalysisContainer.style.cssText += 'width: 100% !important; min-width: 100% !important;';
                }
            }, 100);
            
            if (data.success) {
                // Show analysis
                if (analysisEl) {
                    const contentEl = analysisEl.querySelector('.grok-analysis-content');
                    if (contentEl) {
                        contentEl.innerHTML = data.analysis;
                        // Force dark theme after content insertion
                        contentEl.style.cssText += 'background: #0f172a !important; color: #ffffff !important; width: 100% !important;';
                    }
                    analysisEl.style.display = 'block';
                    analysisEl.style.cssText += 'width: 100% !important; min-width: 100% !important;';
                }
                
                // Update button
                if (analyzeBtn) {
                    analyzeBtn.innerHTML = '<i class="fas fa-sync me-1"></i>Re-analyze';
                    analyzeBtn.disabled = false;
                }
                
                // Show success notification with source info
                const sourceMsg = data.source === 'cached' ? ' (from cache)' : '';
                showNotification(`AI analysis completed for ${cveId}${sourceMsg}`, 'success');
            } else {
                // Show error in analysis container
                if (analysisEl) {
                    const contentEl = analysisEl.querySelector('.grok-analysis-content');
                    if (contentEl) {
                        contentEl.innerHTML = `
                            <div class="alert alert-warning mb-0">
                                <i class="fas fa-exclamation-triangle me-2"></i>
                                <strong>Analysis Error:</strong><br>
                                ${data.analysis || 'Failed to analyze with Grok AI'}
                            </div>
                        `;
                        contentEl.style.cssText += 'background: #0f172a !important; color: #ffffff !important; width: 100% !important;';
                    }
                    analysisEl.style.display = 'block';
                    analysisEl.style.cssText += 'width: 100% !important; min-width: 100% !important;';
                }
                
                // Reset button
                if (analyzeBtn) {
                    analyzeBtn.innerHTML = '<i class="fas fa-magic me-1"></i>Analyze';
                    analyzeBtn.disabled = false;
                }
                
                showNotification(`Analysis failed: ${data.analysis || 'Unknown error'}`, 'error');
            }
            
            // FINAL FORCE MODAL SIZE MAINTENANCE
            setTimeout(() => {
                if (modalDialog) {
                    modalDialog.style.cssText += 'max-width: 95vw !important; width: 95vw !important; height: calc(100vh - 2rem) !important;';
                }
                if (modalContent) {
                    modalContent.style.cssText += 'height: 100% !important; display: flex !important; flex-direction: column !important;';
                }
                if (modalBody) {
                    modalBody.style.cssText += 'flex: 1 !important; overflow-y: auto !important;';
                }
            }, 500);
        })
        .catch(error => {
            clearTimeout(timeoutId);
            console.error('🤖 Grok AI error:', error);
            
            // Hide loading
            if (loadingEl) loadingEl.classList.add('d-none');
            
            // Determine error type and message
            let errorMessage = 'Unknown error occurred';
            let errorType = 'danger';
            
            if (error.name === 'AbortError') {
                errorMessage = 'Request timed out after 2 minutes. Grok AI may be overloaded.';
                errorType = 'warning';
            } else if (error.message.includes('Failed to fetch')) {
                errorMessage = 'Network connection failed. Please check your internet connection.';
                errorType = 'warning';
            } else if (error.message.includes('HTTP 429')) {
                errorMessage = 'Grok API rate limit exceeded. Please wait a few minutes before trying again.';
                errorType = 'warning';
            } else if (error.message.includes('HTTP 5')) {
                errorMessage = 'Grok API server error. Please try again later.';
                errorType = 'warning';
            } else {
                errorMessage = error.message || 'Connection error occurred';
            }
            
            // Show error in analysis container
            if (analysisEl) {
                const contentEl = analysisEl.querySelector('.grok-analysis-content');
                if (contentEl) {
                    contentEl.innerHTML = `
                        <div class="alert alert-${errorType} mb-0">
                            <i class="fas fa-exclamation-circle me-2"></i>
                            <strong>Connection Error:</strong><br>
                            ${errorMessage}
                            <br><br>
                            <small class="text-muted">
                                <i class="fas fa-info-circle me-1"></i>
                                If this persists, the Grok AI service may be temporarily unavailable.
                            </small>
                        </div>
                    `;
                    contentEl.style.cssText += 'background: #0f172a !important; color: #ffffff !important; width: 100% !important;';
                }
                analysisEl.style.display = 'block';
                analysisEl.style.cssText += 'width: 100% !important; min-width: 100% !important;';
            }
            
            // Reset button
            if (analyzeBtn) {
                analyzeBtn.innerHTML = '<i class="fas fa-magic me-1"></i>Analyze';
                analyzeBtn.disabled = false;
            }
            
            showNotification(errorMessage, 'error');
            
            // MAINTAIN MODAL SIZE EVEN ON ERROR
            setTimeout(() => {
                if (modalDialog) {
                    modalDialog.style.cssText += 'max-width: 95vw !important; width: 95vw !important; height: calc(100vh - 2rem) !important;';
                }
                if (modalContent) {
                    modalContent.style.cssText += 'height: 100% !important; display: flex !important; flex-direction: column !important;';
                }
                if (modalBody) {
                    modalBody.style.cssText += 'flex: 1 !important; overflow-y: auto !important;';
                }
            }, 500);
        });
}

function updateModalFooter(vuln) {
    const footerCveId = document.getElementById('modalFooterCveId');
    const footerAffectedCount = document.getElementById('modalFooterAffectedCount');
    
    if (footerCveId) footerCveId.textContent = vuln.cve?.cve_id || 'N/A';
    if (footerAffectedCount) footerAffectedCount.textContent = `${vuln.technology?.name || 'Unknown'} affected`;
}

function switchModalTab(tabIndex) {
    // Remove active from all tabs
    document.querySelectorAll('.modal-tab').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.modal-tab-content').forEach(content => content.classList.add('d-none'));
    
    // Add active to selected tab
    const tabs = document.querySelectorAll('.modal-tab');
    const contents = document.querySelectorAll('.modal-tab-content');
    
    if (tabs[tabIndex]) tabs[tabIndex].classList.add('active');
    if (contents[tabIndex]) contents[tabIndex].classList.remove('d-none');
}

function toggleFullscreen() {
    const modal = document.getElementById('cveDetailsModal');
    const dialog = modal.querySelector('.modal-dialog');
    const icon = event.target.closest('button').querySelector('i');
    
    if (dialog.classList.contains('modal-fullscreen')) {
        dialog.classList.remove('modal-fullscreen');
        dialog.classList.add('modal-xl');
        icon.classList.remove('fa-compress');
        icon.classList.add('fa-expand');
    } else {
        dialog.classList.remove('modal-xl');
        dialog.classList.add('modal-fullscreen');
        icon.classList.remove('fa-expand');
        icon.classList.add('fa-compress');
    }
}

function markAsReviewed() {
    showNotification('Vulnerability marked as reviewed', 'success');
}

// Export/Download functions
function exportResults() {
    const sessionId = document.querySelector('[data-session-id]')?.getAttribute('data-session-id');
    if (sessionId) {
        window.open(`/api/export-scan-results/${sessionId}`, '_blank');
        showNotification('Exporting scan results...', 'success');
    } else {
        showNotification('Session ID not found', 'error');
    }
}

function downloadScanReport(sessionId) {
    window.open(`/api/scan-report/${sessionId}`, '_blank');
    showNotification(`Downloading report for scan ${sessionId}`, 'success');
}

// Populate table with CVE grouping logic (scan-details specific)
function populateScanDetailsTable() {
    const tbody = document.getElementById('vulnerabilitiesTableBody');
    if (!tbody) {
        return;
    }
    
    tbody.innerHTML = '';
    
    if (!vulnerabilitiesData || vulnerabilitiesData.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td colspan="8" class="text-center py-4">
                <div class="text-muted">
                    <i class="fas fa-info-circle me-2"></i>
                    No vulnerabilities found in this scan session
                </div>
            </td>
        `;
        tbody.appendChild(row);
        return;
    }
    
    // Group vulnerabilities by CVE ID first
    const cveGroups = {};
    vulnerabilitiesData.forEach((vuln, index) => {
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
    
    // Sort by risk priority
    const riskOrder = { 'critical': 4, 'high': 3, 'medium': 2, 'low': 1, 'unknown': 0 };
    uniqueVulnerabilities.sort((a, b) => {
        const riskA = a.analysis?.risk_assessment?.toLowerCase() || 'unknown';
        const riskB = b.analysis?.risk_assessment?.toLowerCase() || 'unknown';
        return riskOrder[riskB] - riskOrder[riskA];
    });
    
    uniqueVulnerabilities.forEach((vuln, index) => {
        try {
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
                <td><a href="#" onclick="showCVEDetails('${vuln.cve?.cve_id || 'N/A'}', ${index})" class="text-decoration-none"><strong>${vuln.cve?.cve_id || 'N/A'}</strong></a></td>
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
                        <button class="btn btn-outline-primary" onclick="showCVEDetails('${vuln.cve?.cve_id || 'N/A'}', ${index})">
                            <i class="fas fa-eye"></i>
                        </button>
                    </div>
                </td>
            `;
            
            tbody.appendChild(row);
            
        } catch (error) {
            console.error(`Error creating row ${index + 1}:`, error);
        }
    });
    
    // Update global vulnerabilities data for modal access
    window.groupedVulnerabilities = uniqueVulnerabilities;
}

// Helper functions for risk and color calculations
function getRiskPriority(risk) {
    const map = { 'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1 };
    return map[risk?.toUpperCase()] || 0;
}

function getRiskColor(risk) {
    const colors = { 
        'critical': 'danger',
        'high': 'danger',
        'medium': 'warning',
        'low': 'success',
        'unknown': 'secondary'
    };
    return colors[risk] || 'secondary';
}

function getCVSSColor(score) {
    if (typeof score === 'string' && score === 'N/A') return 'secondary';
    const numScore = parseFloat(score);
    if (numScore >= 9.0) return 'danger';
    if (numScore >= 7.0) return 'warning';
    if (numScore >= 4.0) return 'info';
    return 'success';
}

// Helper functions for notifications
function getNotificationBorderColor(type) {
    const colors = {
        success: '#10b981', error: '#dc2626', danger: '#dc2626',
        warning: '#f59e0b', info: '#3b82f6'
    };
    return colors[type] || '#6b7280';
}

function getNotificationBgColor(type) {
    const colors = {
        success: 'rgba(16, 185, 129, 0.95)', error: 'rgba(220, 38, 38, 0.95)',
        danger: 'rgba(220, 38, 38, 0.95)', warning: 'rgba(245, 158, 11, 0.95)',
        info: 'rgba(59, 130, 246, 0.95)'
    };
    return colors[type] || 'rgba(107, 114, 128, 0.95)';
}

function getNotificationIcon(type) {
    const icons = {
        success: 'check-circle', error: 'exclamation-triangle',
        danger: 'exclamation-triangle', warning: 'exclamation-circle',
        info: 'info-circle'
    };
    return icons[type] || 'bell';
}

// Initialize scan details page
function initializeScanDetails(vulnData) {
    vulnerabilitiesData = vulnData || [];
    console.log('🚀 SCAN DETAILS: Initializing with', vulnerabilitiesData.length, 'vulnerabilities');
    
    // Populate table with grouped vulnerabilities
    populateScanDetailsTable();
    
    // Setup filter functionality
    const filterInput = document.getElementById('vulnerabilityFilter');
    if (filterInput) {
        filterInput.addEventListener('input', function() {
            const filterValue = this.value.toLowerCase();
            document.querySelectorAll('#vulnerabilitiesTableBody tr').forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filterValue) ? '' : 'none';
            });
        });
    }
    
    // Setup modal event handling
    setTimeout(() => {
        setupModalEventHandling();
        initializeTooltips();
        
        if (vulnerabilitiesData.length > 0) {
            console.log('✅ SCAN DETAILS: Modal ready with', vulnerabilitiesData.length, 'vulnerabilities');
            showNotification('Scan details loaded successfully', 'success');
        } else {
            console.log('⚠️ SCAN DETAILS: No vulnerability data available');
            showNotification('No vulnerability data available', 'warning');
        }
    }, 1000);
}

// 7. INITIALIZE CONFLICT-FREE ENVIRONMENT
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 SCAN DETAILS: Conflict-free initialization...');
    
    // Auto-initialize if vulnerabilities data is available globally
    if (typeof window.vulnerabilitiesData !== 'undefined') {
        initializeScanDetails(window.vulnerabilitiesData);
    }
});

// Disable modal-fix.js cleanup functions that interfere with our modal
if (window.modalUtils) {
    console.log('🔧 SCAN DETAILS: Disabling modal-fix.js interference...');
    
    // Store original functions
    window.originalModalUtils = { ...window.modalUtils };
    
    // Override with no-op functions for scan details
    window.modalUtils.hideModal = function(modalId) {
        console.log('🔧 SCAN DETAILS: Blocked modal-fix hideModal for', modalId);
        // Do nothing - let our custom modal handling work
    };
    
    window.modalUtils.cleanupModals = function() {
        console.log('🔧 SCAN DETAILS: Blocked modal-fix cleanupModals');
        // Do nothing - prevent size reset
    };
}

// Override any modal event listeners from modal-fix.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 SCAN DETAILS: Setting up modal-fix override...');
    
    // Remove modal-fix.js event listeners
    const modal = document.getElementById('cveDetailsModal');
    if (modal) {
        // Clone modal to remove all event listeners
        const newModal = modal.cloneNode(true);
        modal.parentNode.replaceChild(newModal, modal);
        
        console.log('✅ SCAN DETAILS: Modal event listeners cleared');
    }
}, { once: true });

// Make functions globally accessible
window.showCVEDetails = showCVEDetails;
window.switchModalTab = switchModalTab;
window.toggleFullscreen = toggleFullscreen;
window.markAsReviewed = markAsReviewed;
window.analyzeWithGrok = analyzeWithGrok;
window.exportResults = exportResults;
window.downloadScanReport = downloadScanReport;
window.initializeScanDetails = initializeScanDetails;

console.log('✅ SCAN DETAILS: JavaScript loaded successfully');

