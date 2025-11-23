import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter
import streamlit as st

class AtmosphereVisualizer:
    """Create professional plots for atmospheric and performance data"""
    
    def __init__(self):
        plt.style.use('seaborn-v0_8')
        self.fig_size = (10, 6)
    
    def plot_atmospheric_properties(self, profile):
        """Plot atmospheric properties vs altitude"""
        altitudes = [p['altitude'] / 1000 for p in profile]  # Convert to km
        temperatures = [p['temperature_c'] for p in profile]
        pressures = [p['pressure'] / 1000 for p in profile]  # Convert to kPa
        densities = [p['density'] for p in profile]
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        
        # Temperature plot
        ax1.plot(temperatures, altitudes, 'r-', linewidth=2)
        ax1.set_xlabel('Temperature (°C)')
        ax1.set_ylabel('Altitude (km)')
        ax1.set_title('Temperature vs Altitude')
        ax1.grid(True, alpha=0.3)
        
        # Pressure plot
        ax2.plot(pressures, altitudes, 'b-', linewidth=2)
        ax2.set_xlabel('Pressure (kPa)')
        ax2.set_ylabel('Altitude (km)')
        ax2.set_title('Pressure vs Altitude')
        ax2.grid(True, alpha=0.3)
        ax2.set_xscale('log')
        
        # Density plot
        ax3.plot(densities, altitudes, 'g-', linewidth=2)
        ax3.set_xlabel('Density (kg/m³)')
        ax3.set_ylabel('Altitude (km)')
        ax3.set_title('Density vs Altitude')
        ax3.grid(True, alpha=0.3)
        ax3.set_xscale('log')
        
        # All properties together
        ax4.plot(temperatures, altitudes, 'r-', label='Temperature', linewidth=2)
        ax4_twin = ax4.twinx()
        ax4_twin.plot(pressures, altitudes, 'b-', label='Pressure', linewidth=2)
        ax4_twin.plot(densities, altitudes, 'g-', label='Density', linewidth=2)
        
        ax4.set_xlabel('Temperature (°C)')
        ax4.set_ylabel('Altitude (km)')
        ax4_twin.set_ylabel('Pressure (kPa) / Density (kg/m³)')
        ax4.set_title('All Properties vs Altitude')
        ax4.legend(loc='upper left')
        ax4_twin.legend(loc='upper right')
        ax4.grid(True, alpha=0.3)
        ax4_twin.set_yscale('linear')
        
        plt.tight_layout()
        return fig
    
    def plot_performance_curves(self, performance_data, altitudes, velocity):
        """Plot aircraft performance curves"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        
        # Lift and Drag vs Altitude
        lift_forces = [p['lift_force'] / 1000 for p in performance_data]  # kN
        drag_forces = [p['drag_force'] / 1000 for p in performance_data]  # kN
        thrust_required = [p['required_thrust'] / 1000 for p in performance_data]  # kN
        
        ax1.plot(altitudes, lift_forces, 'g-', label='Lift Force', linewidth=2)
        ax1.plot(altitudes, drag_forces, 'r-', label='Drag Force', linewidth=2)
        ax1.plot(altitudes, thrust_required, 'b--', label='Required Thrust', linewidth=2)
        ax1.set_xlabel('Altitude (m)')
        ax1.set_ylabel('Force (kN)')
        ax1.set_title(f'Forces vs Altitude (Velocity: {velocity} m/s)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Lift-to-Drag Ratio vs Altitude
        L_D_ratios = [p['lift_to_drag_ratio'] for p in performance_data]
        ax2.plot(altitudes, L_D_ratios, 'purple', linewidth=2)
        ax2.set_xlabel('Altitude (m)')
        ax2.set_ylabel('L/D Ratio')
        ax2.set_title('Lift-to-Drag Ratio vs Altitude')
        ax2.grid(True, alpha=0.3)
        
        # Coefficients vs Altitude
        CL_values = [p['lift_coefficient'] for p in performance_data]
        CD_values = [p['drag_coefficient'] for p in performance_data]
        
        ax3.plot(altitudes, CL_values, 'orange', label='Lift Coefficient (CL)', linewidth=2)
        ax3.plot(altitudes, CD_values, 'brown', label='Drag Coefficient (CD)', linewidth=2)
        ax3.set_xlabel('Altitude (m)')
        ax3.set_ylabel('Coefficient Value')
        ax3.set_title('Aerodynamic Coefficients vs Altitude')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Stall Speed vs Altitude
        stall_speeds = [p['stall_speed'] for p in performance_data]
        ax4.plot(altitudes, stall_speeds, 'red', linewidth=2)
        ax4.set_xlabel('Altitude (m)')
        ax4.set_ylabel('Stall Speed (m/s)')
        ax4.set_title('Stall Speed vs Altitude')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_thrust_drag_curves(self, performance_calc, altitude, velocities):
        """Plot thrust vs drag curves"""
        thrust_values = []
        drag_values = []
        L_D_ratios = []
        
        for vel in velocities:
            perf = performance_calc.performance_at_condition(altitude, vel)
            thrust_values.append(perf['required_thrust'] / 1000)  # kN
            drag_values.append(perf['drag_force'] / 1000)  # kN
            L_D_ratios.append(perf['lift_to_drag_ratio'])
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Thrust vs Drag
        ax1.plot(velocities, thrust_values, 'b-', label='Required Thrust', linewidth=2)
        ax1.plot(velocities, drag_values, 'r-', label='Drag Force', linewidth=2)
        ax1.set_xlabel('Velocity (m/s)')
        ax1.set_ylabel('Force (kN)')
        ax1.set_title(f'Thrust and Drag vs Velocity (Altitude: {altitude} m)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # L/D Ratio vs Velocity
        ax2.plot(velocities, L_D_ratios, 'green', linewidth=2)
        ax2.set_xlabel('Velocity (m/s)')
        ax2.set_ylabel('L/D Ratio')
        ax2.set_title(f'Lift-to-Drag Ratio vs Velocity (Altitude: {altitude} m)')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig