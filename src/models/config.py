import json
from dataclasses import dataclass, field
from typing import List

from src.models.audio_models import AudioTrack
from src.models.text_models import TextOverlay
from src.models.video_models import VideoClip, ImageClip, Effect


@dataclass
class VideoConfig:
    video_clips: List[VideoClip] = field(default_factory=list)
    audio_tracks: List[AudioTrack] = field(default_factory=list)
    text_overlays: List[TextOverlay] = field(default_factory=list)
    image_overlays: List[ImageClip] = field(default_factory=list)
    effects: List[Effect] = field(default_factory=list)

    @classmethod
    def from_json(cls, file_path: str):
        """Load configuration from JSON file"""
        with open(file_path, 'r') as f:
            data = json.load(f)

        return cls(
            video_clips=[VideoClip(**vc) for vc in data.get("video_clips", [])],
            audio_tracks=[AudioTrack(**at) for at in data.get("audio_tracks", [])],
            text_overlays=[TextOverlay(**to) for to in data.get("text_overlays", [])],
            image_overlays=[ImageClip(**io) for io in data.get("image_overlays", [])],
            effects=[Effect(**eff) for eff in data.get("effects", [])]
        )

