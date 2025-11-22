"""
Basic usage examples for the Standard Atmosphere Analyzer
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.atmosphere_model import StandardAtmosphere
from src.aircraft_performance import AircraftPerformance
from src.visualization import AtmosphereVisualizer

def example_basic_atmosphere():
    """Basic example of using the atmosphere model"""
    print("=== Basic Atmosphere Model Example ===")
    
    # Create atmosphere model
    atm = StandardAtmosphere()
    
    # Get properties at different altitudes
    altitudes = [0, 5000, 10000, 15000]  # meters
    
    for alt in altitudes:
        props = atm.get_atmospheric_properties(alt)
        print(f"\nAltitude: {alt:,} m ({alt/1000:.1f} km)")
        print(f"  Temperature: {props['temperature_c']:.2f}°C")
        print(f"  Pressure: {props['pressure']/1000:.2f} kPa")
        print(f"  Density: {props['density']:.4f} kg/m³")
        print(f"  Speed of Sound: {props['speed_of_sound']:.2f} m/s")

def example_aircraft_performance():
    """Basic example of aircraft performance calculations"""
    print("\n=== Aircraft Performance Example ===")
    
    atm = StandardAtmosphere()
    performance = AircraftPerformance(atm)
    
    # Analyze at cruise conditions
    altitude = 10000  # meters
    velocity = 250    # m/s
    
    perf = performance.performance_at_condition(altitude, velocity)
    
    print(f"\nPerformance at {altitude:,} m, {velocity} m/s:")
    print(f"  Lift Coefficient (CL): {perf['lift_coefficient']:.4f}")
    print(f"  Drag Coefficient (CD): {perf['drag_coefficient']:.4f}")
    print(f"  Lift Force: {perf['lift_force']/1000:.2f} kN")
    print(f"  Drag Force: {perf['drag_force']/1000:.2f} kN")
    print(f"  Required Thrust: {perf['required_thrust']/1000:.2f} kN")
    print(f"  Lift-to-Drag Ratio: {perf['lift_to_drag_ratio']:.2f}")
    print(f"  Stall Speed: {perf['stall_speed']:.2f} m/s")

def example_visualization():
    """Example of generating visualizations"""
    print("\n=== Visualization Example ===")
    
    atm = StandardAtmosphere()
    visualizer = AtmosphereVisualizer()
    
    # Generate altitude profile
    profile = atm.generate_altitude_profile(max_altitude=20000, step=500)
    
    # Create and save plot
    fig = visualizer.plot_atmospheric_properties(profile)
    fig.savefig('atmosphere_profile.png', dpi=300, bbox_inches='tight')
    print("Atmosphere profile saved as 'atmosphere_profile.png'")

if __name__ == "__main__":
    example_basic_atmosphere()
    example_aircraft_performance()
    example_visualization()
