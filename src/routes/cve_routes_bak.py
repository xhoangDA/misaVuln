# CVE scan and report related routes
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, Response
from src.models import ScanSession, VulnerabilityReport, CVE, Technology, Project, Manager
from src.utils.cve_scanner import CVEScanner
from src import db
import json, io, csv, traceback
from datetime import datetime
import pytz

cve_bp = Blueprint('cve', __name__)

@cve_bp.route('/cve-scan', methods=['GET', 'POST'])
def cve_scan():
    if request.method == 'POST':
        # --- API: JSON POST (from JS) ---
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = request.get_json() or {}
            # Mock scan result for demo (now matches frontend structure)
            result = {
                'success': True,
                'stats': {
                    'vulnerabilities_found': 3,
                    'critical': 1,
                    'high': 1,
                    'medium': 1,
                    'low': 0,
                    'total_cves': 3,
                    'total_technologies': 3
                },
                'vulnerabilities': [
                    {
                        'cve': {
                            'cve_id': 'CVE-2024-12345',
                            'description': 'Critical RCE in React',
                            'publish_date': '2024-05-01',
                            'cvss_data': { 'baseScore': 9.8, 'baseSeverity': 'CRITICAL' }
                        },
                        'technology': { 'name': 'React', 'version': '18.2.0', 'project_name': 'Demo Project' },
                        'analysis': { 'risk_assessment': 'CRITICAL', 'confidence_score': 0.95 }
                    },
                    {
                        'cve': {
                            'cve_id': 'CVE-2024-23456',
                            'description': 'High severity bug in Node.js',
                            'publish_date': '2024-04-15',
                            'cvss_data': { 'baseScore': 8.1, 'baseSeverity': 'HIGH' }
                        },
                        'technology': { 'name': 'Node.js', 'version': '20.0.0', 'project_name': 'Demo Project' },
                        'analysis': { 'risk_assessment': 'HIGH', 'confidence_score': 0.90 }
                    },
                    {
                        'cve': {
                            'cve_id': 'CVE-2024-34567',
                            'description': 'Medium risk in MySQL',
                            'publish_date': '2024-03-10',
                            'cvss_data': { 'baseScore': 6.2, 'baseSeverity': 'MEDIUM' }
                        },
                        'technology': { 'name': 'MySQL', 'version': '8.0.36', 'project_name': 'Demo Project' },
                        'analysis': { 'risk_assessment': 'MEDIUM', 'confidence_score': 0.80 }
                    }
                ]
            }
            return jsonify(result)
        # --- END API ---

        # Get the selected project and technology from the form
        project_id = request.form.get('project')
        technology_id = request.form.get('technology')

        # Get the file from the request
        file = request.files.get('file')

        # Validate the file type
        if not file or not file.filename.endswith('.csv'):
            flash('Invalid file type. Please upload a CSV file.', 'error')
            return redirect(request.url)

        # Read the CSV file
        file_contents = file.read().decode('utf-8')
        csv_reader = csv.reader(io.StringIO(file_contents))

        # Extract the header row
        header = next(csv_reader)

        # Extract the data rows
        data = [row for row in csv_reader]

        # Perform CVE scanning using the CVEScanner utility
        scanner = CVEScanner()
        scan_results = scanner.scan(data)

        # Save the scan session to the database
        session = ScanSession(project_id=project_id, technology_id=technology_id, file_name=file.filename)
        db.session.add(session)
        db.session.commit()

        # Save the scan results to the database
        for result in scan_results:
            vulnerability = VulnerabilityReport(session_id=session.id, **result)
            db.session.add(vulnerability)

        db.session.commit()

        flash('CVE scan completed successfully.', 'success')
        return redirect(url_for('cve.scan_details', session_id=session.id))

    # GET request - render the CVE scan form
    projects = Project.query.all()
    technologies = Technology.query.all()
    return render_template('cve_scan.html', projects=projects, technologies=technologies)

@cve_bp.route('/health')
def health_check():
    return jsonify(status='healthy')

@cve_bp.route('/api/scan-history', methods=['GET'])
def get_scan_history():
    # Get all scan sessions from the database
    scan_sessions = ScanSession.query.all()

    # Serialize the scan sessions to JSON
    result = []
    for session in scan_sessions:
        result.append({
            'id': session.id,
            'project_id': session.project_id,
            'technology_id': session.technology_id,
            'file_name': session.file_name,
            'created_at': session.created_at.isoformat(),
            'updated_at': session.updated_at.isoformat()
        })

    return jsonify(result)

@cve_bp.route('/api/scan-report/<int:session_id>')
def download_scan_report(session_id):
    # Get the scan session by ID
    session = ScanSession.query.get_or_404(session_id)

    # Get the associated vulnerability reports
    vulnerabilities = VulnerabilityReport.query.filter_by(session_id=session_id).all()

    # Generate the CSV report
    output = io.StringIO()
    csv_writer = csv.writer(output)

    # Write the header row
    csv_writer.writerow(['CVE ID', 'Description', 'Severity', 'Status'])

    # Write the vulnerability data rows
    for vulnerability in vulnerabilities:
        csv_writer.writerow([vulnerability.cve_id, vulnerability.description, vulnerability.severity, vulnerability.status])

    # Seek to the beginning of the StringIO buffer
    output.seek(0)

    # Return the CSV file as a response
    return Response(output, mimetype='text/csv', headers={'Content-Disposition': f'attachment; filename=scan_report_{session_id}.csv'})

@cve_bp.route('/api/export-scan-history')
def export_scan_history():
    # Get all scan sessions from the database
    scan_sessions = ScanSession.query.all()

    # Generate the CSV report
    output = io.StringIO()
    csv_writer = csv.writer(output)

    # Write the header row
    csv_writer.writerow(['ID', 'Project ID', 'Technology ID', 'File Name', 'Created At', 'Updated At'])

    # Write the scan session data rows
    for session in scan_sessions:
        csv_writer.writerow([session.id, session.project_id, session.technology_id, session.file_name, session.created_at, session.updated_at])

    # Seek to the beginning of the StringIO buffer
    output.seek(0)

    # Return the CSV file as a response
    return Response(output, mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=scan_history.csv'})

@cve_bp.route('/scan-details/<int:session_id>')
def scan_details(session_id):
    # Get the scan session by ID
    session = ScanSession.query.get_or_404(session_id)

    # Get the associated vulnerability reports
    vulnerabilities = VulnerabilityReport.query.filter_by(session_id=session_id).all()

    return render_template('scan_details.html', session=session, vulnerabilities=vulnerabilities)

@cve_bp.route('/api/technology-usage/<technology_name>')
def get_technology_usage(technology_name):
    # Get the projects using the specified technology
    projects = Project.query.filter(Project.technologies.any(name=technology_name)).all()

    # Serialize the project data to JSON
    result = []
    for project in projects:
        result.append({
            'id': project.id,
            'name': project.name,
            'description': project.description
        })

    return jsonify(result)

@cve_bp.route('/api/vulnerability-impact/<cve_identifier>')
def get_vulnerability_impact(cve_identifier):
    # Get the vulnerability report by CVE identifier
    vulnerability = VulnerabilityReport.query.filter_by(cve_id=cve_identifier).first()

    if not vulnerability:
        return jsonify(error='Vulnerability not found'), 404

    # Serialize the vulnerability data to JSON
    result = {
        'cve_id': vulnerability.cve_id,
        'description': vulnerability.description,
        'severity': vulnerability.severity,
        'status': vulnerability.status,
        'affected_projects': []
    }

    # Get the projects affected by this vulnerability
    for session in vulnerability.scan_sessions:
        project = Project.query.get(session.project_id)
        if project:
            result['affected_projects'].append({
                'id': project.id,
                'name': project.name
            })

    return jsonify(result)
