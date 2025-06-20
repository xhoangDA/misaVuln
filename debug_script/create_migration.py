from flask import Flask
from flask_migrate import Migrate, upgrade, init, migrate
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ntlong:new_password@10.1.36.248/project_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate_instance = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        # Create migration
        migrate(message='fix_foreign_key_relationships')
        print("Migration created successfully!")