from dataclasses import dataclass, field
from typing import List


@dataclass
class VideoClip:
    source: str
    start: float
    end: float
    position: List[float]
    scale : float
    video_begin: float


@dataclass
class ImageClip:
    source: str
    start: float
    end: float
    position: List[float]
    scale : float


@dataclass
class Effect:
    type: str
    value: float
    start: float
    end: float