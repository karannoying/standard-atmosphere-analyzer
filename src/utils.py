"""
Utility functions for the Standard Atmosphere Analyzer
"""

import json
import numpy as np
from typing import Dict, Any, List

def load_aircraft_config(filepath: str) -> Dict[str, Any]:
    """
    Load aircraft configuration from JSON file
    
    Args:
        filepath: Path to JSON configuration file
        
    Returns:
        Dictionary containing aircraft parameters
    """
    try:
        with open(filepath, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Aircraft configuration file not found: {filepath}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in configuration file: {filepath}")

def save_aircraft_config(config: Dict[str, Any], filepath: str):
    """
    Save aircraft configuration to JSON file
    
    Args:
        config: Aircraft configuration dictionary
        filepath: Path to save the configuration
    """
    with open(filepath, 'w') as f:
        json.dump(config, f, indent=2)

def validate_altitude(altitude: float) -> bool:
    """
    Validate that altitude is within reasonable bounds
    
    Args:
        altitude: Altitude in meters
        
    Returns:
        True if valid, False otherwise
    """
    return 0 <= altitude <= 50000

def validate_velocity(velocity: float) -> bool:
    """
    Validate that velocity is within reasonable bounds
    
    Args:
        velocity: Velocity in m/s
        
    Returns:
        True if valid, False otherwise
    """
    return 0 < velocity <= 1000

def meters_to_feet(meters: float) -> float:
    """Convert meters to feet"""
    return meters * 3.28084

def feet_to_meters(feet: float) -> float:
    """Convert feet to meters"""
    return feet / 3.28084

def mps_to_knots(mps: float) -> float:
    """Convert meters per second to knots"""
    return mps * 1.94384

def knots_to_mps(knots: float) -> float:
    """Convert knots to meters per second"""
    return knots / 1.94384

def calculate_mach_number(velocity: float, speed_of_sound: float) -> float:
    """
    Calculate Mach number
    
    Args:
        velocity: Velocity in m/s
        speed_of_sound: Speed of sound in m/s
        
    Returns:
        Mach number
    """
    return velocity / speed_of_sound if speed_of_sound > 0 else 0

def calculate_dynamic_pressure(density: float, velocity: float) -> float:
    """
    Calculate dynamic pressure
    
    Args:
        density: Air density in kg/m³
        velocity: Velocity in m/s
        
    Returns:
        Dynamic pressure in Pa
    """
    return 0.5 * density * velocity**2

class UnitConverter:
    """Class for handling unit conversions"""
    
    @staticmethod
    def pressure_pa_to_inhg(pa: float) -> float:
        """Convert Pascals to inches of mercury"""
        return pa / 3386.389
    
    @staticmethod
    def pressure_pa_to_psi(pa: float) -> float:
        """Convert Pascals to PSI"""
        return pa / 6894.76
    
    @staticmethod
    def temperature_c_to_f(celsius: float) -> float:
        """Convert Celsius to Fahrenheit"""
        return celsius * 9/5 + 32
    
    @staticmethod
    def force_n_to_lbf(newtons: float) -> float:
        """Convert Newtons to pound-force"""
        return newtons / 4.44822
