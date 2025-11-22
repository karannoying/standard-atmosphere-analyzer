```markdown
# Usage Guide

## Web Application

### Starting the Application

1. Open a terminal/command prompt
2. Navigate to the project directory
3. Run: `streamlit run main.py`
4. Open your browser to the displayed URL (usually http://localhost:8501)

### Interface Overview

The application has four main tabs:

#### 1. Atmosphere Overview
- **Purpose**: View how atmospheric properties change with altitude
- **Controls**: 
  - Maximum altitude slider (1-50 km)
  - Step size selector
- **Outputs**: 
  - Interactive table of properties
  - Four-panel visualization

#### 2. Single Point Analysis
- **Purpose**: Get detailed data at specific flight conditions
- **Controls**:
  - Altitude input (0-50,000 meters)
  - Velocity input (50-500 m/s)
- **Outputs**:
  - Atmospheric conditions panel
  - Aircraft performance panel

#### 3. Performance Curves
- **Purpose**: Analyze how performance changes with altitude
- **Controls**:
  - Altitude range (min/max)
  - Flight velocity
  - Altitude step size
- **Outputs**:
  - Four performance graphs
  - Data table

#### 4. Thrust-Drag Analysis
- **Purpose**: Study thrust requirements across speeds
- **Controls**:
  - Analysis altitude
  - Velocity range
  - Velocity step size
- **Outputs**:
  - Thrust-Drag curves
  - L/D ratio vs velocity
  - Detailed data table

## Python API Usage

### Basic Atmosphere Model

```python
from src.atmosphere_model import StandardAtmosphere

# Create model
atm = StandardAtmosphere()

# Get properties at specific altitude
props = atm.get_atmospheric_properties(10000)  # 10,000 meters
print(f"Temperature: {props['temperature_c']}°C")
print(f"Density: {props['density']} kg/m³")

# Generate altitude profile
profile = atm.generate_altitude_profile(max_altitude=20000, step=500)
