"""
Unit tests for the atmosphere model
"""

import sys
import os
import unittest
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.atmosphere_model import StandardAtmosphere

class TestStandardAtmosphere(unittest.TestCase):
    
    def setUp(self):
        self.atm = StandardAtmosphere()
    
    def test_sea_level_properties(self):
        """Test that sea level properties match ISA standards"""
        props = self.atm.get_atmospheric_properties(0)
        
        self.assertAlmostEqual(props['temperature'], 288.15, places=1)
        self.assertAlmostEqual(props['pressure'], 101325, places=0)
        self.assertAlmostEqual(props['density'], 1.225, places=2)
    
    def test_temperature_decrease(self):
        """Test temperature decreases in troposphere"""
        temp_0 = self.atm.temperature(0)
        temp_5000 = self.atm.temperature(5000)
        
        self.assertLess(temp_5000, temp_0)
    
    def test_pressure_decrease(self):
        """Test pressure decreases with altitude"""
        press_0 = self.atm.pressure(0)
        press_10000 = self.atm.pressure(10000)
        
        self.assertLess(press_10000, press_0)
    
    def test_density_decrease(self):
        """Test density decreases with altitude"""
        density_0 = self.atm.density(0)
        density_10000 = self.atm.density(10000)
        
        self.assertLess(density_10000, density_0)
    
    def test_negative_altitude(self):
        """Test behavior at negative altitude (should handle gracefully)"""
        with self.assertRaises(ValueError):
            self.atm.get_atmospheric_properties(-1000)
    
    def test_very_high_altitude(self):
        """Test behavior at very high altitude"""
        props = self.atm.get_atmospheric_properties(50000)
        
        self.assertIsInstance(props['temperature'], float)
        self.assertIsInstance(props['pressure'], float)
        self.assertIsInstance(props['density'], float)
    
    def test_altitude_profile_generation(self):
        """Test profile generation function"""
        profile = self.atm.generate_altitude_profile(max_altitude=10000, step=1000)
        
        self.assertEqual(len(profile), 11)  # 0, 1000, 2000, ..., 10000
        self.assertEqual(profile[0]['altitude'], 0)
        self.assertEqual(profile[-1]['altitude'], 10000)

if __name__ == '__main__':
    unittest.main()
