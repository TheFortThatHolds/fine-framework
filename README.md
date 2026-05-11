# F.I.N.E. — Framework for Interpreting Nonliteral Expression

An emotional compiler where the LLM is embedded in the compilation passes, not bolted on after.

## The Four Passes

```
LOOK IN     →  intake, assessment, body signals, color identification
SPIRAL UP   →  routing, state machine, voice selection  (LLM decides)
FLOW OUT    →  execution, generation, the deliverable   (LLM generates)
RETURN      →  integration, feedback, next cycle
```

## Architecture

```
look_in/     — parser: human input → EmotionalSignature (compound-aware)
spiral_up/   — router: EmotionalSignature → voice configuration (thinking pass)
flow_out/    — executor: voice + context → output (generation pass)
return_to/   — integrator: output → feedback loop
voices/      — voice family definitions (Fort Kit v2.0 schema)
core/        — shared state types, LLM client, primitives
```

## Compound Emotion Routing

Emotions don't arrive alone. Humor structurally requires fear (tension) + surprise (incongruity) + joy (release) — pull any one and it stops working. LOOK IN detects when multiple emotions are load-bearing and names the configuration. SPIRAL UP routes to voice assemblies, not just single voices.

Known configurations: `humor`, `tragicomic`, `bittersweet`, `anxious-excitement`, `righteous-grief`

For humor routing, RhythmKeeper is always the tempo spine — timing is the mechanism.

## Usage

```bash
python fine.py "I don't know what I'm feeling but something is wrong"
python fine.py "I am so angry I can't breathe" --target poem
python fine.py "I keep circling the same grief" --target prose --feedback "too fast, needs more space"
```

## Environment

```
FINE_LLM_URL   local LLM endpoint (default: http://127.0.0.1:8080/v1)
FINE_MODEL     model name (default: gemma4e4b)
```

## Philosophy

Emotion is the organizational infrastructure beneath all visible rational systems.
Logic tells you *how* to pursue a goal. Emotion tells a system *what's worth protecting,
dangerous, beautiful, worth sacrificing for.* F.I.N.E. reads the layer logic can't provide.

Song, prose chapter, therapeutic protocol, boundary script — all run the same four passes.
The voice families are what change. The engine stays.
