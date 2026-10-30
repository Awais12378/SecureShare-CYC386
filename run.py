#!/usr/bin/env python3
"""
SecureShare - Secure File Sharing Platform
Main application entry point
"""
import os
from app import create_app

# Get configuration from environment variable, default to development
config_name = os.environ.get('FLASK_ENV', 'development')

app = create_app(config_name)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
