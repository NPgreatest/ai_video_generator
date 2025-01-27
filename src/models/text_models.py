from dataclasses import dataclass, field
from typing import List


@dataclass
class TextOverlay:
    content: str
    position: List[str]
    font: str
    size: int
    color: str
    start: float
    end: float