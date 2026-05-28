from abc import ABC, abstractmethod
from typing import List


class Saver(ABC):
    @abstractmethod
    def save(self, file_paths: List[str], metadata: dict) -> bool:
        pass

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def configure(self, config: dict) -> bool:
        pass
