"""
Unit tests for utility functions
"""

import sys
import os
import unittest
import tempfile
import json
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.utils import *

class TestUtils(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary aircraft config file for testing
        self.temp_config = {
            "test_aircraft": {
                "name": "Test Aircraft",
                "wing_area": 100.0,
                "mass": 50000.0,
                "max_lift_coeff": 1.8,
                "zero_lift_drag": 0.02,
                "oswald_efficiency": 0.85,
                "aspect_ratio": 9.0,
                "description": "Test aircraft configuration"
            },
            "another_aircraft": {
                "name": "Another Test Aircraft",
                "wing_area": 150.0,
                "mass": 75000.0
            }
        }
        
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(self.temp_config, self.temp_file)
        self.temp_file.close()
    
    def tearDown(self):
        """Clean up after each test method."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_load_aircraft_config(self):
        """Test loading aircraft configuration from JSON file."""
        # Test successful load
        config = load_aircraft_config(self.temp_file.name)
        
        self.assertIsInstance(config, dict)
        self.assertIn('test_aircraft', config)
        self.assertIn('another_aircraft', config)
        
        # Verify data integrity
        self.assertEqual(config['test_aircraft']['name'], 'Test Aircraft')
        self.assertEqual(config['test_aircraft']['wing_area'], 100.0)
        self.assertEqual(config['test_aircraft']['mass'], 50000.0)
        
        # Test file not found
        with self.assertRaises(FileNotFoundError):
            load_aircraft_config('nonexistent_file.json')
    
    def test_save_aircraft_config(self):
        """Test saving aircraft configuration to JSON file."""
        test_config = {
            "new_aircraft": {
                "name": "New Test Aircraft",
                "wing_area": 200.0,
                "mass": 60000.0,
                "description": "New test configuration"
            }
        }
        
        # Create temporary file for saving
        with tempfile.NamedTemporaryFile(mode='r', suffix='.json', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            # Save configuration
            save_aircraft_config(test_config, tmp_path)
            
            # Verify file was created and contains correct data
            self.assertTrue(os.path.exists(tmp_path))
            
            with open(tmp_path, 'r') as f:
                loaded_config = json.load(f)
            
            self.assertIn('new_aircraft', loaded_config)
            self.assertEqual(loaded_config['new_aircraft']['name'], 'New Test Aircraft')
            self.assertEqual(loaded_config['new_aircraft']['wing_area'], 200.0)
            
        finally:
            # Clean up
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_validate_altitude(self):
        """Test altitude validation function."""
        # Valid altitudes
        valid_altitudes = [0, 1000, 10000, 25000, 50000]
        for alt in valid_altitudes:
            self.assertTrue(validate_altitude(alt), f"Altitude {alt} should be valid")
        
        # Invalid altitudes
        invalid_altitudes = [-1000, -1, 50001, 100000]
        for alt in invalid_altitudes:
            self.assertFalse(validate_altitude(alt), f"Altitude {alt} should be invalid")
        
        # Boundary cases
        self.assertTrue(validate_altitude(0))
        self.assertTrue(validate_altitude(50000))
        self.assertFalse(validate_altitude(50001))
        self.assertFalse(validate_altitude(-1))
    
    def test_validate_velocity(self):
        """Test velocity validation function."""
        # Valid velocities
        valid_velocities = [1, 50, 100, 250, 500, 1000]
        for vel in valid_velocities:
            self.assertTrue(validate_velocity(vel), f"Velocity {vel} should be valid")
        
        # Invalid velocities
        invalid_velocities = [0, -100, -1, 1001, 1500]
        for vel in invalid_velocities:
            self.assertFalse(validate_velocity(vel), f"Velocity {vel} should be invalid")
        
        # Boundary cases
        self.assertTrue(validate_velocity(1))
        self.assertTrue(validate_velocity(1000))
        self.assertFalse(validate_velocity(0))
        self.assertFalse(validate_velocity(1001))
    
    def test_unit_conversions_length(self):
        """Test length unit conversion functions."""
        # Meters to feet and back
        test_values = [0, 1, 1000, 10000, 1524]  # 1524m = 5000ft approx
        
        for meters in test_values:
            feet = meters_to_feet(meters)
            meters_back = feet_to_meters(feet)
            
            self.assertIsInstance(feet, float)
            self.assertIsInstance(meters_back, float)
            self.assertAlmostEqual(meters, meters_back, places=4,
                                 msg=f"Conversion round-trip failed for {meters}m")
        
        # Specific known values
        self.assertAlmostEqual(meters_to_feet(1), 3.28084, places=4)
        self.assertAlmostEqual(feet_to_meters(3.28084), 1.0, places=4)
        self.assertAlmostEqual(meters_to_feet(1000), 3280.84, places=2)
    
    def test_unit_conversions_velocity(self):
        """Test velocity unit conversion functions."""
        # m/s to knots and back
        test_values = [0, 1, 50, 100, 250, 300]
        
        for mps in test_values:
            knots = mps_to_knots(mps)
            mps_back = knots_to_mps(knots)
            
            self.assertIsInstance(knots, float)
            self.assertIsInstance(mps_back, float)
            self.assertAlmostEqual(mps, mps_back, places=4,
                                 msg=f"Conversion round-trip failed for {mps} m/s")
        
        # Specific known values
        self.assertAlmostEqual(mps_to_knots(1), 1.94384, places=4)
        self.assertAlmostEqual(knots_to_mps(1.94384), 1.0, places=4)
        self.assertAlmostEqual(mps_to_knots(100), 194.384, places=2)
    
    def test_mach_number_calculation(self):
        """Test Mach number calculation."""
        # Normal cases
        test_cases = [
            (300, 340, 300/340),  # Subsonic
            (340, 340, 1.0),      # Sonic
            (400, 340, 400/340),  # Supersonic
        ]
        
        for velocity, speed_of_sound, expected_mach in test_cases:
            mach = calculate_mach_number(velocity, speed_of_sound)
            self.assertAlmostEqual(mach, expected_mach, places=6)
            self.assertIsInstance(mach, float)
        
        # Edge case: zero speed of sound
        mach_zero = calculate_mach_number(300, 0)
        self.assertEqual(mach_zero, 0)
        
        # Edge case: zero velocity
        mach_zero_vel = calculate_mach_number(0, 340)
        self.assertEqual(mach_zero_vel, 0)
    
    def test_dynamic_pressure_calculation(self):
        """Test dynamic pressure calculation."""
        test_cases = [
            (1.225, 100, 6125.0),    # Sea level, 100 m/s
            (0.5, 200, 10000.0),     # High altitude, high speed
            (0.1, 300, 4500.0),      # Very high altitude, very high speed
        ]
        
        for density, velocity, expected_pressure in test_cases:
            q = calculate_dynamic_pressure(density, velocity)
            expected = 0.5 * density * velocity**2
            self.assertAlmostEqual(q, expected, places=2)
            self.assertIsInstance(q, float)
        
        # Edge cases
        self.assertEqual(calculate_dynamic_pressure(0, 100), 0)
        self.assertEqual(calculate_dynamic_pressure(1.225, 0), 0)
    
    def test_unit_converter_class(self):
        """Test UnitConverter class methods."""
        # Pressure conversions
        self.assertAlmostEqual(UnitConverter.pressure_pa_to_inhg(101325), 29.92, places=1)
        self.assertAlmostEqual(UnitConverter.pressure_pa_to_psi(101325), 14.7, places=1)
        
        # Test round-trip consistency (approximate due to floating point)
        pa_value = 50000
        inhg = UnitConverter.pressure_pa_to_inhg(pa_value)
        self.assertIsInstance(inhg, float)
        
        psi = UnitConverter.pressure_pa_to_psi(pa_value)
        self.assertIsInstance(psi, float)
        
        # Temperature conversions
        test_temperatures = [-40, 0, 15, 100]  # Celsius
        
        for celsius in test_temperatures:
            fahrenheit = UnitConverter.temperature_c_to_f(celsius)
            expected = celsius * 9/5 + 32
            self.assertAlmostEqual(fahrenheit, expected, places=2)
            self.assertIsInstance(fahrenheit, float)
        
        # Specific known values
        self.assertAlmostEqual(UnitConverter.temperature_c_to_f(0), 32.0, places=1)
        self.assertAlmostEqual(UnitConverter.temperature_c_to_f(100), 212.0, places=1)
        self.assertAlmostEqual(UnitConverter.temperature_c_to_f(-40), -40.0, places=1)
        
        # Force conversions
        self.assertAlmostEqual(UnitConverter.force_n_to_lbf(4.44822), 1.0, places=4)
        self.assertAlmostEqual(UnitConverter.force_n_to_lbf(1000), 1000/4.44822, places=2)
        
        # Test various force values
        test_forces = [1, 100, 1000, 10000]  # Newtons
        
        for newtons in test_forces:
            lbf = UnitConverter.force_n_to_lbf(newtons)
            self.assertIsInstance(lbf, float)
            self.assertGreater(lbf, 0)
    
    def test_unit_converter_edge_cases(self):
        """Test UnitConverter with edge cases."""
        # Zero and negative values
        self.assertEqual(UnitConverter.pressure_pa_to_inhg(0), 0)
        self.assertEqual(UnitConverter.pressure_pa_to_psi(0), 0)
        self.assertEqual(UnitConverter.force_n_to_lbf(0), 0)
        
        # Negative pressure (should handle gracefully)
        negative_inhg = UnitConverter.pressure_pa_to_inhg(-1000)
        self.assertIsInstance(negative_inhg, float)
        
        negative_psi = UnitConverter.pressure_pa_to_psi(-1000)
        self.assertIsInstance(negative_psi, float)
    
    def test_configuration_file_errors(self):
        """Test error handling for configuration files."""
        # Test invalid JSON file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as bad_file:
            bad_file.write("invalid json content {")
            bad_path = bad_file.name
        
        try:
            with self.assertRaises(ValueError):
                load_aircraft_config(bad_path)
        finally:
            if os.path.exists(bad_path):
                os.unlink(bad_path)
        
        # Test empty file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as empty_file:
            empty_path = empty_file.name
        
        try:
            with self.assertRaises(ValueError):
                load_aircraft_config(empty_path)
        finally:
            if os.path.exists(empty_path):
                os.unlink(empty_path)
    
    def test_comprehensive_unit_conversion(self):
        """Test comprehensive unit conversion scenarios."""
        # Real-world aviation scenario
        altitude_m = 10000
        velocity_ms = 250
        
        # Convert to imperial units
        altitude_ft = meters_to_feet(altitude_m)
        velocity_kts = mps_to_knots(velocity_ms)
        
        self.assertAlmostEqual(altitude_ft, 32808.4, places=1)
        self.assertAlmostEqual(velocity_kts, 485.96, places=1)
        
        # Convert back
        altitude_back = feet_to_meters(altitude_ft)
        velocity_back = knots_to_mps(velocity_kts)
        
        self.assertAlmostEqual(altitude_back, altitude_m, places=4)
        self.assertAlmostEqual(velocity_back, velocity_ms, places=4)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)