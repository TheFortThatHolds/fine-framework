"""
LLM client — uses local Gemma model via llama-server (same as Hermes pipeline).
Two call types: decide() for the thinking pass, generate() for the execution pass.
Set FINE_LLM_URL / FINE_MODEL env vars to override.
"""
import os
from openai import OpenAI

LOCAL_BASE_URL = os.getenv("FINE_LLM_URL", "http://127.0.0.1:8080/v1")
LOCAL_MODEL = os.getenv("FINE_MODEL", "gemma4e4b")

_client = OpenAI(base_url=LOCAL_BASE_URL, api_key="local")


def decide(system: str, prompt: str, model: str = None) -> str:
    """SPIRAL UP pass — structured reasoning, returns decision."""
    return _call(system, prompt, model, temperature=0.3)


def generate(system: str, prompt: str, model: str = None) -> str:
    """FLOW OUT pass — creative generation, higher temperature."""
    return _call(system, prompt, model, temperature=0.9)


def _call(system: str, prompt: str, model: str = None, temperature: float = 0.7) -> str:
    response = _client.chat.completions.create(
        model=model or LOCAL_MODEL,
        temperature=temperature,
        max_tokens=4096,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content
