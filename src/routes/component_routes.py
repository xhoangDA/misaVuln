# Component/Technology-related routes
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from src.models import Technology, Project, Manager
from src import db
import pandas as pd, re, io
from src.utils.cve_scanner import CVEScanner, check_component_vulnerability
from datetime import datetime
from sqlalchemy import func

component_bp = Blueprint('component', __name__)

@component_bp.route('/components', methods=['GET', 'POST'])
def manage_components():
    if request.method == 'POST':
        try:
            data = request.json
            existing_component = Technology.query.filter_by(
                name=data['name'],
                project_id=data.get('project_id')
            ).first()
            if existing_component:
                existing_component.version = data.get('version')
                existing_component.category = data.get('category')
                existing_component.description = data.get('description')
                existing_component.vendor = data.get('vendor')
                existing_component.notes = data.get('notes')
                existing_component.updated_at = datetime.utcnow()
                db.session.commit()
                return jsonify({
                    'message': 'Technology component updated successfully',
                    'component': {
                        'id': existing_component.id,
                        'name': existing_component.name,
                        'version': existing_component.version,
                        'category': existing_component.category,
                        'description': existing_component.description,
                        'project_id': existing_component.project_id,
                        'project_name': existing_component.project.project_name if existing_component.project else None,
                        'manager_name': existing_component.project.manager.name if existing_component.project and existing_component.project.manager else None,
                        'vendor': existing_component.vendor,
                        'notes': existing_component.notes,
                        'created_at': existing_component.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'updated_at': existing_component.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                    }
                }), 200
            else:
                new_component = Technology(
                    name=data['name'],
                    version=data.get('version'),
                    category=data.get('category'),
                    description=data.get('description'),
                    project_id=data.get('project_id'),
                    vendor=data.get('vendor'),
                    notes=data.get('notes')
                )
                db.session.add(new_component)
                db.session.commit()
                return jsonify({
                    'message': 'Technology component created successfully',
                    'component': {
                        'id': new_component.id,
                        'name': new_component.name,
                        'version': new_component.version,
                        'category': new_component.category,
                        'description': new_component.description,
                        'project_id': new_component.project_id,
                        'project_name': new_component.project.project_name if new_component.project else None,
                        'manager_name': new_component.project.manager.name if new_component.project and new_component.project.manager else None,
                        'vendor': new_component.vendor,
                        'notes': new_component.notes,
                        'created_at': new_component.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'updated_at': new_component.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                    }
                }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    # GET: Render components.html with context
    components = Technology.query.options(
        db.joinedload(Technology.project).joinedload(Project.manager)
    ).all()
    projects = Project.query.all()
    # Popular technologies
    popular_techs_query = db.session.query(
        Technology.name,
        func.count(Technology.id).label('count')
    ).group_by(Technology.name).order_by(func.count(Technology.id).desc()).limit(10)
    popular_techs = list(popular_techs_query.all())
    # Tech stats by category
    tech_stats = {}
    category_counts = db.session.query(
        Technology.category,
        func.count(Technology.id).label('count')
    ).filter(Technology.category.isnot(None)).group_by(Technology.category).all()
    for category, count in category_counts:
        if category:
            tech_stats[category] = count
    # Add unmapped components
    unmapped_components = Technology.query.filter(Technology.category.is_(None)).all()
    for component in unmapped_components:
        tech_name = component.name.lower()
        if any(tech in tech_name for tech in ['react', 'vue', 'angular', 'jquery', 'bootstrap']):
            category = 'Frontend'
        elif any(tech in tech_name for tech in ['node', 'express', 'django', 'flask', 'spring', 'laravel']):
            category = 'Backend'
        elif any(tech in tech_name for tech in ['mysql', 'postgresql', 'mongodb', 'redis', 'sqlite']):
            category = 'Database'
        elif any(tech in tech_name for tech in ['docker', 'kubernetes', 'jenkins', 'gitlab', 'nginx']):
            category = 'DevOps'
        elif any(tech in tech_name for tech in ['python', 'java', 'javascript', 'php', 'c#', 'go']):
            category = 'Language'
        else:
            category = 'Other'
        if category not in tech_stats:
            tech_stats[category] = 0
        tech_stats[category] += 1
    return render_template('components.html',
                          components=components,
                          projects=projects,
                          tech_stats=tech_stats,
                          popular_techs=popular_techs)

@component_bp.route('/components/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def component_operations(id):
    component = Technology.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({
            'id': component.id,
            'name': component.name,
            'version': component.version,
            'category': component.category,
            'description': component.description,
            'project_id': component.project_id,
            'project_name': component.project.project_name if component.project else None,
            'manager_name': component.project.manager.name if component.project and component.project.manager else None,
            'vendor': component.vendor,
            'notes': component.notes,
            'created_at': component.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': component.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    elif request.method == 'PUT':
        try:
            data = request.json
            component.name = data.get('name', component.name)
            component.version = data.get('version', component.version)
            component.category = data.get('category', component.category)
            component.description = data.get('description', component.description)
            component.project_id = data.get('project_id', component.project_id)
            component.vendor = data.get('vendor', component.vendor)
            component.notes = data.get('notes', component.notes)
            db.session.commit()
            return jsonify({
                'message': 'Component updated successfully',
                'component': {
                    'id': component.id,
                    'name': component.name,
                    'version': component.version,
                    'category': component.category,
                    'description': component.description,
                    'project_id': component.project_id,
                    'project_name': component.project.project_name if component.project else None,
                    'manager_name': component.project.manager.name if component.project and component.project.manager else None,
                    'vendor': component.vendor,
                    'notes': component.notes,
                    'created_at': component.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'updated_at': component.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    elif request.method == 'DELETE':
        try:
            db.session.delete(component)
            db.session.commit()
            return jsonify({'message': 'Component deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

@component_bp.route('/components/import_csv', methods=['POST'])
def import_single_csv():
    try:
        if 'csv_file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['csv_file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        file_content = file.read().decode('utf-8')
        df = pd.read_csv(io.StringIO(file_content), skiprows=4, header=0)
        df.columns = df.columns.str.strip()
        expected_columns = ['Nội dung', 'Công nghệ sử dụng', 'Phiên bản', 'Ngày cập nhật']
        if not all(col in df.columns for col in expected_columns):
            return jsonify({'error': 'CSV must have columns: {}'.format(", ".join(expected_columns))}), 400
        project_name = None
        for index, row in df.iterrows():
            content = str(row['Nội dung']) if pd.notna(row['Nội dung']) else ''
            if 'Tên webapp:' in content:
                match = re.search(r'Tên webapp:\s*([^\n\r]+)', content)
                if match:
                    project_name = match.group(1).strip()
                    break
        if not project_name:
            project_name = file.filename.replace('.csv', '').replace('[', '').replace(']', '').strip()
        project_code = re.sub(r'[^A-Z0-9]', '', project_name.upper())[:10]
        key = project_code[:5] if project_code else 'PROJ'
        project = Project.query.filter(
            (Project.project_name == project_name) |
            (Project.key == key) |
            (Project.project_code == project_code)
        ).first()
        if not project:
            default_manager = Manager.query.first()
            if not default_manager:
                return jsonify({'error': 'No manager found. Please create a manager first.'}), 400
            counter = 1
            original_key = key
            original_project_code = project_code
            while Project.query.filter(
                (Project.key == key) | (Project.project_code == project_code)
            ).first():
                key = (original_key + str(counter))[:5] if original_key else ('PROJ' + str(counter))[:5]
                project_code = (original_project_code + str(counter))[:10] if original_project_code else ('PROJ' + str(counter))[:10]
                counter += 1
            project = Project(
                project_code=project_code,
                key=key,
                project_name=project_name,
                manager_id=default_manager.id
            )
            db.session.add(project)
            db.session.commit()
        project_id = project.id
        imported_count = 0
        errors = []
        vendor_mapping = {
            'jquery': 'jQuery Foundation',
            'blazor': 'Microsoft',
            'javascript': 'ECMA International',
            'c#': 'Microsoft',
            'msbuild': 'Microsoft',
            'cloudflare': 'Cloudflare Inc.',
            'iis': 'Microsoft',
            'k8s': 'Kubernetes',
            'kubernetes': 'Kubernetes',
            '.net core': 'Microsoft',
            'netcore': 'Microsoft',
            'jwt': 'OpenID Foundation',
            'api key': 'OpenID Foundation',
            'redis': 'Redis Ltd.',
            'fileshare': 'Microsoft',
            'nginx': 'NGINX Inc.',
            'sqlserver': 'Microsoft',
            'sql server': 'Microsoft',
            'jenkins': 'CloudBees',
            'elasticsearch': 'Elastic N.V.',
            'mobifone': 'MobiFone Corporation'
        }
        category_mapping = {
            'Framework / Library': 'Frontend Framework',
            'Ngôn ngữ lập trình': 'Programming Language',
            'Thư viện UI/UX': 'UI Library',
            'Công cụ build/deploy': 'Build Tool',
            'CDN cache': 'CDN',
            'Web Server': 'Web Server',
            'Framework': 'Backend Framework',
            'API Gateway': 'API Gateway',
            'Phương thức xác thực (authentication/authorization)': 'Authentication',
            'Cache': 'Cache',
            'Queue': 'Queue',
            'Quản lý FileUpload/ FileStorage': 'File Storage',
            'Search Engine': 'Search Engine',
            'LoadBalance': 'Load Balancer',
            'Streaming real-time': 'Real-time Streaming',
            'Loại database': 'Database',
            'Công cụ quản lý database': 'Database Tool',
            'Công cụ điều phối ứng dụng': 'Application Server',
            'CI': 'CI/CD',
            'CD': 'CI/CD',
            'Công cụ lưu trữ log': 'Logging',
            'Dịch vụ thanh toán': 'Payment Service',
            'Dịch vụ Email': 'Email Service',
            'Dịch vụ phân tích và tracking': 'Analytics',
            'Các API bên ngoài khác': 'External API'
        }
        for index, row in df.iterrows():
            try:
                category_raw = str(row['Nội dung']).strip() if pd.notna(row['Nội dung']) else ''
                name = str(row['Công nghệ sử dụng']).strip() if pd.notna(row['Công nghệ sử dụng']) else ''
                version = str(row['Phiên bản']).strip() if pd.notna(row['Phiên bản']) and str(row['Phiên bản']).strip() != 'nan' else None
                if not category_raw or not name or name.lower() in ['không sử dụng', 'không', '']:
                    continue
                if any(skip_text in category_raw.lower() for skip_text in [
                    'front-end', 'back-end', 'cơ sở dữ liệu', 'hạ tầng', 'dịch vụ',
                    'thông tin chung', 'tên webapp', 'url:', 'người phụ trách'
                ]):
                    continue
                category_cleaned = category_raw.replace(':', '').strip()
                if category_cleaned.endswith(':'):
                    category_cleaned = category_cleaned[:-1].strip()
                category = category_mapping.get(category_cleaned, category_cleaned)
                if len(category) > 50:
                    category = category[:47] + '...'
                technologies = [tech.strip() for tech in name.split(',')]
                for tech in technologies:
                    if not tech or tech.lower() in ['không sử dụng', 'không']:
                        continue
                    if version and version != 'nan':
                        version = re.sub(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', '', version).strip()
                        if not version:
                            version = None
                    else:
                        version = None
                    existing_tech = Technology.query.filter_by(
                        project_id=project_id,
                        name=tech
                    ).first()
                    if existing_tech:
                        existing_tech.version = version
                        existing_tech.category = category
                        existing_tech.vendor = vendor_mapping.get(tech.lower())
                        existing_tech.updated_at = datetime.utcnow()
                        db.session.commit()
                        continue
                    new_tech = Technology(
                        name=tech,
                        version=version,
                        category=category,
                        vendor=vendor_mapping.get(tech.lower()),
                        project_id=project_id,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.session.add(new_tech)
                    imported_count += 1
            except Exception as e:
                db.session.rollback()
                errors.append('Row {}: {}'.format(index + 1, str(e)))
                continue
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to save data: {}'.format(str(e))}), 500
        message = 'Successfully imported {} technology components for project "{}"'.format(
            imported_count, project.project_name)
        if errors:
            message += '. {} errors occurred'.format(len(errors))
        return jsonify({
            'message': message,
            'imported_count': imported_count,
            'project_name': project.project_name,
            'project_id': project.id,
            'errors': errors[:10]
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Import failed: {}'.format(str(e))}), 500
