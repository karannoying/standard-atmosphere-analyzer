import streamlit as st
import pandas as pd
import numpy as np
from atmosphere_model import StandardAtmosphere
from aircraft_performance import AircraftPerformance
from visualization import AtmosphereVisualizer

def main():
    st.set_page_config(
        page_title="Standard Atmosphere & Aircraft Performance Analyzer",
        page_icon="✈️",
        layout="wide"
    )
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .section-header {
            font-size: 1.5rem;
            color: #2e86ab;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">✈️ Standard Atmosphere & Aircraft Performance Analyzer</h1>', 
                unsafe_allow_html=True)
    
    # Initialize models
    atm_model = StandardAtmosphere()
    performance_calc = AircraftPerformance(atm_model)
    visualizer = AtmosphereVisualizer()
    
    # Sidebar for user inputs
    st.sidebar.header("Configuration Settings")
    
    # Aircraft parameters
    st.sidebar.subheader("Aircraft Parameters")
    wing_area = st.sidebar.number_input("Wing Area (m²)", value=125.0, min_value=10.0, max_value=500.0)
    aircraft_mass = st.sidebar.number_input("Aircraft Mass (kg)", value=70000.0, min_value=1000.0, max_value=500000.0)
    max_lift_coeff = st.sidebar.number_input("Maximum Lift Coefficient", value=1.8, min_value=0.5, max_value=3.0)
    zero_lift_drag = st.sidebar.number_input("Zero-Lift Drag Coefficient", value=0.02, min_value=0.001, max_value=0.1)
    aspect_ratio = st.sidebar.number_input("Aspect Ratio", value=9.5, min_value=5.0, max_value=20.0)
    
    # Update aircraft parameters
    performance_calc.set_aircraft_parameters(
        wing_area=wing_area,
        mass=aircraft_mass,
        max_lift_coeff=max_lift_coeff,
        zero_lift_drag=zero_lift_drag,
        aspect_ratio=aspect_ratio
    )
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Atmosphere Overview", 
        "Single Point Analysis", 
        "Performance Curves", 
        "Thrust-Drag Analysis"
    ])
    
    with tab1:
        st.markdown('<h2 class="section-header">International Standard Atmosphere Model</h2>', 
                    unsafe_allow_html=True)
        
        max_alt = st.slider("Maximum Altitude for Profile (km)", 1, 50, 20)
        step_size = st.selectbox("Step Size (m)", [100, 500, 1000], index=0)
        
        if st.button("Generate Atmosphere Profile"):
            with st.spinner("Calculating atmospheric properties..."):
                profile = atm_model.generate_altitude_profile(max_altitude=max_alt*1000, step=step_size)
                
                # Create dataframe for display
                df_profile = pd.DataFrame(profile)
                df_display = df_profile[['altitude', 'temperature_c', 'pressure', 'density', 'speed_of_sound']].copy()
                df_display.columns = ['Altitude (m)', 'Temperature (°C)', 'Pressure (Pa)', 'Density (kg/m³)', 'Speed of Sound (m/s)']
                df_display['Altitude (km)'] = df_display['Altitude (m)'] / 1000
                
                st.subheader("Atmospheric Properties Table")
                st.dataframe(df_display.style.format({
                    'Altitude (m)': '{:.0f}',
                    'Altitude (km)': '{:.2f}',
                    'Temperature (°C)': '{:.2f}',
                    'Pressure (Pa)': '{:.2f}',
                    'Density (kg/m³)': '{:.4f}',
                    'Speed of Sound (m/s)': '{:.2f}'
                }), height=400)
                
                # Plot atmospheric properties
                st.subheader("Atmospheric Properties Visualization")
                fig_atm = visualizer.plot_atmospheric_properties(profile)
                st.pyplot(fig_atm)
    
    with tab2:
        st.markdown('<h2 class="section-header">Single Point Performance Analysis</h2>', 
                    unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            altitude = st.number_input("Altitude (m)", value=10000, min_value=0, max_value=50000)
            velocity = st.number_input("Velocity (m/s)", value=250, min_value=50, max_value=500)
        
        if st.button("Calculate Performance"):
            # Get atmospheric properties
            atm_props = atm_model.get_atmospheric_properties(altitude)
            perf_data = performance_calc.performance_at_condition(altitude, velocity)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Atmospheric Conditions")
                st.metric("Altitude", f"{altitude:,} m")
                st.metric("Temperature", f"{atm_props['temperature_c']:.2f} °C")
                st.metric("Pressure", f"{atm_props['pressure']/1000:.2f} kPa")
                st.metric("Density", f"{atm_props['density']:.4f} kg/m³")
                st.metric("Speed of Sound", f"{atm_props['speed_of_sound']:.2f} m/s")
                st.metric("Density Ratio", f"{atm_props['density_ratio']:.4f}")
            
            with col2:
                st.subheader("Aircraft Performance")
                st.metric("Lift Coefficient", f"{perf_data['lift_coefficient']:.4f}")
                st.metric("Drag Coefficient", f"{perf_data['drag_coefficient']:.4f}")
                st.metric("Lift Force", f"{perf_data['lift_force']/1000:.2f} kN")
                st.metric("Drag Force", f"{perf_data['drag_force']/1000:.2f} kN")
                st.metric("Required Thrust", f"{perf_data['required_thrust']/1000:.2f} kN")
                st.metric("Lift-to-Drag Ratio", f"{perf_data['lift_to_drag_ratio']:.2f}")
                st.metric("Stall Speed", f"{perf_data['stall_speed']:.2f} m/s")
    
    with tab3:
        st.markdown('<h2 class="section-header">Performance vs Altitude</h2>', 
                    unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            min_alt = st.number_input("Minimum Altitude (m)", value=0, min_value=0, max_value=40000)
            max_alt = st.number_input("Maximum Altitude (m)", value=15000, min_value=1000, max_value=50000)
            alt_step = st.number_input("Altitude Step (m)", value=500, min_value=100, max_value=2000)
        
        with col2:
            velocity_analysis = st.number_input("Flight Velocity (m/s)", value=250, min_value=100, max_value=400)
        
        if st.button("Generate Performance Curves"):
            with st.spinner("Calculating performance across altitudes..."):
                altitudes = np.arange(min_alt, max_alt + alt_step, alt_step)
                performance_data = []
                
                for alt in altitudes:
                    perf = performance_calc.performance_at_condition(alt, velocity_analysis)
                    performance_data.append(perf)
                
                # Plot performance curves
                fig_perf = visualizer.plot_performance_curves(performance_data, altitudes, velocity_analysis)
                st.pyplot(fig_perf)
                
                # Create performance table
                df_perf = pd.DataFrame(performance_data)
                df_perf['altitude'] = altitudes
                df_perf['altitude_km'] = df_perf['altitude'] / 1000
                
                st.subheader("Performance Data Table")
                st.dataframe(df_perf.style.format({
                    'altitude': '{:.0f}',
                    'altitude_km': '{:.2f}',
                    'lift_coefficient': '{:.4f}',
                    'drag_coefficient': '{:.4f}',
                    'lift_force': '{:.2f}',
                    'drag_force': '{:.2f}',
                    'lift_to_drag_ratio': '{:.2f}',
                    'required_thrust': '{:.2f}',
                    'stall_speed': '{:.2f}'
                }), height=400)
    
    with tab4:
        st.markdown('<h2 class="section-header">Thrust-Drag Analysis</h2>', 
                    unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            analysis_altitude = st.number_input("Analysis Altitude (m)", value=10000, min_value=0, max_value=50000)
        
        with col2:
            min_vel = st.number_input("Minimum Velocity (m/s)", value=150, min_value=50, max_value=300)
            max_vel = st.number_input("Maximum Velocity (m/s)", value=350, min_value=200, max_value=500)
            vel_step = st.number_input("Velocity Step (m/s)", value=10, min_value=1, max_value=50)
        
        if st.button("Analyze Thrust-Drag Relationship"):
            with st.spinner("Calculating thrust-drag curves..."):
                velocities = np.arange(min_vel, max_vel + vel_step, vel_step)
                
                # Plot thrust-drag curves
                fig_td = visualizer.plot_thrust_drag_curves(performance_calc, analysis_altitude, velocities)
                st.pyplot(fig_td)
                
                # Create detailed table
                thrust_data = []
                for vel in velocities:
                    atm_props = atm_model.get_atmospheric_properties(analysis_altitude)
                    perf = performance_calc.performance_at_condition(analysis_altitude, vel)
                    
                    thrust_data.append({
                        'velocity': vel,
                        'mach_number': vel / atm_props['speed_of_sound'],
                        'required_thrust_kN': perf['required_thrust'] / 1000,
                        'drag_force_kN': perf['drag_force'] / 1000,
                        'lift_coefficient': perf['lift_coefficient'],
                        'drag_coefficient': perf['drag_coefficient'],
                        'L_D_ratio': perf['lift_to_drag_ratio']
                    })
                
                df_thrust = pd.DataFrame(thrust_data)
                st.subheader("Thrust-Drag Analysis Data")
                st.dataframe(df_thrust.style.format({
                    'velocity': '{:.1f}',
                    'mach_number': '{:.3f}',
                    'required_thrust_kN': '{:.2f}',
                    'drag_force_kN': '{:.2f}',
                    'lift_coefficient': '{:.4f}',
                    'drag_coefficient': '{:.4f}',
                    'L_D_ratio': '{:.2f}'
                }), height=400)

    # Footer
    st.markdown("---")
    st.markdown("""
    ### 📚 Educational Purpose
    This tool demonstrates the International Standard Atmosphere model and basic aircraft performance calculations.
    **Perfect for aerospace students and enthusiasts!**
    
    *Note: This uses simplified models suitable for educational purposes.*
    """)

if __name__ == "__main__":
    main()