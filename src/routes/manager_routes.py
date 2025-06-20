# Manager-related routes
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, make_response
from src.models import Manager
from src import db
import csv, io
from src.utils.cve_scanner import CVEScanner, check_component_vulnerability

manager_bp = Blueprint('manager', __name__)

@manager_bp.route('/managers', methods=['GET', 'POST'])
def manage_managers():
    if request.method == 'POST':
        # Create a new manager
        data = request.get_json()
        new_manager = Manager(
            name=data['name'],
            email=data['email'],
            password=data['password'],  # Ensure password is hashed in the model
            phone=data['phone'],
            address=data['address'],
            role=data['role']
        )
        db.session.add(new_manager)
        db.session.commit()
        return jsonify({'message': 'Manager created', 'manager': new_manager.serialize()}), 201

    # GET method: return HTML for browser, JSON for API
    managers = Manager.query.all()
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify({'managers': [manager.serialize() for manager in managers]})
    return render_template('managers.html', managers=managers)

@manager_bp.route('/managers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manager_operations(id):
    manager = Manager.query.get_or_404(id)

    if request.method == 'PUT':
        # Update manager details
        data = request.get_json()
        manager.name = data['name']
        manager.email = data['email']
        manager.phone = data['phone']
        manager.address = data['address']
        manager.role = data['role']
        db.session.commit()
        return jsonify({'message': 'Manager updated', 'manager': manager.serialize()})

    if request.method == 'DELETE':
        # Delete the manager
        db.session.delete(manager)
        db.session.commit()
        return jsonify({'message': 'Manager deleted'})

    # GET method: return manager details
    return jsonify({'manager': manager.serialize()})

@manager_bp.route('/managers/import', methods=['POST'])
def import_managers():
    # ...existing code from app.py...
    pass

@manager_bp.route('/managers/sample-csv')
def download_sample_managers_csv():
    # ...existing code from app.py...
    pass
