"""
AirLogger backend application package.
"""
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global database session
Session = None


def create_app(testing=False):
    """Create and configure Flask application."""
    app = Flask(__name__)
    
    # Configuration
    app.config['TESTING'] = testing
    
    if testing:
        app.config['DATABASE_URL'] = 'sqlite:///:memory:'
    else:
        app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'sqlite:///./airlogger.db')
    
    # Initialize database
    from app.models import Base
    engine = create_engine(app.config['DATABASE_URL'])
    Base.metadata.create_all(engine)
    
    # Create session factory
    global Session
    Session = sessionmaker(bind=engine)
    
    # Register blueprints
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app