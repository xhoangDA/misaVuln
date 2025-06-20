from flask import Blueprint, request, jsonify, render_template, make_response
from src.models import db, Project, Manager
from datetime import datetime
import json

project_bp = Blueprint('project', __name__)

@project_bp.route('/projects', methods=['GET', 'POST'])
def manage_projects():
    if request.method == 'POST':
        try:
            data = request.get_json()
            new_project = Project(
                project_code=data['project_code'],
                key=data['key'],
                project_name=data['project_name'],
                manager_id=data['manager_id']
            )
            db.session.add(new_project)
            db.session.commit()
            return jsonify({'message': 'Project created successfully', 'id': new_project.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    projects = Project.query.all()
    managers = Manager.query.all()
    now = datetime.now()
    return render_template('projects.html', projects=projects, managers=managers, now=now)

@project_bp.route('/projects/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def project_operations(id):
    project = Project.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({
            'id': project.id,
            'project_code': project.project_code,
            'key': project.key,
            'project_name': project.project_name,
            'manager_id': project.manager_id
        })
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            project.project_code = data.get('project_code', project.project_code)
            project.key = data.get('key', project.key)
            project.project_name = data.get('project_name', project.project_name)
            if 'manager_id' in data:
                project.manager_id = data['manager_id']
            db.session.commit()
            return jsonify({'message': 'Project updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    elif request.method == 'DELETE':
        try:
            db.session.delete(project)
            db.session.commit()
            return jsonify({'message': 'Project deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

@project_bp.route('/get_project_info', methods=['GET'])
def get_project_info():
    project_id = request.args.get('project_id')
    if not project_id:
        return jsonify({'error': 'Missing project_id'}), 400
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    return jsonify({
        'project_name': project.project_name,
        'manager_name': project.manager.name if project.manager else None
    })

@project_bp.route('/projects/import', methods=['POST'])
def import_projects():
    try:
        if 'json_file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['json_file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        default_manager_id = request.form.get('manager_id', 1)
        file_content = file.read().decode('utf-8')
        projects_data = json.loads(file_content)
        if not isinstance(projects_data, list):
            return jsonify({'error': 'JSON file must contain an array of projects'}), 400
        imported_count = 0
        errors = []
        for index, project_data in enumerate(projects_data):
            try:
                if 'id' not in project_data or 'key' not in project_data or 'name' not in project_data:
                    errors.append(f'Project {index + 1}: Missing required fields (id, key, name)')
                    continue
                project_code = str(project_data['id']).strip()
                key = str(project_data['key']).strip()
                project_name = str(project_data['name']).strip()
                if not project_code or not key or not project_name:
                    errors.append(f'Project {index + 1}: Empty values for required fields')
                    continue
                existing_project = Project.query.filter(
                    (Project.project_code == project_code) | (Project.key == key)
                ).first()
                if existing_project:
                    errors.append(f'Project {index + 1}: Project with code "{project_code}" or key "{key}" already exists')
                    continue
                manager = Manager.query.get(default_manager_id)
                if not manager:
                    errors.append(f'Project {index + 1}: Manager with ID {default_manager_id} not found')
                    continue
                new_project = Project(
                    project_code=project_code,
                    key=key,
                    project_name=project_name,
                    manager_id=default_manager_id
                )
                db.session.add(new_project)
                imported_count += 1
            except Exception as e:
                errors.append(f'Project {index + 1}: {str(e)}')
        db.session.commit()
        message = f'Successfully imported {imported_count} projects'
        if errors:
            message += f'. {len(errors)} errors occurred'
        return jsonify({
            'message': message,
            'imported_count': imported_count,
            'errors': errors[:10]
        }), 200
    except json.JSONDecodeError as e:
        return jsonify({'error': f'Invalid JSON format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Import failed: {str(e)}'}), 500
