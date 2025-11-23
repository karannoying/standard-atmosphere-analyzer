"""
Test suite for Standard Atmosphere Analyzer.

This package contains unit tests for:
- atmosphere_model.py
- aircraft_performance.py  
- visualization.py
- utils.py

Run tests with: python -m pytest tests/
"""

import os
import sys

# Add the src directory to Python path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Test configuration
TEST_CONFIG = {
    'test_altitudes': [0, 5000, 10000, 15000, 20000],
    'test_velocities': [100, 200, 250, 300],
    'tolerance': 1e-6  # For floating point comparisons
}

# Import test modules to make them discoverable
from .test_atmosphere import TestStandardAtmosphere
from .test_performance import TestAircraftPerformance
from .test_visualization import TestVisualization
from .test_utils import TestUtils

__all__ = [
    'TestStandardAtmosphere',
    'TestAircraftPerformance', 
    'TestVisualization',
    'TestUtils',
    'TEST_CONFIG'
]

def run_all_tests():
    """Convenience function to run all tests."""
    import pytest
    pytest.main([os.path.dirname(__file__), '-v'])