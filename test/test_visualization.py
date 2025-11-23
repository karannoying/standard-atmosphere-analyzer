"""
Unit tests for visualization module
"""

import sys
import os
import unittest
import tempfile
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.atmosphere_model import StandardAtmosphere
from src.aircraft_performance import AircraftPerformance
from src.visualization import AtmosphereVisualizer

class TestVisualization(unittest.TestCase):
    
    def setUp(self):
        self.atm = StandardAtmosphere()
        self.performance = AircraftPerformance(self.atm)
        self.visualizer = AtmosphereVisualizer()
        
        # Generate sample data for testing
        self.profile = self.atm.generate_altitude_profile(max_altitude=10000, step=1000)
        
        # Generate sample performance data
        self.altitudes = [0, 5000, 10000]
        self.performance_data = []
        for alt in self.altitudes:
            perf = self.performance.performance_at_condition(alt, 250)
            self.performance_data.append(perf)
    
    def test_visualizer_initialization(self):
        """Test visualization class initialization"""
        self.assertIsInstance(self.visualizer, AtmosphereVisualizer)
        self.assertEqual(self.visualizer.fig_size, (10, 6))
    
    def test_atmospheric_properties_plot(self):
        """Test atmospheric properties plotting"""
        fig = self.visualizer.plot_atmospheric_properties(self.profile)
        
        self.assertIsNotNone(fig)
        self.assertEqual(len(fig.axes), 4)  # Should have 4 subplots
    
    def test_performance_curves_plot(self):
        """Test performance curves plotting"""
        fig = self.visualizer.plot_performance_curves(
            self.performance_data, 
            self.altitudes, 
            250
        )
        
        self.assertIsNotNone(fig)
        self.assertEqual(len(fig.axes), 4)  # Should have 4 subplots
    
    def test_thrust_drag_curves_plot(self):
        """Test thrust-drag curves plotting"""
        velocities = [150, 200, 250, 300]
        fig = self.visualizer.plot_thrust_drag_curves(
            self.performance,
            10000,
            velocities
        )
        
        self.assertIsNotNone(fig)
        self.assertEqual(len(fig.axes), 2)  # Should have 2 subplots
    
    def test_plot_saving(self):
        """Test that plots can be saved to file"""
        fig = self.visualizer.plot_atmospheric_properties(self.profile)
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            fig.savefig(tmp_file.name, dpi=100, bbox_inches='tight')
            self.assertTrue(os.path.exists(tmp_file.name))
            
            # Clean up
            os.unlink(tmp_file.name)

if __name__ == '__main__':
    unittest.main()