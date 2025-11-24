"""
Standard Atmosphere Analyzer - A comprehensive tool for atmospheric modeling and aircraft performance analysis.

This package provides:
- International Standard Atmosphere (ISA) model calculations
- Aircraft performance analysis (lift, drag, thrust requirements)
- Professional visualization capabilities
- Educational tools for aerospace engineering

Author: Kumar Karan Bohidar
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Kumar Karan Bohidar"
__email__ = "kumar.25bas10049@vitbhopal.ac.in"

# Import key classes to make them available at package level
from .atmosphere_model import StandardAtmosphere
from .aircraft_performance import AircraftPerformance
from .visualization import AtmosphereVisualizer
from .utils import (
    load_aircraft_config,
    save_aircraft_config,
    validate_altitude,
    validate_velocity,
    meters_to_feet,
    feet_to_meters,
    mps_to_knots,
    knots_to_mps,
    calculate_mach_number,
    calculate_dynamic_pressure,
    UnitConverter
)

# Define what gets imported with "from src import *"
__all__ = [
    'StandardAtmosphere',
    'AircraftPerformance', 
    'AtmosphereVisualizer',
    'load_aircraft_config',
    'save_aircraft_config',
    'validate_altitude',
    'validate_velocity',
    'meters_to_feet',
    'feet_to_meters', 
    'mps_to_knots',
    'knots_to_mps',
    'calculate_mach_number',
    'calculate_dynamic_pressure',
    'UnitConverter'
]

# Package-level configuration
PACKAGE_CONFIG = {
    'max_altitude': 50000,  # meters
    'min_altitude': 0,      # meters  
    'default_step': 100,    # meters
    'supported_units': ['metric', 'imperial']
}

def get_version():
    """Return the current version of the package."""
    return __version__

def get_authors():
    """Return package author information."""
    return {
        'author': __author__,
        'email': __email__,
        'version': __version__
    }

def print_welcome():
    """Print a welcome message when the package is imported."""
    print(f"🚀 Standard Atmosphere Analyzer v{__version__}")
    print("   International Standard Atmosphere Model & Aircraft Performance Analysis")
    print("   For educational and research purposes")
    print()
