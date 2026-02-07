"""
Backend module for Legal Assistance System
"""

# Only import config - heavy modules imported lazily when needed
from . import config

# Lazy imports - don't import heavy modules here to avoid loading ML libraries at startup
# These will be imported on-demand in the frontend
__all__ = ['config']

