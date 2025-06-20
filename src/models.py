# -*- coding: utf-8 -*-
from datetime import datetime
import json
from src import db

class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'employee_code': self.employee_code,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_code = db.Column(db.String(20), unique=True, nullable=False)  # Mã dự án
    key = db.Column(db.String(20), unique=True, nullable=False)  # Key dự án
    project_name = db.Column(db.String(100), nullable=False)  # Tên dự án
    # Relationship với Manager (Many-to-One) - Quản lý dự án
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'), nullable=False)
    manager = db.relationship('Manager', backref=db.backref('managed_projects', lazy=True))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'project_code': self.project_code,
            'key': self.key,
            'project_name': self.project_name,
            'manager_id': self.manager_id,
            'manager': self.manager.name if self.manager else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Technology(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)  # Ánh xạ sang Project
    project = db.relationship('Project', backref='technologies')  # Thêm relationship
    vendor = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Thêm unique constraint để đảm bảo mỗi project chỉ có 1 component với tên duy nhất
    __table_args__ = (
        db.UniqueConstraint('name', 'project_id', name='unique_component_per_project'),
    )

class CVE(db.Model):
    __tablename__ = 'cve'  # Thêm tên bảng rõ ràng
    id = db.Column(db.Integer, primary_key=True)
    cve_id = db.Column(db.String(20), unique=True, nullable=False)  # CVE-2023-1234
    description = db.Column(db.Text, nullable=True)
    publish_date = db.Column(db.String(50), nullable=True)
    severity = db.Column(db.String(20), nullable=True)  # LOW, MEDIUM, HIGH, CRITICAL
    cvss_score = db.Column(db.Float, nullable=True)
    vector_attack = db.Column(db.String(20), nullable=True)  # NETWORK, ADJACENT, LOCAL
    attack_complexity = db.Column(db.String(20), nullable=True)
    attack_requirements = db.Column(db.String(50), nullable=True)
    privileges_required = db.Column(db.String(20), nullable=True)
    vector_string = db.Column(db.String(200), nullable=True)
    source_identifier = db.Column(db.String(100), nullable=True)
    vuln_status = db.Column(db.String(50), nullable=True)
    last_modified = db.Column(db.String(50), nullable=True)
    references = db.Column(db.Text, nullable=True)  # JSON string
    weaknesses = db.Column(db.Text, nullable=True)  # JSON string
    affected_products = db.Column(db.Text, nullable=True)  # JSON string
    extra_info = db.Column(db.Text, nullable=True)  # JSON for additional data
    is_analyzed = db.Column(db.Boolean, default=False)
    ai_analysis = db.Column(db.Text, nullable=True)  # AI analysis result
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ScanSession(db.Model):
    __tablename__ = 'scan_sessions'  # Đảm bảo tên bảng đúng với foreign key
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)  # CVE filter start date
    end_date = db.Column(db.String(20), nullable=False)    # CVE filter end date
    scan_start_time = db.Column(db.DateTime, default=datetime.utcnow)
    scan_end_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='RUNNING')  # RUNNING, COMPLETED, FAILED
    total_cves_found = db.Column(db.Integer, default=0)
    total_technologies_scanned = db.Column(db.Integer, default=0)
    vulnerabilities_found = db.Column(db.Integer, default=0)
    critical_count = db.Column(db.Integer, default=0)
    high_count = db.Column(db.Integer, default=0)
    medium_count = db.Column(db.Integer, default=0)
    low_count = db.Column(db.Integer, default=0)
    error_log = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class VulnerabilityReport(db.Model):
    __tablename__ = 'vulnerability_reports'  # Đổi tên bảng về số nhiều cho đồng bộ

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('scan_sessions.id'), nullable=False)
    cve_id = db.Column(db.Integer, db.ForeignKey('cve.id'), nullable=False)  # Sửa từ 'cves.id' thành 'cve.id'
    
    # Denormalized technology fields (không cần foreign key)
    technology_name = db.Column(db.String(255), nullable=False, default='')
    technology_version = db.Column(db.String(50), nullable=True)
    technology_category = db.Column(db.String(100), nullable=True)
    technology_vendor = db.Column(db.String(255), nullable=True)
    
    # Denormalized project/manager fields
    project_name = db.Column(db.String(255), nullable=True)
    manager_name = db.Column(db.String(255), nullable=True)
    
    # Denormalized CVE fields
    cve_identifier = db.Column(db.String(20), nullable=False, default='')
    cvss_score = db.Column(db.Float, nullable=True)
    cvss_severity = db.Column(db.String(20), nullable=True)
    published_date = db.Column(db.String(50), nullable=True)
    attack_vector = db.Column(db.String(20), nullable=True)
    attack_complexity = db.Column(db.String(20), nullable=True)
    privileges_required = db.Column(db.String(20), nullable=True)
    
    # Analysis fields
    confidence_score = db.Column(db.Float, nullable=True)
    match_type = db.Column(db.String(255), nullable=True)
    risk_assessment = db.Column(db.String(20), nullable=True)
    mitigation_status = db.Column(db.String(50), default='PENDING')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships - chỉ cần sửa lại tên bảng cho đúng
    session = db.relationship('ScanSession',
                              foreign_keys=[session_id],
                              backref=db.backref('vulnerability_reports', lazy='dynamic'))
    cve = db.relationship('CVE',
                          foreign_keys=[cve_id],
                          backref=db.backref('vulnerability_reports', lazy='dynamic'))

    def __repr__(self):
        return '<VulnerabilityReport {} - {}>'.format(self.cve_identifier, self.technology_name)
