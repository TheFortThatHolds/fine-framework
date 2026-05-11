"""
SPIRAL UP — routing pass.
Takes an EmotionalSignature and decides which voice(s) to engage,
what tempo/wavelength to use, and why. This is the THINKING pass.
"""
import json
import re
from pathlib import Path
from core.state import EmotionalSignature, RouteDecision
from core import llm

VOICES_DIR = Path(__file__).parent.parent / "assets" / "voices"


def _load_voice_index() -> str:
    index = []
    for f in sorted(VOICES_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text())
            # Fort Kit v2.0 stores name at identity.voiceName; fall back to legacy name field
            name = (
                data.get("identity", {}).get("voiceName")
                or data.get("name", f.stem)
            )
            territory = data.get("territory") or data.get("domain", {}).get("primaryHome", "")
            reachable = data.get("reachable_from", [])
            not_from = data.get("not_from", [])
            zone = data.get("domain", {}).get("containmentZone") or data.get("containmentZone", "")

            line = f"{name}: {territory}"
            if reachable:
                line += f" | reach: {'; '.join(reachable[:3])}"
            if not_from:
                line += f" | NOT from: {'; '.join(not_from[:2])}"
            if zone:
                line += f" | zone:{zone}"
            index.append(line)
        except Exception:
            pass
    return "\n".join(index) if index else "No voices loaded."


def _extract_json(text: str) -> dict:
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass
    data = {}
    for field, pattern in [
        ("primary_voice", r'"primary_voice"\s*:\s*"([^"]+)"'),
        ("tempo_spine",   r'"tempo_spine"\s*:\s*"([^"]+)"'),
        ("wavelength",    r'"wavelength"\s*:\s*"([^"]+)"'),
        ("reasoning",     r'"reasoning"\s*:\s*"([^"]+)"'),
    ]:
        m = re.search(pattern, text)
        if m:
            data[field] = m.group(1)
    sv = re.search(r'"support_voices"\s*:\s*\[([^\]]*)\]', text)
    if sv:
        data["support_voices"] = [v.strip().strip('"') for v in sv.group(1).split(',') if v.strip()]
    return data


SYSTEM = """You are a JSON routing engine. Output ONLY raw JSON. No explanation. No markdown. No preamble.

Route this emotional signature to the correct voice(s) from the available list.

SINGLE-EMOTION ROUTING:
- Match color temperature: infrared=body voices (EmberGuide), deep blue/navy=grief (DeepCurrent), ultraviolet=transcendent (UltravioletWitness)
- Match intensity to containment zone: zone 1 = all intensities, zone 2 = mid-high, zone 3 = intensity 5+
- Primary voice does the core work. Support voices add texture only — 1-2 max.
- If no voice fits perfectly, pick the closest one.

COMPOUND EMOTION / CONFIGURATION ROUTING:
When a configuration is named, assemble voices intentionally — not just the loudest emotion:
- "humor": fear(tension) + surprise(incongruity) + joy(release)
  → primary: JoyKeeper, support: [FearTender, ExcitementSpark], tempo_spine: RhythmKeeper
  → RhythmKeeper is always the spine for humor — timing IS the mechanism
- "tragicomic": grief/loss + absurdity simultaneously
  → primary: DeepCurrent, support: [JoyKeeper], tempo_spine: RhythmKeeper
- "bittersweet": joy/love + grief/loss, neither canceling the other
  → primary: DeepCurrent or LoveWeaver depending on which is heavier, support: [JoyKeeper or LoveWeaver]
- "anxious-excitement": fear(approach) + excitement at similar intensities
  → primary: FearTender, support: [ExcitementSpark], tempo_spine: RhythmKeeper
- "righteous-grief": anger(injustice) + grief, fused
  → primary: RevolutionCraft, support: [DeepCurrent]
When compound_emotions are present but no named configuration, route to the emotion carrying the highest structural weight (not necessarily the highest intensity — consider role).

Available voices:
{voice_index}

OUTPUT FORMAT — exactly this, nothing else:
{{"primary_voice":"VoiceName","support_voices":[],"tempo_spine":null,"wavelength":null,"transition_path":[],"reasoning":"one sentence"}}"""


def _format_compound(signature: EmotionalSignature) -> str:
    if not signature.compound_emotions:
        return ""
    parts = []
    for c in signature.compound_emotions:
        parts.append(f"{c.emotion}({c.role or 'present'}, {c.color or '?'}, intensity {c.intensity})")
    config = f" | configuration: {signature.configuration}" if signature.configuration else ""
    return f" | compound: [{', '.join(parts)}]{config}"


def spiral_up(signature: EmotionalSignature) -> RouteDecision:
    voice_index = _load_voice_index()
    system = SYSTEM.format(voice_index=voice_index)

    prompt = (
        f"Color: {signature.color} | "
        f"Body: {signature.body_location} | "
        f"Intensity: {signature.intensity}/10 | "
        f"Shadow: {signature.shadow_layer} | "
        f"Tags: {', '.join(signature.tags)}"
        f"{_format_compound(signature)} | "
        f"Input: {signature.raw_input[:300]}"
    )

    result = llm.decide(system, prompt)
    data = _extract_json(result)

    return RouteDecision(
        primary_voice=data.get("primary_voice", "DeepCurrent"),
        support_voices=data.get("support_voices", []),
        tempo_spine=data.get("tempo_spine"),
        wavelength=data.get("wavelength"),
        transition_path=data.get("transition_path", []),
        reasoning=data.get("reasoning"),
    )
