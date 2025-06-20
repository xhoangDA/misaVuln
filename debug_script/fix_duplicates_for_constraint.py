#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to fix duplicate technology components specifically for unique constraint
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from app import app, db
from models import Technology, Project
from sqlalchemy import func, and_
from datetime import datetime

def find_and_fix_duplicates():
    """Find and fix duplicate entries based on name + project_id combination"""
    print("🔍 Tìm kiếm duplicates theo name + project_id...")
    
    # Tìm duplicates theo name và project_id (không quan tâm category)
    duplicates_query = db.session.query(
        Technology.name,
        Technology.project_id,
        func.count(Technology.id).label('count')
    ).group_by(
        Technology.name,
        Technology.project_id
    ).having(func.count(Technology.id) > 1)
    
    duplicates = duplicates_query.all()
    
    print("📊 Tìm thấy {} nhóm duplicates:".format(len(duplicates)))
    
    fixed_count = 0
    
    for dup in duplicates:
        # Lấy tất cả records trùng lặp
        duplicate_records = Technology.query.filter(
            and_(
                Technology.name == dup.name,
                Technology.project_id == dup.project_id
            )
        ).order_by(Technology.updated_at.desc(), Technology.created_at.desc()).all()
        
        print("  📦 {} (Project ID: {}) - {} bản ghi".format(
            dup.name, dup.project_id, len(duplicate_records)))
        
        if len(duplicate_records) > 1:
            # Giữ lại record mới nhất (có updated_at hoặc created_at mới nhất)
            keep_record = duplicate_records[0]
            remove_records = duplicate_records[1:]
            
            # Merge thông tin từ các record cũ vào record mới nhất
            for old_record in remove_records:
                # Cập nhật thông tin nếu record cũ có thông tin mà record mới không có
                if not keep_record.version and old_record.version:
                    keep_record.version = old_record.version
                if not keep_record.category and old_record.category:
                    keep_record.category = old_record.category
                if not keep_record.description and old_record.description:
                    keep_record.description = old_record.description
                if not keep_record.vendor and old_record.vendor:
                    keep_record.vendor = old_record.vendor
                if not keep_record.notes and old_record.notes:
                    keep_record.notes = old_record.notes
            
            # Cập nhật timestamp
            keep_record.updated_at = datetime.utcnow()
            
            print("    ✅ Giữ lại ID {}, xóa {} bản ghi".format(
                keep_record.id, len(remove_records)))
            
            # Xóa các record trùng lặp
            for record in remove_records:
                db.session.delete(record)
                fixed_count += 1
    
    try:
        db.session.commit()
        print("✅ Đã xóa thành công {} bản ghi trùng lặp".format(fixed_count))
        return True
    except Exception as e:
        db.session.rollback()
        print("❌ Lỗi khi xóa duplicates: {}".format(str(e)))
        return False

def verify_no_duplicates():
    """Verify that no duplicates remain"""
    print("\n🔍 Kiểm tra lại duplicates...")
    
    remaining_duplicates = db.session.query(
        Technology.name,
        Technology.project_id,
        func.count(Technology.id).label('count')
    ).group_by(
        Technology.name,
        Technology.project_id
    ).having(func.count(Technology.id) > 1)
    
    duplicates = remaining_duplicates.all()
    
    if duplicates:
        print("⚠️ Vẫn còn {} nhóm duplicates:".format(len(duplicates)))
        for dup in duplicates:
            print("  - {} (Project ID: {}): {} bản ghi".format(
                dup.name, dup.project_id, dup.count))
        return False
    else:
        print("✅ Không còn duplicates!")
        return True

def main():
    """Main function"""
    print("🚀 SỬA CHỮA DUPLICATES CHO UNIQUE CONSTRAINT")
    print("=" * 60)
    
    with app.app_context():
        # Step 1: Fix duplicates
        if find_and_fix_duplicates():
            # Step 2: Verify
            if verify_no_duplicates():
                print("\n🎉 HOÀN THÀNH! Có thể áp dụng unique constraint.")
                print("\nBây giờ có thể chạy:")
                print("flask db upgrade")
            else:
                print("\n❌ Vẫn còn duplicates. Cần kiểm tra thủ công.")
        else:
            print("\n❌ Không thể sửa duplicates.")

if __name__ == "__main__":
    main()