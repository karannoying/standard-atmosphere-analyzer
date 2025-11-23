import numpy as np
from scipy.interpolate import interp1d

class StandardAtmosphere:
    """
    International Standard Atmosphere (ISA) Model
    Calculates atmospheric properties at different altitudes
    """
    
    def __init__(self):
        # ISA constants
        self.R = 287.05  # Gas constant for air [J/(kg·K)]
        self.g0 = 9.80665  # Gravitational acceleration [m/s²]
        self.T0 = 288.15  # Sea level temperature [K]
        self.P0 = 101325  # Sea level pressure [Pa]
        self.rho0 = 1.225  # Sea level density [kg/m³]
        
        # Layer boundaries (geopotential altitude in meters)
        self.layers = {
            'troposphere': (0, 11000),
            'tropopause': (11000, 20000),
            'stratosphere1': (20000, 32000),
            'stratosphere2': (32000, 47000),
            'stratopause': (47000, 51000)
        }
        
    def temperature(self, altitude):
        """
        Calculate temperature at given altitude using ISA model
        """
        h = altitude
        
        if h <= 11000:  # Troposphere
            return self.T0 - 0.0065 * h
        elif h <= 20000:  # Tropopause
            return 216.65
        elif h <= 32000:  # Stratosphere 1
            return 216.65 + 0.001 * (h - 20000)
        elif h <= 47000:  # Stratosphere 2
            return 228.65 + 0.0028 * (h - 32000)
        elif h <= 51000:  # Stratopause
            return 270.65
        else:
            return 270.65  # Simplified for higher altitudes
    
    def pressure(self, altitude):
        """
        Calculate pressure at given altitude using ISA model
        """
        h = altitude
        T = self.temperature(h)
        
        if h <= 11000:  # Troposphere
            return self.P0 * (T / self.T0) ** (self.g0 / (0.0065 * self.R))
        elif h <= 20000:  # Tropopause
            P11 = self.pressure(11000)
            return P11 * np.exp(-self.g0 * (h - 11000) / (self.R * 216.65))
        elif h <= 32000:  # Stratosphere 1
            P20 = self.pressure(20000)
            return P20 * (T / 216.65) ** (-self.g0 / (0.001 * self.R))
        elif h <= 47000:  # Stratosphere 2
            P32 = self.pressure(32000)
            return P32 * (T / 228.65) ** (-self.g0 / (0.0028 * self.R))
        else:  # Stratopause and above
            P47 = self.pressure(47000)
            return P47 * np.exp(-self.g0 * (h - 47000) / (self.R * 270.65))
    
    def density(self, altitude):
        """
        Calculate air density at given altitude
        """
        T = self.temperature(altitude)
        P = self.pressure(altitude)
        return P / (self.R * T)
    
    def speed_of_sound(self, altitude):
        """
        Calculate speed of sound at given altitude
        """
        T = self.temperature(altitude)
        gamma = 1.4  # Ratio of specific heats for air
        return np.sqrt(gamma * self.R * T)
    
    def get_atmospheric_properties(self, altitude):
        """
        Get all atmospheric properties at specified altitude
        """
        T = self.temperature(altitude)
        P = self.pressure(altitude)
        rho = self.density(altitude)
        a = self.speed_of_sound(altitude)
        
        return {
            'altitude': altitude,
            'temperature': T,
            'temperature_c': T - 273.15,
            'pressure': P,
            'pressure_ratio': P / self.P0,
            'density': rho,
            'density_ratio': rho / self.rho0,
            'speed_of_sound': a
        }
    
    def generate_altitude_profile(self, max_altitude=50000, step=100):
        """
        Generate atmospheric profile from sea level to max_altitude
        """
        altitudes = np.arange(0, max_altitude + step, step)
        profile = []
        
        for alt in altitudes:
            props = self.get_atmospheric_properties(alt)
            profile.append(props)
        
        return profile