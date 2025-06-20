# -*- coding: utf-8 -*-
from flask import Flask
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ntlong:new_password@10.1.36.248/project_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        connection = db.engine.connect()
        
        # Kiểm tra các bảng hiện có
        result = connection.execute("SHOW TABLES")
        tables = [row[0] for row in result]
        print("Current tables:", tables)
        
        # Kiểm tra nếu bảng vulnerability_reports chưa tồn tại thì tạo
        if 'vulnerability_reports' not in tables:
            print("Creating vulnerability_reports table...")
            try:
                connection.execute("""
                    CREATE TABLE vulnerability_reports (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        session_id INT NOT NULL,
                        cve_id INT NOT NULL,
                        technology_name VARCHAR(255) NOT NULL DEFAULT '',
                        technology_version VARCHAR(50),
                        technology_category VARCHAR(100),
                        technology_vendor VARCHAR(255),
                        project_name VARCHAR(255),
                        manager_name VARCHAR(255),
                        cve_identifier VARCHAR(20) NOT NULL DEFAULT '',
                        cvss_score FLOAT,
                        cvss_severity VARCHAR(20),
                        published_date VARCHAR(50),
                        attack_vector VARCHAR(20),
                        attack_complexity VARCHAR(20),
                        privileges_required VARCHAR(20),
                        confidence_score FLOAT,
                        match_type VARCHAR(255),
                        risk_assessment VARCHAR(20),
                        mitigation_status VARCHAR(50) DEFAULT 'PENDING',
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        FOREIGN KEY (session_id) REFERENCES scan_sessions(id),
                        FOREIGN KEY (cve_id) REFERENCES cve(id)
                    )
                """)
                print("vulnerability_reports table created successfully")
            except Exception as e:
                print("Error creating vulnerability_reports:", e)
        
        # Di chuyển dữ liệu từ bảng cũ nếu tồn tại
        if 'vulnerability_report' in tables and 'vulnerability_reports' in tables:
            print("Migrating data from vulnerability_report to vulnerability_reports...")
            try:
                connection.execute("""
                    INSERT IGNORE INTO vulnerability_reports 
                    (id, session_id, cve_id, technology_name, technology_version, technology_category, 
                     technology_vendor, project_name, manager_name, cve_identifier, cvss_score, 
                     cvss_severity, published_date, attack_vector, attack_complexity, privileges_required,
                     confidence_score, match_type, risk_assessment, mitigation_status, created_at, updated_at)
                    SELECT id, session_id, cve_id, technology_name, technology_version, technology_category,
                           technology_vendor, project_name, manager_name, cve_identifier, cvss_score,
                           cvss_severity, published_date, attack_vector, attack_complexity, privileges_required,
                           confidence_score, match_type, risk_assessment, mitigation_status, created_at, updated_at
                    FROM vulnerability_report
                """)
                print("Data migration completed")
            except Exception as e:
                print("Error migrating data:", e)
        
        # Xóa bảng cũ nếu tồn tại
        if 'vulnerability_report' in tables:
            print("Dropping old vulnerability_report table...")
            try:
                connection.execute("DROP TABLE vulnerability_report")
                print("Old table dropped successfully")
            except Exception as e:
                print("Error dropping old table:", e)
        
        # Xóa bảng scan_session cũ nếu tồn tại
        if 'scan_session' in tables:
            print("Dropping old scan_session table...")
            try:
                # Di chuyển dữ liệu trước nếu cần
                if 'scan_sessions' in tables:
                    connection.execute("INSERT IGNORE INTO scan_sessions SELECT * FROM scan_session")
                connection.execute("DROP TABLE scan_session")
                print("Old scan_session table dropped successfully")
            except Exception as e:
                print("Error dropping old scan_session table:", e)
        
        connection.close()
        print("Database schema fix completed!")