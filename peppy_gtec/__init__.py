"""
Peppy G-TEC: Keep Teams Status Green!

A tool that prevents system inactivity by simulating mouse movement and clicks
during configured working hours to keep status indicators (such as Microsoft Teams)
remain green/active.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "Keep Teams Status Green with Peppy G-TEC"

from .core import AlwaysGreen

__all__ = ["AlwaysGreen"]
