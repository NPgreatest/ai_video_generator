from dataclasses import dataclass, field

@dataclass
class AudioTrack:
    source: str
    start: float
    end: float
    volume: float
    audio_start: float

