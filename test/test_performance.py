"""
Unit tests for aircraft performance calculations
"""

import sys
import os
import unittest
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.atmosphere_model import StandardAtmosphere
from src.aircraft_performance import AircraftPerformance

class TestAircraftPerformance(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.atm = StandardAtmosphere()
        self.performance = AircraftPerformance(self.atm)
    
    def test_lift_coefficient_calculation(self):
        """Test lift coefficient calculation at various conditions."""
        # Test at cruise conditions
        CL = self.performance.lift_coefficient(10000, 250)
        self.assertIsInstance(CL, float)
        self.assertGreater(CL, 0)
        self.assertLess(CL, 2.0)  # Reasonable CL range
        
        # Test at low altitude
        CL_low = self.performance.lift_coefficient(0, 100)
        self.assertGreater(CL_low, CL)  # Higher CL at lower altitude/speed
        
        # Test with custom mass
        CL_custom = self.performance.lift_coefficient(10000, 250, mass=80000)
        self.assertGreater(CL_custom, CL)  # Higher mass requires higher CL
    
    def test_drag_coefficient_calculation(self):
        """Test drag coefficient calculation using drag polar."""
        # Test with various lift coefficients
        test_CLs = [0.1, 0.5, 1.0, 1.5]
        
        for CL in test_CLs:
            CD = self.performance.drag_coefficient(CL)
            self.assertIsInstance(CD, float)
            self.assertGreater(CD, self.performance.default_params['zero_lift_drag'])
            
            # Verify drag polar equation: CD = CD0 + (CL² / (π * AR * e))
            CD0 = self.performance.default_params['zero_lift_drag']
            AR = self.performance.default_params['aspect_ratio']
            e = self.performance.default_params['oswald_efficiency']
            expected_CD = CD0 + (CL**2 / (np.pi * AR * e))
            self.assertAlmostEqual(CD, expected_CD, places=6)
    
    def test_lift_force_calculation(self):
        """Test lift force calculation."""
        CL = 0.5
        lift = self.performance.lift_force(10000, 250, CL)
        
        self.assertIsInstance(lift, float)
        self.assertGreater(lift, 0)
        
        # Verify lift equation: L = 0.5 * ρ * V² * S * CL
        rho = self.atm.density(10000)
        S = self.performance.default_params['wing_area']
        expected_lift = 0.5 * rho * 250**2 * S * CL
        self.assertAlmostEqual(lift, expected_lift, places=2)
    
    def test_drag_force_calculation(self):
        """Test drag force calculation."""
        CD = 0.05
        drag = self.performance.drag_force(10000, 250, CD)
        
        self.assertIsInstance(drag, float)
        self.assertGreater(drag, 0)
        
        # Verify drag equation: D = 0.5 * ρ * V² * S * CD
        rho = self.atm.density(10000)
        S = self.performance.default_params['wing_area']
        expected_drag = 0.5 * rho * 250**2 * S * CD
        self.assertAlmostEqual(drag, expected_drag, places=2)
    
    def test_required_thrust(self):
        """Test required thrust calculation for level flight."""
        thrust = self.performance.required_thrust(10000, 250)
        
        self.assertIsInstance(thrust, float)
        self.assertGreater(thrust, 0)
        
        # In steady level flight, thrust should equal drag
        CL = self.performance.lift_coefficient(10000, 250)
        CD = self.performance.drag_coefficient(CL)
        expected_thrust = self.performance.drag_force(10000, 250, CD)
        self.assertAlmostEqual(thrust, expected_thrust, places=2)
    
    def test_stall_speed(self):
        """Test stall speed calculation."""
        stall_speed = self.performance.stall_speed(5000)
        
        self.assertIsInstance(stall_speed, float)
        self.assertGreater(stall_speed, 0)
        
        # Verify stall speed equation: V_stall = √(2 * W / (ρ * S * CL_max))
        mass = self.performance.default_params['mass']
        rho = self.atm.density(5000)
        S = self.performance.default_params['wing_area']
        CL_max = self.performance.default_params['max_lift_coeff']
        g = 9.81
        
        expected_stall = np.sqrt((2 * mass * g) / (rho * S * CL_max))
        self.assertAlmostEqual(stall_speed, expected_stall, places=2)
        
        # Stall speed should increase with altitude
        stall_sea = self.performance.stall_speed(0)
        stall_high = self.performance.stall_speed(15000)
        self.assertGreater(stall_high, stall_sea)
    
    def test_lift_to_drag_ratio(self):
        """Test lift-to-drag ratio calculation."""
        # Test various CL values
        test_cases = [
            (0.1, 0.02),  # Low CL
            (0.5, 0.05),  # Medium CL  
            (1.0, 0.12),  # High CL
        ]
        
        for CL, expected_min_LD in test_cases:
            CD = self.performance.drag_coefficient(CL)
            L_D = self.performance.lift_to_drag_ratio(CL, CD)
            
            self.assertIsInstance(L_D, float)
            self.assertGreater(L_D, expected_min_LD)
            self.assertAlmostEqual(L_D, CL / CD, places=6)
        
        # Test edge case: zero drag coefficient
        L_D_zero = self.performance.lift_to_drag_ratio(0.5, 0)
        self.assertEqual(L_D_zero, 0)
    
    def test_performance_at_condition(self):
        """Test comprehensive performance calculation."""
        perf = self.performance.performance_at_condition(10000, 250)
        
        # Check all required keys are present
        required_keys = [
            'lift_coefficient', 'drag_coefficient', 'lift_force',
            'drag_force', 'lift_to_drag_ratio', 'required_thrust', 'stall_speed'
        ]
        
        for key in required_keys:
            self.assertIn(key, perf)
            self.assertIsInstance(perf[key], (int, float))
        
        # Verify internal consistency
        self.assertAlmostEqual(
            perf['lift_to_drag_ratio'],
            perf['lift_coefficient'] / perf['drag_coefficient'],
            places=6
        )
        
        self.assertAlmostEqual(
            perf['required_thrust'],
            perf['drag_force'],
            places=2
        )
        
        # All values should be positive (except L/D which can be any value)
        for key, value in perf.items():
            if key != 'lift_to_drag_ratio':
                self.assertGreater(value, 0)
    
    def test_parameter_update(self):
        """Test aircraft parameter updating functionality."""
        original_wing_area = self.performance.default_params['wing_area']
        original_mass = self.performance.default_params['mass']
        
        new_params = {
            'wing_area': 150.0,
            'mass': 80000.0,
            'max_lift_coeff': 2.0,
            'zero_lift_drag': 0.015,
            'aspect_ratio': 10.0
        }
        
        # Update parameters
        self.performance.set_aircraft_parameters(**new_params)
        
        # Verify updates
        for param, value in new_params.items():
            self.assertEqual(self.performance.default_params[param], value)
        
        # Test that performance calculations use new parameters
        perf_original = AircraftPerformance(self.atm).performance_at_condition(10000, 250)
        perf_updated = self.performance.performance_at_condition(10000, 250)
        
        # Performance should be different with different parameters
        self.assertNotAlmostEqual(
            perf_original['required_thrust'],
            perf_updated['required_thrust'],
            places=2
        )
    
    def test_edge_cases(self):
        """Test performance calculations at edge cases."""
        # Very low altitude
        perf_low = self.performance.performance_at_condition(0, 50)
        self.assertGreater(perf_low['lift_coefficient'], 0)
        
        # Very high altitude
        perf_high = self.performance.performance_at_condition(40000, 300)
        self.assertGreater(perf_high['lift_coefficient'], 0)
        
        # Very low speed (near stall)
        perf_slow = self.performance.performance_at_condition(5000, 80)
        self.assertGreater(perf_slow['lift_coefficient'], 0)
    
    def test_physical_plausibility(self):
        """Test that results are physically plausible."""
        test_conditions = [
            (0, 100),    # Low altitude, low speed
            (10000, 250), # Cruise conditions
            (15000, 300), # High altitude, high speed
        ]
        
        for altitude, velocity in test_conditions:
            perf = self.performance.performance_at_condition(altitude, velocity)
            
            # CL should be reasonable for conventional aircraft
            self.assertGreater(perf['lift_coefficient'], 0.1)
            self.assertLess(perf['lift_coefficient'], 2.0)
            
            # CD should be greater than CD0
            self.assertGreater(perf['drag_coefficient'], 
                             self.performance.default_params['zero_lift_drag'])
            
            # L/D ratio should be reasonable
            self.assertGreater(perf['lift_to_drag_ratio'], 5)
            self.assertLess(perf['lift_to_drag_ratio'], 25)
            
            # Stall speed should be less than current velocity
            self.assertLess(perf['stall_speed'], velocity * 1.5)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)