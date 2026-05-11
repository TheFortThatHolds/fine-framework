"""
FLOW OUT — execution pass.
Takes the route decision, loads the selected voice, and generates the output.
This is the creative generation pass — higher temperature, full voice embodiment.
"""
import json
from pathlib import Path
from core.state import EmotionalSignature, RouteDecision, CompilerOutput, OutputTarget
from core import llm

VOICES_DIR = Path(__file__).parent.parent / "assets" / "voices"


def _load_voice(name: str) -> dict:
    for f in VOICES_DIR.glob("*.json"):
        try:
            data = json.loads(f.read_text())
            # Fort Kit v2.0: name at identity.voiceName; fall back to legacy name field
            voice_name = data.get("identity", {}).get("voiceName") or data.get("name", "")
            if voice_name.lower() == name.lower():
                return data
        except Exception:
            pass
    return {"identity": {"voiceName": name}, "system_prompt": f"You are {name}. Speak from this voice fully."}


def flow_out(
    signature: EmotionalSignature,
    route: RouteDecision,
    target: OutputTarget = OutputTarget.SONG,
) -> CompilerOutput:
    voice = _load_voice(route.primary_voice)
    support = [_load_voice(v) for v in route.support_voices]

    system = voice.get("system_prompt", f"You are {route.primary_voice}.")
    if support:
        support_context = "\n".join(
            f"Also weave in the voice of {v['name']}: {v.get('essence','')}"
            for v in support
        )
        system += f"\n\n{support_context}"

    prompt = f"""Generate a {target.value} for this emotional signature.

Color: {signature.color}
Intensity: {signature.intensity}/10
Shadow layer: {signature.shadow_layer or 'none'}
Tags: {', '.join(signature.tags)}
Tempo: {route.tempo_spine or 'not specified'}
Wavelength: {route.wavelength or 'not specified'}
Routing reason: {route.reasoning}

Raw feeling: {signature.raw_input}

Generate only the {target.value} content. No preamble, no explanation."""

    content = llm.generate(system, prompt)

    return CompilerOutput(
        content=content,
        target=target,
        voice_used=route.primary_voice,
        emotional_signature=signature,
        route=route,
    )
