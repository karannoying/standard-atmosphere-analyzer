"""
Data files for Standard Atmosphere Analyzer.

This package contains:
- sample_aircraft.json: Predefined aircraft configurations
- Additional data files for atmospheric models and performance analysis
"""

import os

DATA_PATH = os.path.dirname(__file__)

def get_data_path(filename):
    """Get absolute path to data file."""
    return os.path.join(DATA_PATH, filename)

def list_data_files():
    """List available data files."""
    files = []
    for file in os.listdir(DATA_PATH):
        if file.endswith('.json') and file != '__init__.py':
            files.append(file)
    return files

__all__ = ['get_data_path', 'list_data_files']
