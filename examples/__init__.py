"""
Example scripts and usage patterns for Standard Atmosphere Analyzer.

This package contains:
- basic_usage.py: Simple examples to get started
- advanced_analysis.py: More complex analysis scenarios
- custom_aircraft.py: How to work with custom aircraft configurations
"""

__all__ = ['basic_usage', 'advanced_analysis', 'custom_aircraft']

def list_examples():
    """Print available examples and their purposes."""
    examples = {
        'basic_usage': 'Simple examples to get started with the package',
        'advanced_analysis': 'Complex analysis and optimization scenarios',
        'custom_aircraft': 'Working with custom aircraft configurations'
    }
    
    print("Available examples:")
    for name, description in examples.items():
        print(f"  {name}: {description}")
