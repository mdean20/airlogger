"""
Main entry point for AirLogger backend application.
"""
import os
import logging
from dotenv import load_dotenv
from app import create_app

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Suppress noisy loggers
logging.getLogger('urllib3').setLevel(logging.WARNING)

# Create Flask app
app = create_app()

if __name__ == "__main__":
    # Get configuration from environment
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    # Log startup information
    logging.info(f"Starting AirLogger backend on port {port}")
    logging.info(f"Debug mode: {debug}")
    
    # Run the application
    app.run(
        host='0.0.0.0',  # Accessible from any IP (needed for Tailscale)
        port=port,
        debug=debug
    )