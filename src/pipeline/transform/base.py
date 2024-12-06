from abc import ABC, abstractmethod


class BaseProcessor(ABC):
    @abstractmethod
    def process(self):
        """Abstract method to process data.
        It should be the main method running the processing logic.
        """
