# base.py
from abc import ABC, abstractmethod

class BaseConnector(ABC):
    """Abstract base class for all connectors."""

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass
