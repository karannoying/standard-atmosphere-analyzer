# Installation Guide

## System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **RAM**: Minimum 4 GB (8 GB recommended)
- **Disk Space**: 100 MB free space

## Installation Methods

### Method 1: Using pip (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/standard-atmosphere-analyzer.git
   cd standard-atmosphere-analyzer
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

**Method 2: Using conda**
   ```bash
Create a new conda environment:

 conda create -n atmosphere-analyzer python=3.9
 conda activate atmosphere-analyzer

 pip install -r requirements.txt

**Method 3: Development Installation**
For contributors who want to modify the code:

Clone and install in development mode:

git clone https://github.com/yourusername/standard-atmosphere-analyzer.git
cd standard-atmosphere-analyzer
pip install -e .
