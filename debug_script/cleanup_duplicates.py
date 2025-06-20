#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to clean up duplicate technology components in the database
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from app import app, db
from models import Technology, Project
from sqlalchemy import func, and_

def find_duplicates():
    """Find duplicate technology entries"""
    print("🔍 Đang tìm kiếm dữ liệu trùng lặp...")
    
    # Query để tìm duplicates dựa trên name, project_id, và category
    duplicates_query = db.session.query(
        Technology.name,
        Technology.project_id,
        Technology.category,
        func.count(Technology.id).label('count')
    ).group_by(
        Technology.name,
        Technology.project_id,
        Technology.category
    ).having(func.count(Technology.id) > 1)
    
    duplicates = duplicates_query.all()
    
    print("📊 Tìm thấy {} nhóm dữ liệu trùng lặp:".format(len(duplicates)))
    
    total_duplicate_records = 0
    for dup in duplicates:
        total_duplicate_records += dup.count - 1  # Keep one, remove others
        print("  - {} (Project ID: {}, Category: {}): {} bản ghi".format(
            dup.name, dup.project_id, dup.category, dup.count))
    
    print("📈 Tổng cộng có {} bản ghi trùng lặp cần xóa".format(total_duplicate_records))
    return duplicates

def cleanup_duplicates(duplicates, dry_run=True):
    """Clean up duplicate entries"""
    prefix = "[DRY RUN] " if dry_run else ""
    print("\n🧹 {}Đang dọn dẹp dữ liệu trùng lặp...".format(prefix))
    
    removed_count = 0
    
    for dup in duplicates:
        # Find all records for this duplicate group
        duplicate_records = Technology.query.filter(
            and_(
                Technology.name == dup.name,
                Technology.project_id == dup.project_id,
                Technology.category == dup.category
            )
        ).order_by(Technology.created_at.asc()).all()  # Keep the oldest one
        
        # Keep the first record, remove the rest
        records_to_remove = duplicate_records[1:]
        
        print("  📦 {} - Giữ lại 1, xóa {} bản ghi".format(dup.name, len(records_to_remove)))
        
        if not dry_run:
            for record in records_to_remove:
                db.session.delete(record)
                removed_count += 1
    
    if not dry_run:
        try:
            db.session.commit()
            print("✅ Đã xóa thành công {} bản ghi trùng lặp".format(removed_count))
        except Exception as e:
            db.session.rollback()
            print("❌ Lỗi khi xóa dữ liệu: {}".format(str(e)))
            return False
    else:
        total_to_remove = sum(len(Technology.query.filter(and_(
            Technology.name == dup.name,
            Technology.project_id == dup.project_id,
            Technology.category == dup.category
        )).all()) - 1 for dup in duplicates)
        print("🔍 [DRY RUN] Sẽ xóa {} bản ghi".format(total_to_remove))
    
    return True

def update_categories():
    """Update and standardize category names"""
    print("\n🏷️ Đang cập nhật và chuẩn hóa category...")
    
    # Category mapping for standardization
    category_updates = {
        'Frontend Framework': 'Frontend',
        'Programming Language': 'Language',
        'UI Library': 'Frontend',
        'Build Tool': 'DevOps',
        'Web Server': 'Infrastructure',
        'Backend Framework': 'Backend',
        'API Gateway': 'Backend',
        'Authentication': 'Security',
        'File Storage': 'Storage',
        'Search Engine': 'Database',
        'Load Balancer': 'Infrastructure',
        'Real-time Streaming': 'Communication',
        'Database Tool': 'Database',
        'Application Server': 'Infrastructure',
        'CI/CD': 'DevOps',
        'Logging': 'Monitoring',
        'Payment Service': 'External Service',
        'Email Service': 'External Service',
        'Analytics': 'Monitoring',
        'External API': 'External Service'
    }
    
    updated_count = 0
    
    for old_category, new_category in category_updates.items():
        components = Technology.query.filter_by(category=old_category).all()
        if components:
            print("  🔄 Cập nhật '{}' → '{}' ({} bản ghi)".format(
                old_category, new_category, len(components)))
            for component in components:
                component.category = new_category
                updated_count += 1
    
    # Update None/null categories
    null_components = Technology.query.filter(Technology.category.is_(None)).all()
    if null_components:
        print("  🔄 Cập nhật {} bản ghi không có category".format(len(null_components)))
        for component in null_components:
            tech_name = component.name.lower()
            
            # Auto-categorize based on technology name
            if any(tech in tech_name for tech in ['react', 'vue', 'angular', 'jquery', 'bootstrap', 'css', 'html']):
                component.category = 'Frontend'
            elif any(tech in tech_name for tech in ['node', 'express', 'django', 'flask', 'spring', 'laravel', 'asp.net', 'blazor']):
                component.category = 'Backend'
            elif any(tech in tech_name for tech in ['mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'elasticsearch']):
                component.category = 'Database'
            elif any(tech in tech_name for tech in ['docker', 'kubernetes', 'jenkins', 'gitlab', 'nginx', 'apache']):
                component.category = 'DevOps'
            elif any(tech in tech_name for tech in ['python', 'java', 'javascript', 'php', 'c#', 'go', 'typescript']):
                component.category = 'Language'
            elif any(tech in tech_name for tech in ['jwt', 'oauth', 'auth', 'security']):
                component.category = 'Security'
            else:
                component.category = 'Other'
            
            updated_count += 1
    
    try:
        db.session.commit()
        print("✅ Đã cập nhật {} category".format(updated_count))
    except Exception as e:
        db.session.rollback()
        print("❌ Lỗi khi cập nhật category: {}".format(str(e)))
        return False
    
    return True

def optimize_database():
    """Optimize database by updating indexes and cleaning up"""
    print("\n⚡ Đang tối ưu hóa database...")
    
    try:
        # Update statistics
        db.engine.execute("ANALYZE TABLE technology")
        db.engine.execute("ANALYZE TABLE project")
        db.engine.execute("ANALYZE TABLE manager")
        print("✅ Đã cập nhật thống kê database")
    except Exception as e:
        print("⚠️ Không thể cập nhật thống kê: {}".format(str(e)))
    
    return True

def show_summary():
    """Show database summary after cleanup"""
    print("\n📊 TỔNG KẾT SAU KHI DỌN DẸP:")
    print("=" * 50)
    
    # Count total records
    total_components = Technology.query.count()
    total_projects = Project.query.count()
    
    print("📦 Tổng số components: {}".format(total_components))
    print("📁 Tổng số projects: {}".format(total_projects))
    
    # Count by category
    category_counts = db.session.query(
        Technology.category,
        func.count(Technology.id).label('count')
    ).group_by(Technology.category).order_by(func.count(Technology.id).desc()).all()
    
    print("\n🏷️ Phân bố theo category:")
    for category, count in category_counts:
        print("  - {}: {}".format(category or 'Unknown', count))
    
    # Check for remaining duplicates
    remaining_duplicates = db.session.query(
        Technology.name,
        Technology.project_id,
        Technology.category,
        func.count(Technology.id).label('count')
    ).group_by(
        Technology.name,
        Technology.project_id,
        Technology.category
    ).having(func.count(Technology.id) > 1).count()
    
    print("\n🔍 Số nhóm trùng lặp còn lại: {}".format(remaining_duplicates))
    
    return total_components

def main():
    """Main cleanup function"""
    print("🚀 BẮT ĐẦU DỌN DẸP DATABASE")
    print("=" * 50)
    
    with app.app_context():
        # Step 1: Find duplicates
        duplicates = find_duplicates()
        
        if not duplicates:
            print("✅ Không tìm thấy dữ liệu trùng lặp!")
        else:
            # Step 2: Ask for confirmation
            print("\n❓ Bạn có muốn xóa {} nhóm dữ liệu trùng lặp không?".format(len(duplicates)))
            print("1. Có - Xóa ngay (y)")
            print("2. Không - Chỉ xem thử (n)")
            print("3. Dry run - Xem sẽ xóa gì (d)")
            
            choice = input("Lựa chọn (y/n/d): ").lower().strip()
            
            if choice == 'y':
                cleanup_duplicates(duplicates, dry_run=False)
            elif choice == 'd':
                cleanup_duplicates(duplicates, dry_run=True)
            else:
                print("⏭️ Bỏ qua xóa dữ liệu trùng lặp")
        
        # Step 3: Update categories
        update_categories()
        
        # Step 4: Optimize database
        optimize_database()
        
        # Step 5: Show summary
        final_count = show_summary()
        
        print("\n🎉 HOÀN THÀNH! Database hiện có {} components".format(final_count))

if __name__ == "__main__":
    main()