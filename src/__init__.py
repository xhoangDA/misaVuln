from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from src.config import Config
from flask import render_template

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"   # Thêm dòng này!
    )
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from src.routes.project_routes import project_bp
    from src.routes.manager_routes import manager_bp
    from src.routes.component_routes import component_bp
    from src.routes.cve_routes import cve_bp
    app.register_blueprint(project_bp)
    app.register_blueprint(manager_bp)
    app.register_blueprint(component_bp)
    app.register_blueprint(cve_bp)
    
    # Register Jinja2 filters
    from src.utils.helpers import min_filter
    app.jinja_env.filters['min'] = min_filter
    
    def escapejs_filter(value):
        """Escape string for safe embedding in JS (simple version)"""
        if not isinstance(value, str):
            value = str(value)
        replacements = [
            ('\\', '\\\\'),
            ('"', '\\"'),
            ("'", "\\'"),
            ('\n', '\\n'),
            ('\r', '\\r'),
            ('</', '<\/'),
            ('\u2028', '\\u2028'),
            ('\u2029', '\\u2029'),
        ]
        for old, new in replacements:
            value = value.replace(old, new)
        return value

    # Register filter with Jinja2
    app.jinja_env.filters['escapejs'] = escapejs_filter

    # Add root route to render index.html
    @app.route('/')
    def index():
        return render_template('index.html')

    return app
