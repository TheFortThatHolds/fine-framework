"""
LOOK IN — intake pass.
Takes raw human input (chaotic, 50+ words, doesn't matter) and resolves it
into an EmotionalSignature the rest of the compiler can work with.
"""
import json
import re
from core.state import EmotionalSignature, EmotionComponent
from core import llm

SYSTEM = """You are a JSON extraction engine. Output ONLY raw JSON. No explanation. No markdown. No code blocks. No preamble.

Given a description of a feeling, extract these fields:

PRIMARY (always present):
- color: precise color signature of the dominant emotion (NOT generic — "cornflower-blue 3PM loneliness" not "blue")
- body_location: where in the body (chest, throat, stomach, jaw, shoulders, etc)
- intensity: integer 1-10, overall emotional intensity
- shadow_layer: invisible spectrum if applicable (infrared/ultraviolet/radio silence/quantum) or null
- tags: array of 3-5 single words describing the emotional territory

COMPOUND DETECTION (critical):
Ask: are multiple emotions genuinely load-bearing here, not just present but structurally necessary?
- compound_emotions: array of emotion objects, each with:
  - emotion: name (fear, joy, surprise, grief, anger, longing, disgust, shame, etc.)
  - color: precise color for this specific emotion
  - intensity: integer 1-10 for this specific emotion
  - role: what structural role this emotion plays — "tension", "release", "incongruity", "grounding", "longing", "witness", "container"
  If only one emotion is load-bearing, return an empty array [].

CONFIGURATION (only name it if you're certain):
- configuration: if the compound pattern matches a known configuration, name it. Known patterns:
  - "humor" — fear(tension) + surprise(incongruity) + joy(release) working together
  - "tragicomic" — grief or loss + absurdity or irony simultaneously
  - "bittersweet" — joy/love + grief/loss, neither canceling the other
  - "anxious-excitement" — fear(threat) + excitement(approach) at similar intensities
  - "righteous-grief" — anger at injustice + deep sadness, fused not alternating
  - null if no configuration applies or you're not certain

OUTPUT FORMAT — exactly this, nothing else:
{"color":"...","body_location":"...","intensity":5,"shadow_layer":null,"tags":["word","word","word"],"compound_emotions":[{"emotion":"...","color":"...","intensity":5,"role":"..."}],"configuration":null}"""


def _extract_json(text: str) -> dict:
    """Try multiple strategies to pull JSON out of whatever the model returned."""
    text = text.strip()

    # Strategy 1: direct parse
    try:
        return json.loads(text)
    except Exception:
        pass

    # Strategy 2: find outermost {...} block
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass

    # Strategy 3: extract scalar fields manually, leave compound as empty
    data = {}
    for field, pattern in [
        ("color",         r'"color"\s*:\s*"([^"]+)"'),
        ("body_location", r'"body_location"\s*:\s*"([^"]+)"'),
        ("intensity",     r'"intensity"\s*:\s*(\d+)'),
        ("shadow_layer",  r'"shadow_layer"\s*:\s*"([^"]+)"'),
        ("configuration", r'"configuration"\s*:\s*"([^"]+)"'),
    ]:
        m = re.search(pattern, text)
        if m:
            data[field] = int(m.group(1)) if field == "intensity" else m.group(1)

    tags_match = re.search(r'"tags"\s*:\s*\[([^\]]+)\]', text)
    if tags_match:
        data["tags"] = [t.strip().strip('"') for t in tags_match.group(1).split(',')]

    return data


def _parse_compound(raw: list) -> list[EmotionComponent]:
    components = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        components.append(EmotionComponent(
            emotion=item.get("emotion", "unknown"),
            color=item.get("color"),
            intensity=item.get("intensity", 5),
            role=item.get("role"),
        ))
    return components


def look_in(raw_input: str) -> EmotionalSignature:
    result = llm.decide(SYSTEM, raw_input)
    data = _extract_json(result)

    compound_raw = data.get("compound_emotions", [])
    compound = _parse_compound(compound_raw) if isinstance(compound_raw, list) else []

    return EmotionalSignature(
        raw_input=raw_input,
        color=data.get("color"),
        body_location=data.get("body_location"),
        intensity=data.get("intensity", 5),
        shadow_layer=data.get("shadow_layer"),
        tags=data.get("tags", []),
        compound_emotions=compound,
        configuration=data.get("configuration"),
    )
