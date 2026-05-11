"""
RETURN — integration pass.
Did the output land? Feeds back into the next cycle.
Can run silently (no feedback) or interactively.
"""
from core.state import CompilerOutput, IntegrationFeedback, EmotionalSignature


def return_to(output: CompilerOutput, feedback: str = None) -> IntegrationFeedback:
    """
    feedback: optional user response ("yes this landed", "too intense", "wrong voice", etc.)
    If None, returns a neutral pass-through so the pipeline can run non-interactively.
    """
    if feedback is None:
        return IntegrationFeedback(landed=True)

    feedback_lower = feedback.lower()

    landed = not any(word in feedback_lower for word in [
        "no", "wrong", "not quite", "off", "miss", "didn't", "nope"
    ])

    adjustment = None
    if "too intense" in feedback_lower:
        adjustment = "lower_intensity"
    elif "too gentle" in feedback_lower or "need more" in feedback_lower:
        adjustment = "raise_intensity"
    elif "wrong voice" in feedback_lower:
        adjustment = "reroute"
    elif "different" in feedback_lower:
        adjustment = "vary_output"

    next_sig = None
    if not landed and output.emotional_signature:
        sig = output.emotional_signature
        next_sig = EmotionalSignature(
            raw_input=f"{sig.raw_input} [adjustment: {adjustment}]",
            color=sig.color,
            body_location=sig.body_location,
            intensity=sig.intensity,
            shadow_layer=sig.shadow_layer,
            tags=sig.tags,
            compound_emotions=sig.compound_emotions,
            configuration=sig.configuration,
        )

    return IntegrationFeedback(
        landed=landed,
        adjustment=adjustment,
        next_signature=next_sig,
    )
