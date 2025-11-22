# ✈️ Standard Atmosphere & Aircraft Performance Analyzer

A comprehensive Python application that implements the International Standard Atmosphere (ISA) model and calculates aircraft performance metrics across different altitudes and flight conditions.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌟 Features

- **International Standard Atmosphere (ISA) Model**: Accurate calculation of atmospheric properties (temperature, pressure, density) up to 50,000 meters
- **Aircraft Performance Analysis**: Calculate lift, drag, required thrust, and other performance metrics
- **Interactive Web Interface**: User-friendly Streamlit app with real-time calculations
- **Professional Visualizations**: Matplotlib plots for atmospheric profiles and performance curves
- **Customizable Aircraft Parameters**: Modify wing area, mass, aerodynamic coefficients, and more
- **Educational Focus**: Perfect for aerospace students and aviation enthusiasts

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/standard-atmosphere-analyzer.git
   cd standard-atmosphere-analyzer
2. Install required packages:
   ```bash
   pip install -r requirements.txt
3. Run the application:
   ```bash
   streamlit run main.py
4. Open your browser to the displayed URL (typically http://localhost:8501)
 
 ```bash
📖 Usage Guide
Web Application
The main application provides four analysis tabs:

Atmosphere Overview: View how temperature, pressure, and density change with altitude

Single Point Analysis: Get detailed atmospheric and performance data at specific conditions

Performance Curves: See how aircraft performance varies with altitude

Thrust-Drag Analysis: Analyze the relationship between velocity and required thrust

Python API
You can also use the core modules directly in your Python code:

python
from src.atmosphere_model import StandardAtmosphere
from src.aircraft_performance import AircraftPerformance

# Create atmosphere model
atm = StandardAtmosphere()

# Get properties at 10,000 meters
properties = atm.get_atmospheric_properties(10000)
print(f"Temperature: {properties['temperature_c']:.2f}°C")
print(f"Density: {properties['density']:.4f} kg/m³")

# Calculate aircraft performance
performance = AircraftPerformance(atm)
metrics = performance.performance_at_condition(10000, 250)
print(f"Required thrust: {metrics['required_thrust']/1000:.2f} kN")

🛠️ Project Structure

standard-atmosphere-analyzer/
├── src/                 # Core Python modules
├── examples/            # Example scripts and usage patterns
├── tests/               # Unit tests
├── docs/               # Documentation
├── data/               # Sample aircraft configurations
├── requirements.txt    # Python dependencies
├── setup.py           # Package installation script
└── main.py            # Streamlit web application

📊 Sample Outputs
Atmospheric Properties:

-Temperature profile from sea level to 50,000 meters
-Pressure and density variations
-Speed of sound calculations
-Aircraft Performance
-Lift and drag forces
-Required thrust for level flight
-Lift-to-drag ratios
-Stall speed calculations
-Aerodynamic coefficients

🎯 Educational Value
This project is ideal for:

-Aerospace engineering students
-Aviation enthusiasts
-Flight simulation developers
-Researchers studying atmospheric physics
-Pilots wanting to understand performance principles

🤝 Contributing
We welcome contributions! Please feel free to submit pull requests, report bugs, or suggest new features.

-Fork the repository
-Create a feature branch (git checkout -b feature/amazing-feature)
-Commit your changes (git commit -m 'Add some amazing feature')
-Push to the branch (git push origin feature/amazing-feature)
-Open a Pull Request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
-International Standard Atmosphere model based on ISO 2533:1975
-Aircraft performance equations from fundamental aerodynamics
-Built with Streamlit, NumPy, SciPy, and Matplotlib

📞 Support
If you have any questions or run into issues:

1.Check the documentation first
2.Open an issue on GitHub
3.Contact the maintainers
