import numpy as np

class AircraftPerformance:
    """
    Calculate aircraft performance metrics using ISA model
    """
    
    def __init__(self, atmosphere_model):
        self.atm = atmosphere_model
        
        # Default aircraft parameters (Boeing 737-like)
        self.default_params = {
            'wing_area': 125,  # m²
            'mass': 70000,  # kg
            'max_lift_coeff': 1.8,
            'zero_lift_drag': 0.02,
            'oswald_efficiency': 0.85,
            'aspect_ratio': 9.5
        }
    
    def set_aircraft_parameters(self, **params):
        """Update aircraft parameters"""
        self.default_params.update(params)
    
    def lift_coefficient(self, altitude, velocity, mass=None):
        """
        Calculate required lift coefficient
        L = 0.5 * ρ * V² * S * CL
        """
        if mass is None:
            mass = self.default_params['mass']
        
        rho = self.atm.density(altitude)
        S = self.default_params['wing_area']
        g = 9.81  # m/s²
        
        weight = mass * g
        CL = (2 * weight) / (rho * velocity**2 * S)
        return CL
    
    def drag_coefficient(self, CL):
        """
        Calculate drag coefficient using drag polar
        CD = CD0 + (CL² / (π * AR * e))
        """
        CD0 = self.default_params['zero_lift_drag']
        AR = self.default_params['aspect_ratio']
        e = self.default_params['oswald_efficiency']
        
        CD = CD0 + (CL**2 / (np.pi * AR * e))
        return CD
    
    def lift_force(self, altitude, velocity, CL):
        """Calculate lift force"""
        rho = self.atm.density(altitude)
        S = self.default_params['wing_area']
        L = 0.5 * rho * velocity**2 * S * CL
        return L
    
    def drag_force(self, altitude, velocity, CD):
        """Calculate drag force"""
        rho = self.atm.density(altitude)
        S = self.default_params['wing_area']
        D = 0.5 * rho * velocity**2 * S * CD
        return D
    
    def lift_to_drag_ratio(self, CL, CD):
        """Calculate lift-to-drag ratio"""
        return CL / CD if CD > 0 else 0
    
    def required_thrust(self, altitude, velocity, mass=None):
        """
        Calculate required thrust for level flight
        Thrust = Drag in steady level flight
        """
        CL = self.lift_coefficient(altitude, velocity, mass)
        CD = self.drag_coefficient(CL)
        return self.drag_force(altitude, velocity, CD)
    
    def stall_speed(self, altitude, mass=None):
        """Calculate stall speed"""
        if mass is None:
            mass = self.default_params['mass']
        
        rho = self.atm.density(altitude)
        S = self.default_params['wing_area']
        CL_max = self.default_params['max_lift_coeff']
        g = 9.81
        
        weight = mass * g
        V_stall = np.sqrt((2 * weight) / (rho * S * CL_max))
        return V_stall
    
    def performance_at_condition(self, altitude, velocity, mass=None):
        """Calculate all performance metrics at given condition"""
        if mass is None:
            mass = self.default_params['mass']
        
        CL = self.lift_coefficient(altitude, velocity, mass)
        CD = self.drag_coefficient(CL)
        L = self.lift_force(altitude, velocity, CL)
        D = self.drag_force(altitude, velocity, CD)
        L_D = self.lift_to_drag_ratio(CL, CD)
        thrust_required = self.required_thrust(altitude, velocity, mass)
        stall_speed = self.stall_speed(altitude, mass)
        
        return {
            'lift_coefficient': CL,
            'drag_coefficient': CD,
            'lift_force': L,
            'drag_force': D,
            'lift_to_drag_ratio': L_D,
            'required_thrust': thrust_required,
            'stall_speed': stall_speed
        }