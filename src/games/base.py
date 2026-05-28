from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List


@dataclass
class SaveEntry:
    name: str
    path: str
    game: str
    platform: str = ""
    size_bytes: int = 0
    files: List[str] = field(default_factory=list)


class GameFinder(ABC):
    @abstractmethod
    def find_saves(self) -> List[SaveEntry]:
        pass

    @abstractmethod
    def name(self) -> str:
        pass
