// Enhanced CVE Scanner JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializeCVEScanner();
    initializeModelSelection();
    initializeAnimations();
    loadSystemStats();
});

// Initialize CVE Scanner functionality
function initializeCVEScanner() {
    // Set default dates
    const today = new Date();
    const lastMonth = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
    
    document.getElementById('endDate').value = today.toISOString().split('T')[0];
    document.getElementById('startDate').value = lastMonth.toISOString().split('T')[0];
    
    // Initialize date validation
    document.getElementById('startDate').addEventListener('change', validateDateRange);
    document.getElementById('endDate').addEventListener('change', validateDateRange);
}

// Model selection functionality - Updated
function initializeModelSelection() {
    const modelCards = document.querySelectorAll('.model-card');
    
    modelCards.forEach(card => {
        card.addEventListener('click', function() {
            const modelType = this.getAttribute('data-model');
            
            // Remove active class from all cards
            modelCards.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked card
            this.classList.add('active');
            
            // Handle different model selections
            if (modelType === 'mitre-attack') {
                // Show scan history for MITRE ATT&CK model
                showScanHistory();
                return;
            }
            
            // Show notification for other models
            const modelName = this.querySelector('h4').textContent;
            showNotification(`Selected: ${modelName}`, 'success');
            
            // Animate selection
            gsap.fromTo(this, 
                { scale: 0.95 },
                { scale: 1, duration: 0.3, ease: "back.out(1.7)" }
            );
        });
    });
}

// Quick date range selection
function setQuickDateRange(range) {
    const today = new Date();
    const endDate = today.toISOString().split('T')[0];
    let startDate;
    
    switch(range) {
        case '7days':
            startDate = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
            break;
        case '30days':
            startDate = new Date(today.getTime() - 30 * 24 * 60 * 60 * 1000);
            break;
        case '90days':
            startDate = new Date(today.getTime() - 90 * 24 * 60 * 60 * 1000);
            break;
        default:
            return;
    }
    
    document.getElementById('endDate').value = endDate;
    document.getElementById('startDate').value = startDate.toISOString().split('T')[0];
    
    // Animate button feedback
    const clickedBtn = event.target.closest('.quick-btn');
    gsap.fromTo(clickedBtn, 
        { scale: 0.95, backgroundColor: 'rgba(16, 185, 129, 0.2)' },
        { scale: 1, backgroundColor: 'rgba(31, 41, 55, 0.8)', duration: 0.3 }
    );
    
    showNotification(`Date range set to last ${range.replace('days', ' days')}`, 'info');
}

// Validate date range
function validateDateRange() {
    const startDate = new Date(document.getElementById('startDate').value);
    const endDate = new Date(document.getElementById('endDate').value);
    const today = new Date();
    
    if (startDate > endDate) {
        showNotification('Start date cannot be after end date', 'warning');
        return false;
    }
    
    if (endDate > today) {
        showNotification('End date cannot be in the future', 'warning');
        return false;
    }
    
    return true;
}

// Start CVE scan - Updated to use real API with JSON data
function startCVEScan() {
    if (!validateDateRange()) {
        return;
    }
    
    const scanBtn = document.getElementById('startScanBtn');
    const originalText = scanBtn.innerHTML;
    
    // Show loading state
    scanBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span>Initializing Scan...</span>';
    scanBtn.disabled = true;
    
    // Get form data as JSON (not FormData)
    const requestData = {
        start_date: document.getElementById('startDate').value,
        end_date: document.getElementById('endDate').value
    };
    
    // Show scan progress
    showScanProgress();
    
    // Make actual API call to backend with JSON data
    fetch('/cve-scan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);
        
        if (!response.ok) {
            return response.text().then(text => {
                console.error('Server error response:', text);
                throw new Error(`Server error: ${response.status} - ${response.statusText}`);
            });
        }
        
        // Check if response is JSON
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            return response.text().then(text => {
                console.error('Non-JSON response received:', text);
                throw new Error(`Server returned non-JSON response: ${contentType}`);
            });
        }
        
        return response.json();
    })
    .then(data => {
        console.log('Scan response data:', data);
        if (data && data.success) {
            // Clear intervals first
            if (window.scanProgressInterval) {
                clearInterval(window.scanProgressInterval);
            }
            if (window.scanTimeInterval) {
                clearInterval(window.scanTimeInterval);
            }
            
            // Update scan statistics
            updateScanStatistics(data.stats || {});
            
            // Show scan results with real data
            showRealScanResults(data.vulnerabilities || [], data.stats || {});
            
            showNotification(`Scan completed! Found ${data.stats?.vulnerabilities_found || 0} vulnerabilities`, 'success');
        } else {
            throw new Error(data?.message || 'Scan failed - Invalid response format');
        }
    })
    .catch(error => {
        console.error('Scan error details:', error);
        
        let errorMessage = 'Unknown error occurred';
        if (error.message) {
            errorMessage = error.message;
        } else if (error.name === 'TypeError' && error.message.includes('fetch')) {
            errorMessage = 'Network connection failed - Check if server is running';
        } else if (error.name === 'SyntaxError' && error.message.includes('JSON')) {
            errorMessage = 'Server returned invalid response format';
        }
        
        showNotification(`Scan failed: ${errorMessage}`, 'error');
        
        // Hide progress section on error
        const progressSection = document.getElementById('scanProgressSection');
        if (progressSection) {
            progressSection.style.display = 'none';
        }
        
        // Clean up intervals
        if (window.scanProgressInterval) {
            clearInterval(window.scanProgressInterval);
        }
        if (window.scanTimeInterval) {
            clearInterval(window.scanTimeInterval);
        }
    })
    .finally(() => {
        // Reset scan button
        scanBtn.innerHTML = originalText;
        scanBtn.disabled = false;
    });
    
    showNotification('CVE scan initiated successfully', 'success');
}

// Show scan progress section
function showScanProgress() {
    const progressSection = document.getElementById('scanProgressSection');
    progressSection.style.display = 'block';
    
    // Initialize progress bar
    const progressBar = document.getElementById('scanProgressBar');
    const progressText = document.getElementById('scanProgressText');
    progressBar.style.width = '0%';
    progressText.textContent = '0%';
    
    // Reset counters
    document.getElementById('scannedCVEs').textContent = '0';
    document.getElementById('scannedTechnologies').textContent = '0';
    document.getElementById('vulnerabilitiesFound').textContent = '0';
    document.getElementById('scanElapsedTime').textContent = '0s';
    
    // Start elapsed time counter
    startElapsedTimeCounter();
    
    // Simulate progress animation
    simulateProgressAnimation();
    
    // Scroll to progress section
    progressSection.scrollIntoView({ behavior: 'smooth' });
    
    // Animate progress section appearance
    gsap.fromTo(progressSection, 
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }
    );
}

// Simulate progress animation while waiting for real data
function simulateProgressAnimation() {
    let progress = 0;
    let cveCount = 0;
    let techCount = 0;
    
    const progressInterval = setInterval(() => {
        progress += Math.random() * 15 + 5; // Random increment 5-20%
        if (progress > 95) progress = 95; // Stop at 95% until real completion
        
        cveCount += Math.floor(Math.random() * 50 + 10);
        techCount += Math.floor(Math.random() * 3 + 1);
        
        // Update progress bar
        document.getElementById('scanProgressBar').style.width = progress + '%';
        document.getElementById('scanProgressText').textContent = Math.floor(progress) + '%';
        
        // Update counters
        document.getElementById('scannedCVEs').textContent = cveCount.toLocaleString();
        document.getElementById('scannedTechnologies').textContent = techCount;
        
        // Stop simulation when progress reaches 95%
        if (progress >= 95) {
            clearInterval(progressInterval);
        }
    }, 800);
    
    // Store interval ID for potential cleanup
    window.scanProgressInterval = progressInterval;
}

// Start elapsed time counter
function startElapsedTimeCounter() {
    let seconds = 0;
    
    const timeInterval = setInterval(() => {
        seconds++;
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        
        let timeText;
        if (minutes > 0) {
            timeText = `${minutes}m ${remainingSeconds}s`;
        } else {
            timeText = `${seconds}s`;
        }
        
        document.getElementById('scanElapsedTime').textContent = timeText;
    }, 1000);
    
    // Store interval ID for cleanup
    window.scanTimeInterval = timeInterval;
}

// Load system statistics
function loadSystemStats() {
    // Simulate loading system stats (replace with actual API call)
    setTimeout(() => {
        document.getElementById('totalTechnologies').textContent = '1,247';
        document.getElementById('totalProjects').textContent = '89';
        
        // Animate stat numbers
        animateNumbers();
    }, 500);
}

// Animate numbers counting up
function animateNumbers() {
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(element => {
        const finalValue = element.textContent.replace(/[,+]/g, '');
        if (!isNaN(finalValue)) {
            gsap.fromTo(element, 
                { textContent: 0 },
                { 
                    textContent: finalValue,
                    duration: 2,
                    ease: "power2.out",
                    snap: { textContent: 1 },
                    onUpdate: function() {
                        element.textContent = Math.floor(this.targets()[0].textContent).toLocaleString();
                    }
                }
            );
        }
    });
}

// Initialize animations
function initializeAnimations() {
    // Animate model cards on page load
    gsap.fromTo('.model-card', 
        { opacity: 0, y: 30, scale: 0.9 },
        { 
            opacity: 1, 
            y: 0, 
            scale: 1, 
            duration: 0.8, 
            stagger: 0.2,
            ease: "back.out(1.7)" 
        }
    );
    
    // Animate scan configuration card
    gsap.fromTo('.scan-config-card', 
        { opacity: 0, x: -50 },
        { opacity: 1, x: 0, duration: 0.8, delay: 0.3 }
    );
    
    // Animate stats panel
    gsap.fromTo('.stats-panel', 
        { opacity: 0, x: 50 },
        { opacity: 1, x: 0, duration: 0.8, delay: 0.5 }
    );
}

// Utility function to get risk color class
function getRiskColor(risk) {
    switch(risk.toLowerCase()) {
        case 'critical': return 'danger';
        case 'high': return 'warning';
        case 'medium': return 'info';
        case 'low': return 'success';
        default: return 'secondary';
    }
}

// Utility function to get CVSS score color
function getCVSSColor(score) {
    if (typeof score === 'string' && score === 'N/A') return 'secondary';
    const numScore = parseFloat(score);
    if (numScore >= 9.0) return 'danger';
    if (numScore >= 7.0) return 'warning';
    if (numScore >= 4.0) return 'info';
    return 'success';
}

// Show notification function
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    `;
    
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-${getNotificationIcon(type)} me-2"></i>
            <span>${message}</span>
        </div>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Get notification icon based on type
function getNotificationIcon(type) {
    switch(type) {
        case 'success': return 'check-circle';
        case 'error': 
        case 'danger': return 'exclamation-triangle';
        case 'warning': return 'exclamation-circle';
        case 'info': return 'info-circle';
        default: return 'bell';
    }
}

// Add missing functions for handling scan results
function updateScanStatistics(stats) {
    // Clear any existing intervals
    if (window.scanProgressInterval) {
        clearInterval(window.scanProgressInterval);
    }
    if (window.scanTimeInterval) {
        clearInterval(window.scanTimeInterval);
    }
    
    document.getElementById('scannedCVEs').textContent = stats.total_cves || 0;
    document.getElementById('scannedTechnologies').textContent = stats.total_technologies || 0;
    document.getElementById('vulnerabilitiesFound').textContent = stats.vulnerabilities_found || 0;
    
    // Update progress bar to 100%
    const progressBar = document.getElementById('scanProgressBar');
    const progressText = document.getElementById('scanProgressText');
    progressBar.style.width = '100%';
    progressText.textContent = '100%';
}

function showRealScanResults(vulnerabilities, stats) {
    // Hide scan progress section after scan completes
    const progressSection = document.getElementById('scanProgressSection');
    if (progressSection) progressSection.style.display = 'none';

    // Store results globally for modal access
    window.lastScanResults = vulnerabilities;
    
    const resultsSection = document.getElementById('scanResultsSection');
    resultsSection.style.display = 'block';
    
    // Update vulnerability counts from real data
    document.getElementById('criticalCount').textContent = stats.critical || 0;
    document.getElementById('highCount').textContent = stats.high || 0;
    document.getElementById('mediumCount').textContent = stats.medium || 0;
    document.getElementById('lowCount').textContent = stats.low || 0;
    
    // Populate vulnerabilities table with real data
    populateRealVulnerabilitiesTable(vulnerabilities);
    
    // Animate vulnerability cards
    const vulnCards = document.querySelectorAll('.vulnerability-card');
    vulnCards.forEach((card, index) => {
        gsap.fromTo(card, 
            { opacity: 0, y: 30, scale: 0.9 },
            { 
                opacity: 1, 
                y: 0, 
                scale: 1, 
                duration: 0.6, 
                delay: index * 0.1,
                ease: "back.out(1.7)" 
            }
        );
    });
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

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
    
    // DEBUG: Log all CVE IDs before filtering
    const allCveIds = vulnerabilities.map(v => v.cve?.cve_id).filter(id => id);
    console.log('DEBUG: All CVE IDs before filtering:', allCveIds);
    console.log('DEBUG: Total vulnerabilities:', vulnerabilities.length);
    
    // Cải thiện logic loại bỏ CVE trùng lặp - sử dụng Map để tăng hiệu suất
    const uniqueVulnsMap = new Map();
    
    vulnerabilities.forEach((vuln, originalIndex) => {
        const cveId = vuln.cve?.cve_id;
        
        // Chỉ xử lý nếu có CVE ID hợp lệ
        if (cveId && typeof cveId === 'string' && cveId.trim() !== '') {
            const cleanCveId = cveId.trim().toUpperCase(); // Chuẩn hóa CVE ID
            
            console.log(`DEBUG: Processing vulnerability ${originalIndex}: CVE ${cleanCveId}`);
            
            // Nếu chưa có CVE này trong Map hoặc vulnerability hiện tại có độ ưu tiên cao hơn
            if (!uniqueVulnsMap.has(cleanCveId)) {
                uniqueVulnsMap.set(cleanCveId, vuln);
                console.log(`DEBUG: Added unique CVE: ${cleanCveId}`);
            } else {
                console.log(`DEBUG: Skipped duplicate CVE: ${cleanCveId}`);
                
                // Có thể chọn vulnerability có risk cao hơn nếu muốn
                const existing = uniqueVulnsMap.get(cleanCveId);
                const existingRisk = existing.analysis?.risk_assessment?.toLowerCase() || 'unknown';
                const currentRisk = vuln.analysis?.risk_assessment?.toLowerCase() || 'unknown';
                
                const riskPriority = { 'critical': 4, 'high': 3, 'medium': 2, 'low': 1, 'unknown': 0 };
                
                if (riskPriority[currentRisk] > riskPriority[existingRisk]) {
                    uniqueVulnsMap.set(cleanCveId, vuln);
                    console.log(`DEBUG: Replaced CVE ${cleanCveId} with higher risk (${currentRisk} > ${existingRisk})`);
                }
            }
        } else {
            console.log(`DEBUG: Skipped vulnerability ${originalIndex} - invalid CVE ID:`, cveId);
        }
    });
    
    const uniqueVulns = Array.from(uniqueVulnsMap.values());
    
    console.log(`DEBUG: Original count: ${vulnerabilities.length}, Unique count: ${uniqueVulns.length}`);
    console.log('DEBUG: Unique CVE IDs:', uniqueVulns.map(v => v.cve?.cve_id));
    
    // Show notification about filtering
    if (vulnerabilities.length > uniqueVulns.length) {
        const duplicateCount = vulnerabilities.length - uniqueVulns.length;
        showNotification(`Filtered ${duplicateCount} duplicate CVE${duplicateCount > 1 ? 's' : ''}. Showing ${uniqueVulns.length} unique vulnerabilities.`, 'info');
    }
    
    // Sắp xếp theo độ ưu tiên risk trước khi hiển thị
    const riskOrder = { 'critical': 4, 'high': 3, 'medium': 2, 'low': 1, 'unknown': 0 };
    uniqueVulns.sort((a, b) => {
        const riskA = a.analysis?.risk_assessment?.toLowerCase() || 'unknown';
        const riskB = b.analysis?.risk_assessment?.toLowerCase() || 'unknown';
        return riskOrder[riskB] - riskOrder[riskA]; // Sắp xếp từ cao xuống thấp
    });
    
    uniqueVulns.forEach((vuln, index) => {
        const row = document.createElement('tr');
        const riskClass = vuln.analysis?.risk_assessment?.toLowerCase() || 'unknown';
        const riskBadge = `<span class="badge bg-${getRiskColor(riskClass)}">${vuln.analysis?.risk_assessment || 'Unknown'}</span>`;
        const confidenceScore = vuln.analysis?.confidence_score ? (vuln.analysis.confidence_score * 100).toFixed(0) : '0';
        const confidenceBadge = `<span class="badge bg-info">${confidenceScore}%</span>`;
        const publishDate = vuln.cve?.publish_date ? new Date(vuln.cve.publish_date).toLocaleDateString() : 'N/A';
        const cvssScore = vuln.cve?.cvss_data?.baseScore || 'N/A';
        
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
                        <strong>${vuln.technology?.name || 'Unknown'}</strong>
                        ${vuln.technology?.version ? `<small class="text-muted d-block">v${vuln.technology.version}</small>` : ''}
                        ${vuln.technology?.project_name ? `<small class="text-info d-block">${vuln.technology.project_name}</small>` : ''}
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
    
    // Cập nhật window.lastScanResults để modal vẫn hoạt động với dữ liệu unique
    window.lastScanResults = uniqueVulns;
    console.log('DEBUG: Updated window.lastScanResults with', uniqueVulns.length, 'unique vulnerabilities');
    
    // Thêm summary thống kê vào console để debug
    const summary = uniqueVulns.reduce((acc, vuln) => {
        const risk = vuln.analysis?.risk_assessment?.toLowerCase() || 'unknown';
        acc[risk] = (acc[risk] || 0) + 1;
        return acc;
    }, {});
    console.log('DEBUG: Risk distribution after deduplication:', summary);
}

// Hiển thị modal chi tiết CVE khi click vào nút con mắt hoặc link CVE ID
function showRealCVEDetails(cveId, index) {
    if (!window.lastScanResults || !Array.isArray(window.lastScanResults)) {
        showNotification('No scan results available for details', 'warning');
        return;
    }
    // Ưu tiên lấy theo index nếu hợp lệ
    let vuln = null;
    if (typeof index === 'number' && window.lastScanResults[index]) {
        vuln = window.lastScanResults[index];
    } else if (cveId) {
        vuln = window.lastScanResults.find(v => v.cve && v.cve.cve_id === cveId);
    }
    if (!vuln) {
        showNotification('Could not find vulnerability details for this CVE', 'error');
        return;
    }
    // Đổ dữ liệu vào modal (ví dụ)
    document.getElementById('modalFooterCveId').textContent = vuln.cve?.cve_id || 'N/A';
    document.getElementById('modalFooterAffectedCount').textContent =
        (vuln.technology?.name ? `1 affected component` : 'N/A');
    // TODO: Đổ các trường khác vào modal body nếu cần
    // ...
    // Hiển thị modal
    const modal = new bootstrap.Modal(document.getElementById('cveDetailsModal'));
    modal.show();
}

// Show scan history function
function showScanHistory() {
    // Hide scan configuration and results sections
    document.querySelector('.scan-section').style.display = 'none';
    document.getElementById('scanProgressSection').style.display = 'none';
    document.getElementById('scanResultsSection').style.display = 'none';
    
    // Show scan history section
    let historySection = document.getElementById('scanHistorySection');
    if (!historySection) {
        // Create scan history section if it doesn't exist
        createScanHistorySection();
        historySection = document.getElementById('scanHistorySection');
    }
    
    historySection.style.display = 'block';
    
    // Load scan history data
    loadScanHistory();
    
    // Animate section appearance
    gsap.fromTo(historySection, 
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }
    );
    
    // Scroll to history section
    historySection.scrollIntoView({ behavior: 'smooth' });
    
    showNotification('Loading scan history...', 'info');
}

// Create scan history section
function createScanHistorySection() {
    const historyHTML = `
    <!-- Scan History Section -->
    <div class="scan-history-section" id="scanHistorySection" style="display: none;">
        <div class="container-fluid">
            <!-- History Header -->
            <div class="history-header">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <div>
                        <h2><i class="fas fa-history text-primary me-2"></i>Scan History</h2>
                        <p class="text-muted">Review and manage your previous vulnerability scans</p>
                    </div>
                    <div class="d-flex gap-2">
                        <button class="btn btn-outline-primary" onclick="showCurrentScan()">
                            <i class="fas fa-search me-1"></i>
                            New Scan
                        </button>
                        <button class="btn btn-outline-secondary" onclick="exportScanHistory()">
                            <i class="fas fa-download me-1"></i>
                            Export History
                        </button>
                    </div>
                </div>
            </div>

            <!-- History Statistics -->
            <div class="history-stats mb-4">
                <div class="row g-3">
                    <div class="col-lg-3 col-md-6">
                        <div class="stat-card-history">
                            <div class="stat-icon-history">
                                <i class="fas fa-search text-primary"></i>
                            </div>
                            <div class="stat-content-history">
                                <div class="stat-number-history" id="totalScansCount">0</div>
                                <div class="stat-label-history">Total Scans</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-6">
                        <div class="stat-card-history">
                            <div class="stat-icon-history">
                                <i class="fas fa-exclamation-triangle text-danger"></i>
                            </div>
                            <div class="stat-content-history">
                                <div class="stat-number-history" id="totalVulnsFound">0</div>
                                <div class="stat-label-history">Vulnerabilities Found</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-6">
                        <div class="stat-card-history">
                            <div class="stat-icon-history">
                                <i class="fas fa-clock text-info"></i>
                            </div>
                            <div class="stat-content-history">
                                <div class="stat-number-history" id="avgScanTime">0m</div>
                                <div class="stat-label-history">Avg Scan Time</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-6">
                        <div class="stat-card-history">
                            <div class="stat-icon-history">
                                <i class="fas fa-calendar text-success"></i>
                            </div>
                            <div class="stat-content-history">
                                <div class="stat-number-history" id="lastScanDate">N/A</div>
                                <div class="stat-label-history">Last Scan</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- History Table -->
            <div class="history-table-container">
                <div class="card cyber-card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="mb-0"><i class="fas fa-list me-2"></i>Scan Sessions</h5>
                        <div class="d-flex gap-2">
                            <div class="search-box-small">
                                <i class="fas fa-search"></i>
                                <input type="text" placeholder="Search sessions..." id="historyFilter">
                            </div>
                            <select class="form-select form-select-sm" id="statusFilter" style="width: auto;">
                                <option value="">All Status</option>
                                <option value="COMPLETED">Completed</option>
                                <option value="RUNNING">Running</option>
                                <option value="FAILED">Failed</option>
                            </select>
                        </div>
                    </div>
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-hover cyber-table mb-0" id="scanHistoryTable">
                                <thead>
                                    <tr>
                                        <th>Session</th>
                                        <th>Date Range</th>
                                        <th>Status</th>
                                        <th>Duration</th>
                                        <th>Results</th>
                                        <th>Technologies</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody id="scanHistoryTableBody">
                                    <tr>
                                        <td colspan="7" class="text-center py-4">
                                            <div class="spinner-border text-primary" role="status">
                                                <span class="visually-hidden">Loading...</span>
                                            </div>
                                            <div class="mt-2 text-muted">Loading scan history...</div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>`;
    
    // Insert history section after model selection
    const modelSection = document.querySelector('.model-selection');
    modelSection.insertAdjacentHTML('afterend', historyHTML);
}

// Load scan history from server
function loadScanHistory() {
    fetch('/api/scan-history', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
               }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateHistoryStatistics(data.stats);
            populateScanHistoryTable(data.sessions);
        } else {
            throw new Error(data.message || 'Failed to load scan history');
        }
    })
    .catch(error => {
        console.error('Error loading scan history:', error);
        showNotification('Failed to load scan history', 'error');
        
        // Show error state in table
        const tbody = document.getElementById('scanHistoryTableBody');
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center py-4">
                    <div class="text-danger">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        Failed to load scan history
                    </div>
                </td>
            </tr>`;
    });
}

// Update history statistics
function updateHistoryStatistics(stats) {
    document.getElementById('totalScansCount').textContent = stats.total_scans || 0;
    document.getElementById('totalVulnsFound').textContent = stats.total_vulnerabilities || 0;
    document.getElementById('avgScanTime').textContent = stats.avg_scan_time || '0m';
    document.getElementById('lastScanDate').textContent = stats.last_scan_date || 'N/A';
}

// Populate scan history table
function populateScanHistoryTable(sessions) {
    const tbody = document.getElementById('scanHistoryTableBody');
    tbody.innerHTML = '';
    
    if (!sessions || sessions.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center py-4">
                    <div class="text-muted">
                        <i class="fas fa-inbox me-2"></i>
                        No scan sessions found
                    </div>
                </td>
            </tr>`;
        return;
    }
    
    sessions.forEach((session, index) => {
        const row = document.createElement('tr');
        const statusBadge = getStatusBadge(session.status);
        const duration = calculateDuration(session.scan_start_time, session.scan_end_time);
        const vulnerabilityBreakdown = getVulnerabilityBreakdown(session);
        
        row.innerHTML = `
            <td>
                <div class="d-flex align-items-center">
                    <div class="session-icon me-3">
                        <i class="fas fa-search"></i>
                    </div>
                    <div>
                        <strong>${session.name}</strong>
                        <small class="text-muted d-block">${formatDate(session.scan_start_time)}</small>
                    </div>
                </div>
            </td>
            <td>
                <div class="date-range">
                    <div><strong>${session.start_date}</strong></div>
                    <div class="text-muted small">to ${session.end_date}</div>
                </div>
            </td>
            <td>${statusBadge}</td>
            <td>
                <span class="badge bg-info bg-opacity-10 text-info border border-info">
                    ${duration}
                </span>
            </td>
            <td>
                <div class="vulnerability-summary-small">
                    ${vulnerabilityBreakdown}
                    <div class="text-muted small mt-1">Total: ${session.vulnerabilities_found || 0}</div>
                </div>
            </td>
            <td>
                <span class="badge bg-secondary bg-opacity-10 text-secondary border border-secondary">
                    ${session.total_technologies_scanned ||  0} scanned
                </span>
            </td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" onclick="viewScanDetails(${session.id})" title="View Details">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-outline-success" onclick="downloadScanReport(${session.id})" title="Download Report">
                        <i class="fas fa-download"></i>
                    </button>
                    ${session.status === 'COMPLETED' ? `
                        <button class="btn btn-outline-info" onclick="rescanSession(${session.id})" title="Re-scan">
                            <i class="fas fa-redo"></i>
                        </button>
                    ` : ''}
                </div>
            </td>
        `;
        
        tbody.appendChild(row);
    });
}

// Helper functions
function getStatusBadge(status) {
    const statusConfig = {
        'COMPLETED': { class: 'success', icon: 'check-circle' },
        'RUNNING': { class: 'primary', icon: 'spinner fa-spin' },
        'FAILED': { class: 'danger', icon: 'exclamation-triangle' }
    };
    
    const config = statusConfig[status] || { class: 'secondary', icon: 'question-circle' };
    return `<span class="badge bg-${config.class}"><i class="fas fa-${config.icon} me-1"></i>${status}</span>`;
}

function calculateDuration(startTime, endTime) {
    if (!startTime || !endTime) return 'N/A';
    
    const start = new Date(startTime);
    const end = new Date(endTime);
    const diffMs = end - start;
    const diffMins = Math.floor(diffMs / 60000);
    const diffSecs = Math.floor((diffMs % 60000) / 1000);
    
    if (diffMins > 0) {
        return `${diffMins}m ${diffSecs}s`;
    }
    return `${diffSecs}s`;
}

function getVulnerabilityBreakdown(session) {
    const critical = session.critical_count || 0;
    const high = session.high_count || 0;
    const medium = session.medium_count || 0;
    const low = session.low_count || 0;
    
    return `
        <div class="d-flex gap-1">
            ${critical > 0 ? `<span class="badge bg-danger text-xs">${critical}C</span>` : ''}
            ${high > 0 ? `<span class="badge bg-warning text-xs">${high}H</span>` : ''}
            ${medium > 0 ? `<span class="badge bg-info text-xs">${medium}M</span>` : ''}
            ${low > 0 ? `<span class="badge bg-success text-xs">${low}L</span>` : ''}
        </div>
    `;
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Action functions
function showCurrentScan() {
    // Hide history section and show scan section
    document.getElementById('scanHistorySection').style.display = 'none';
    document.querySelector('.scan-section').style.display = 'block';
    
    // Reset model card selection to RAG LLM
    const modelCards = document.querySelectorAll('.model-card');
    modelCards.forEach(card => card.classList.remove('active'));
    modelCards[0].classList.add('active'); // First card (RAG LLM)
    
    showNotification('Switched to new scan mode', 'info');
}

function viewScanDetails(sessionId) {
    // Implement view scan details functionality
    window.location.href = `/scan-details/${sessionId}`;
    // showNotification(`Loading details for scan session ${sessionId}`, 'info');
    // You can implement a detailed modal or page here
}

function downloadScanReport(sessionId) {
    // Implement download report functionality
    window.open(`/api/scan-report/${sessionId}`, '_blank');
    showNotification(`Downloading report for scan ${sessionId}`, 'success');
}

function rescanSession(sessionId) {
    // Implement re-scan functionality
    if (confirm('Are you sure you want to re-run this scan session?')) {
        showNotification(`Re-scanning session ${sessionId}`, 'info');
        // Implement re-scan logic here
    }
}

function exportScanHistory() {
    // Implement export history functionality
    window.open('/api/export-scan-history', '_blank');
    showNotification('Exporting scan history...', 'info');
}

// Auto-refresh scan history after successful scan
function handleScanSuccess(data) {
    // ...existing scan success handling...
    
    // If user is currently viewing scan history, refresh it
    const historySection = document.getElementById('scanHistorySection');
    if (historySection && historySection.style.display !== 'none') {
        // Delay refresh to allow database commit
        setTimeout(() => {
            loadScanHistory();
            showNotification('Scan history updated!', 'success');
        }, 1000);
    }
    
    // Add button to view latest scan in history
    const viewHistoryBtn = document.createElement('button');
    viewHistoryBtn.className = 'btn btn-outline-info btn-sm mt-2';
    viewHistoryBtn.innerHTML = '<i class="fas fa-history me-1"></i>View in History';
    viewHistoryBtn.onclick = () => {
        showScanHistory();
        // Scroll to top after showing history
        setTimeout(() => {
            document.getElementById('scanHistorySection').scrollIntoView({ behavior: 'smooth' });
        }, 300);
    };
    
    // Add button to scan results section
    const resultsSection = document.getElementById('scanResultsSection');
    if (resultsSection) {
        const existingBtn = resultsSection.querySelector('.btn-outline-info');
        if (!existingBtn) {
            const headerActions = resultsSection.querySelector('.d-flex.justify-content-between .d-flex.gap-2');
            if (headerActions) {
                headerActions.appendChild(viewHistoryBtn);
            }
        }
    }
}

// Update successful scan handling
function handleScanResponse(data) {
    if (data.success) {
        // ...existing success handling...
        handleScanSuccess(data);
    } else {
        // ...existing error handling...
    }
}
