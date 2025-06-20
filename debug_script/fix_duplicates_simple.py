#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple script to fix duplicates for unique constraint
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from app import app, db
from sqlalchemy import text

def fix_duplicates():
    """Fix duplicates using direct SQL to avoid relationship issues"""
    print("🚀 FIXING DUPLICATES WITH DIRECT SQL")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Find duplicates
            result = db.session.execute(text("""
                SELECT name, project_id, COUNT(*) as count, GROUP_CONCAT(id) as ids
                FROM technology 
                WHERE project_id IS NOT NULL 
                GROUP BY name, project_id 
                HAVING COUNT(*) > 1
            """))
            
            duplicates = result.fetchall()
            
            if not duplicates:
                print("✅ Không có duplicate nào!")
                return True
                
            print(f"📊 Tìm thấy {len(duplicates)} nhóm duplicates:")
            
            for dup in duplicates:
                name, project_id, count, ids_str = dup
                ids = ids_str.split(',')
                print(f"  📦 {name} (Project ID: {project_id}) - {count} bản ghi - IDs: {ids_str}")
                
                # Keep first ID, delete others
                keep_id = ids[0]
                delete_ids = ids[1:]
                
                for delete_id in delete_ids:
                    db.session.execute(text("DELETE FROM technology WHERE id = :id"), {"id": int(delete_id)})
                    print(f"    ❌ Đã xóa ID {delete_id}")
                
                print(f"    ✅ Giữ lại ID {keep_id}")
            
            db.session.commit()
            print("✅ Đã xóa tất cả duplicates!")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Lỗi: {e}")
            return False

if __name__ == "__main__":
    if fix_duplicates():
        print("🎉 HOÀN THÀNH!")
    else:
        print("💥 THẤT BẠI!")
