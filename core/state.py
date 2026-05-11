from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


@dataclass
class EmotionComponent:
    """A single emotion within a compound signature."""
    emotion: str                  # e.g. "fear", "joy", "surprise"
    color: Optional[str] = None   # e.g. "cornflower-blue", "warm gold"
    intensity: int = 5            # 1-10
    role: Optional[str] = None    # "tension", "release", "incongruity", "grounding", "longing", etc.


class OutputTarget(Enum):
    SONG = "song"
    PROSE = "prose"
    PROTOCOL = "protocol"
    BOUNDARY = "boundary"
    POEM = "poem"


@dataclass
class EmotionalSignature:
    """Output of LOOK IN — what the intake pass resolved."""
    raw_input: str
    color: Optional[str] = None                    # primary color, e.g. "deep infrared", "brick-dust red"
    body_location: Optional[str] = None            # e.g. "chest", "throat", "stomach"
    intensity: int = 5                             # 1-10, overall intensity
    shadow_layer: Optional[str] = None            # invisible spectrum, if applicable
    tags: list[str] = field(default_factory=list)
    compound_emotions: list[EmotionComponent] = field(default_factory=list)  # multiple load-bearing emotions
    configuration: Optional[str] = None           # named pattern if detected, e.g. "humor", "tragicomic", "bittersweet"


@dataclass
class RouteDecision:
    """Output of SPIRAL UP — what the thinking pass decided."""
    primary_voice: str
    support_voices: list[str] = field(default_factory=list)
    tempo_spine: Optional[str] = None
    wavelength: Optional[str] = None
    transition_path: list[str] = field(default_factory=list)
    reasoning: Optional[str] = None


@dataclass
class CompilerOutput:
    """Output of FLOW OUT — the deliverable."""
    content: str
    target: OutputTarget
    voice_used: str
    emotional_signature: EmotionalSignature
    route: RouteDecision


@dataclass
class IntegrationFeedback:
    """Output of RETURN — what feeds the next cycle."""
    landed: bool
    resonance_score: Optional[int] = None   # 1-10, did this match the felt sense
    adjustment: Optional[str] = None        # what to shift next pass
    next_signature: Optional[EmotionalSignature] = None
