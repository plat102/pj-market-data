# base.py
from abc import ABC, abstractmethod
import pandas as pd

class BaseExtractor(ABC):
    """Abstract base class for all data extractors."""
    
    # @abstractmethod
    def fetch_data(self) -> pd.DataFrame:
        """Fetch raw data."""
        pass
