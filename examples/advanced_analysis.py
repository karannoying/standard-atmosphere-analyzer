"""
Advanced analysis examples for the Standard Atmosphere Analyzer
"""

import sys
import os
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.atmosphere_model import StandardAtmosphere
from src.aircraft_performance import AircraftPerformance
from src.visualization import AtmosphereVisualizer

def advanced_performance_analysis():
    """Advanced performance analysis across multiple conditions"""
    print("=== Advanced Performance Analysis ===")
    
    atm = StandardAtmosphere()
    performance = AircraftPerformance(atm)
    
    # Analyze across a range of altitudes and velocities
    altitudes = np.linspace(0, 15000, 6)  # 0 to 15,000 meters
    velocities = [200, 250, 300]  # m/s
    
    print("\nPerformance Matrix:")
    print("Alt (m) | Vel (m/s) | Thrust (kN) | L/D Ratio | Stall (m/s)")
    print("-" * 60)
    
    for alt in altitudes:
        for vel in velocities:
            perf = performance.performance_at_condition(alt, vel)
            print(f"{alt:7.0f} | {vel:9.0f} | {perf['required_thrust']/1000:10.2f} | "
                  f"{perf['lift_to_drag_ratio']:9.2f} | {perf['stall_speed']:10.2f}")

def optimal_cruise_analysis():
    """Find optimal cruise conditions"""
    print("\n=== Optimal Cruise Analysis ===")
    
    atm = StandardAtmosphere()
    performance = AircraftPerformance(atm)
    
    # Find altitude with best L/D ratio at typical cruise speed
    altitudes = np.arange(5000, 13000, 500)
    cruise_speed = 250  # m/s
    
    best_altitude = 0
    best_LD_ratio = 0
    
    for alt in altitudes:
        perf = performance.performance_at_condition(alt, cruise_speed)
        if perf['lift_to_drag_ratio'] > best_LD_ratio:
            best_LD_ratio = perf['lift_to_drag_ratio']
            best_altitude = alt
    
    print(f"Optimal cruise altitude: {best_altitude:,} m")
    print(f"Best L/D ratio: {best_LD_ratio:.2f}")
    
    # Show performance at optimal altitude
    optimal_perf = performance.performance_at_condition(best_altitude, cruise_speed)
    print(f"Required thrust: {optimal_perf['required_thrust']/1000:.2f} kN")
    print(f"Stall speed: {optimal_perf['stall_speed']:.2f} m/s")

def custom_aircraft_analysis():
    """Analysis with custom aircraft parameters"""
    print("\n=== Custom Aircraft Analysis ===")
    
    atm = StandardAtmosphere()
    performance = AircraftPerformance(atm)
    
    # Custom business jet parameters
    custom_params = {
        'wing_area': 30,      # m²
        'mass': 10000,        # kg
        'max_lift_coeff': 2.0,
        'zero_lift_drag': 0.015,
        'aspect_ratio': 8.0
    }
    
    performance.set_aircraft_parameters(**custom_params)
    
    altitude = 12000  # meters
    velocity = 220    # m/s
    
    perf = performance.performance_at_condition(altitude, velocity)
    
    print(f"Custom Business Jet at {altitude:,} m, {velocity} m/s:")
    print(f"  Required Thrust: {perf['required_thrust']/1000:.2f} kN")
    print(f"  L/D Ratio: {perf['lift_to_drag_ratio']:.2f}")
    print(f"  Stall Speed: {perf['stall_speed']:.2f} m/s")

if __name__ == "__main__":
    advanced_performance_analysis()
    optimal_cruise_analysis()
    custom_aircraft_analysis()
