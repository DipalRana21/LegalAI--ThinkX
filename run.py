"""
Convenience script to run the Streamlit application with Authentication
Run this from the project root: python run.py

This runs the authenticated version that requires login/signup before accessing the main app.
"""

import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    # Use authenticated app as entry point
    app_path = Path(__file__).parent / "frontend" / "authenticated_app.py"
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)])

