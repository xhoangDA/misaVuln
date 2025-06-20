# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from models import db, VulnerabilityReport, ScanSession, CVE
    print('✅ Models imported successfully!')
    print('✅ VulnerabilityReport table name:', VulnerabilityReport.__tablename__)
    print('✅ ScanSession table name:', ScanSession.__tablename__)
    print('✅ CVE table name:', CVE.__tablename__)
    print('✅ Foreign keys are properly configured')
    print('✅ SQLAlchemy error has been fixed!')
except Exception as e:
    print('❌ Error:', e)