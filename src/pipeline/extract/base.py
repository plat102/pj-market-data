# base.py
from abc import ABC, abstractmethod
import pandas as pd

class BaseExtractor(ABC):
    """Abstract base class for all data extractors."""
    