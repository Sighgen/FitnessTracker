"""
Data service module for handling data-related operations.
Saves in CSV format and provides functions to read and write data.
Uses pandas for data manipulation and file handling and NumPy for numerical computations.
"""

import uuid
from datetime import date, datetime
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd