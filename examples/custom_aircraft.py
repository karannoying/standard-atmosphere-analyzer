"""
Custom Aircraft Configuration Examples
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.atmosphere_model import StandardAtmosphere
from src.aircraft_performance import AircraftPerformance
from src.utils import load_aircraft_config, save_aircraft_config

def create_custom_aircraft():
    """Create and save a custom aircraft configuration"""
    
    # Define a custom aircraft (e.g., a large cargo plane)
    custom_aircraft = {
        "antonov_an124": {
            "name": "Antonov An-124 Ruslan",
            "wing_area": 628.0,      # m²
            "mass": 405000.0,        # kg (maximum takeoff weight)
            "max_lift_coeff": 2.2,
            "zero_lift_drag": 0.018,
            "oswald_efficiency": 0.82,
            "aspect_ratio": 8.8,
            "description": "Large strategic airlift cargo aircraft"
        }
    }
    
    # Save to file
    save_aircraft_config(custom_aircraft, 'custom_antonov.json')
    print("Custom aircraft configuration saved as 'custom_antonov.json'")
    
    return custom_aircraft

def load_and_use_custom_aircraft():
    """Load custom aircraft and analyze performance"""
    
    # Load predefined aircraft configurations
    config = load_aircraft_config('data/sample_aircraft.json')
    
    print("Available aircraft types:")
    for aircraft_type, params in config['aircraft_types'].items():
        print(f"  - {params['name']} ({aircraft_type})")
    
    # Create atmosphere and performance models
    atm = StandardAtmosphere()
    performance = AircraftPerformance(atm)
    
    # Analyze different aircraft at the same conditions
    altitude = 11000  # meters (typical cruise altitude)
    velocity = 230    # m/s
    
    print(f"\nPerformance comparison at {altitude:,} m, {velocity} m/s:")
    print("-" * 70)
    print(f"{'Aircraft':<20} {'Thrust (kN)':<12} {'L/D Ratio':<10} {'Stall (m/s)':<12}")
    print("-" * 70)
    
    for aircraft_type, params in config['aircraft_types'].items():
        # Set aircraft parameters
        performance.set_aircraft_parameters(**params)
        
        # Calculate performance
        perf = performance.performance_at_condition(altitude, velocity)
        
        print(f"{params['name']:<20} {perf['required_thrust']/1000:<12.2f} "
              f"{perf['lift_to_drag_ratio']:<10.2f} {perf['stall_speed']:<12.2f}")

def create_ultralight_config():
    """Create configuration for an ultralight aircraft"""
    
    ultralight = {
        "ultralight_sport": {
            "name": "Ultralight Sport Aircraft",
            "wing_area": 12.5,       # m²
            "mass": 350.0,           # kg
            "max_lift_coeff": 1.4,
            "zero_lift_drag": 0.035,
            "oswald_efficiency": 0.70,
            "aspect_ratio": 6.5,
            "description": "Lightweight recreational aircraft"
        }
    }
    
    # Save configuration
    save_aircraft_config(ultralight, 'ultralight_config.json')
    
    # Demonstrate usage
    atm = StandardAtmosphere()
    performance = AircraftPerformance(atm)
    performance.set_aircraft_parameters(**ultralight["ultralight_sport"])
    
    # Low altitude performance
    altitude = 1000  # meters
    velocity = 40    # m/s
    
    perf = performance.performance_at_condition(altitude, velocity)
    
    print(f"\nUltralight Aircraft at {altitude:,} m, {velocity} m/s:")
    print(f"  Required Thrust: {perf['required_thrust']:.1f} N")
    print(f"  Lift-to-Drag Ratio: {perf['lift_to_drag_ratio']:.2f}")
    print(f"  Stall Speed: {perf['stall_speed']:.2f} m/s")
    
    return ultralight

if __name__ == "__main__":
    print("=== Custom Aircraft Configuration Examples ===\n")
    
    # Example 1: Create custom aircraft
    create_custom_aircraft()
    
    # Example 2: Compare different aircraft
    load_and_use_custom_aircraft()
    
    # Example 3: Ultralight aircraft
    create_ultralight_config()