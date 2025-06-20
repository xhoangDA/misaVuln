# create_missing_columns.py
from flask import Flask
from models import db
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ntlong:new_password@10.1.36.248/project_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def add_missing_columns():
    with app.app_context():
        connection = pymysql.connect(
            host='10.1.36.248',
            user='ntlong',
            password='new_password',
            database='project_management',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        print("Checking and adding missing columns...")
        
        # Check if columns exist first
        cursor.execute("DESCRIBE vulnerability_report")
        existing_columns = [row[0] for row in cursor.fetchall()]
        print(f"Existing columns: {existing_columns}")
        
        # List of columns to add if they don't exist
        columns_to_add = [
            ("technology_name", "VARCHAR(255) NOT NULL DEFAULT ''"),
            ("technology_version", "VARCHAR(50) NULL"),
            ("technology_category", "VARCHAR(100) NULL"),
            ("technology_vendor", "VARCHAR(255) NULL"),
            ("project_name", "VARCHAR(255) NULL"),
            ("manager_name", "VARCHAR(255) NULL"),
            ("cve_identifier", "VARCHAR(20) NOT NULL DEFAULT ''"),
            ("cvss_score", "FLOAT NULL"),
            ("cvss_severity", "VARCHAR(20) NULL"),
            ("published_date", "VARCHAR(50) NULL"),
            ("attack_vector", "VARCHAR(20) NULL"),
            ("attack_complexity", "VARCHAR(20) NULL"),
            ("privileges_required", "VARCHAR(20) NULL"),
            ("confidence_score", "FLOAT NULL"),
            ("match_type", "VARCHAR(255) NULL"),
            ("risk_assessment", "VARCHAR(20) NULL"),
            ("mitigation_status", "VARCHAR(50) DEFAULT 'PENDING'"),
            ("created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
            ("updated_at", "DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
        ]
        
        for column_name, column_def in columns_to_add:
            if column_name not in existing_columns:
                try:
                    sql = f"ALTER TABLE vulnerability_report ADD COLUMN {column_name} {column_def}"
                    cursor.execute(sql)
                    print(f"✓ Added column: {column_name}")
                except Exception as e:
                    print(f"✗ Error adding {column_name}: {e}")
            else:
                print(f"- Column {column_name} already exists")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("✓ All missing columns processed!")

if __name__ == '__main__':
    add_missing_columns()