# F.I.N.E. — Framework for Interpreting Nonliteral Expression

> "I'm fine." is always a complete sentence. It is rarely a complete truth. F.I.N.E. reads the gap.

An emotional compiler. You put in what you're actually carrying — inarticulate, half-formed, a wall of text at 2am — and it routes that through a library of 32 emotional voices to generate something that names it, holds it, or helps you move with it.

Not a chatbot. Not a therapist. A compiler — meaning the input is a feeling, the output is a form.

---

## What it actually does

You give it raw emotional input. It runs four passes:

1. **LOOK IN** — reads the emotional signature beneath the words. Color, body location, intensity, whether multiple emotions are structurally load-bearing at once.
2. **SPIRAL UP** — routes to the right voice (or voice assembly) for what's actually being carried. Not just "this is sad" but *which kind* of sad, and whether grief and anger are fused or alternating.
3. **FLOW OUT** — generates the output in the voice of the selected family. Song, poem, prose, protocol, or boundary script.
4. **RETURN** — checks whether it landed. If not, adjusts and recompiles.

The LLM is embedded *in* the passes, not bolted on after. The thinking pass (routing) runs at temperature 0.3. The generation pass runs at 0.9. Different jobs, different temperatures.

---

## Output types

| Target | What you get | When to use it |
|---|---|---|
| `song` | Lyrical, rhythmic emotional expression | Default. When you want it held in musical form. |
| `poem` | Structured poetic form | When the feeling has shape but not story |
| `prose` | Paragraph-form articulation | When you need to say it in words |
| `protocol` | Structured processing steps | When you need to *do* something with what you're feeling |
| `boundary` | Clear boundary-setting language | When you need to say something hard to someone |

---

## Setup

**Requirements:** Python 3.11+, a local or cloud LLM with an OpenAI-compatible API.

```bash
git clone https://github.com/TheFortThatHolds/fine-framework
cd fine-framework
pip install openai
```

**Configure your LLM** — edit `connectors/llm_config.json` or set env vars:

```bash
# Local (llama-server, ollama, LM Studio, etc.)
export FINE_LLM_URL="http://127.0.0.1:8080/v1"
export FINE_MODEL="your-model-name"

# Cloud
export FINE_LLM_URL="https://api.openai.com/v1"
export FINE_MODEL="gpt-4o"
```

Any model works. Larger models route and generate better. The default config points at a local llama-server instance.

---

## Usage

```bash
# Basic — defaults to song output
python fine.py "I don't know what I'm feeling but something is wrong"

# Specify output type
python fine.py "I am so angry I can't breathe" --target poem
python fine.py "I need to tell my manager I can't keep doing this" --target boundary
python fine.py "I can't stop thinking about my dad" --target prose

# With feedback — if the first pass didn't land, add feedback and rerun
python fine.py "I keep circling the same grief" --target prose --feedback "too fast, needs more space"

# Pipe input
echo "three years and I still don't know how to talk about it" | python fine.py --target poem
```

---

## Example run

```
$ python fine.py "everything is fine and I hate that everything is fine and I don't know
what I'm supposed to do with that" --target poem

[LOOK IN]   parsing emotional signature...
            color: flat grey-green | intensity: 6/10 | tags: numb, dissociated, performance
            config: tragicomic | compound: 2 emotions

[SPIRAL UP] routing...
            voice: DeepCurrent + JoyKeeper | spine: RhythmKeeper | compound config: tragicomic

[FLOW OUT]  generating poem...

[RETURN]    integrating...

============================================================
Everything is fine
and the fine is the problem

I have arranged it very carefully
this fine
stacked it like dishes
that don't belong to anyone

Fine is the color of waiting rooms
Fine is the shape of a held breath
Fine means: I have not yet
named what this is

and I am not sure
I want to
============================================================
```

---

## The voice library

32 voices covering the research-grounded emotional spectrum. Each voice is a Fort Kit v2.0 JSON spec in `assets/voices/` — loaded dynamically, so adding a new voice is just adding a file.

A few examples:

| Voice | Territory |
|---|---|
| DeepCurrent | Grief, loss, depth, the weight that doesn't lift |
| FearTender | Fear calibration — threat assessment vs. hypervigilance |
| JoyKeeper | Full-body joy, permission to feel it without guilt |
| RedKeeper | Anger at specific violation — boundary, protection, clarity |
| RevolutionCraft | Personal pain as systemic evidence, collective power |
| RhythmKeeper | Tempo calibration — the pace that matches what the body actually needs |
| ShameHistorian | Identity-level shame — "I am bad" (distinct from guilt) |
| EmberGuide | Body wisdom — what the chest knows before the mind has words |
| SilenceBearer | The silence that has weight, connection loss, radio silence |
| QuantumFamily | Superposition states — feeling two contradictory things at once |

Full list in `assets/voices/`. Full routing logic in `skills/routing_guide.md`.

---

## Compound emotion routing

Some emotional states are structurally compound — multiple emotions are simultaneously load-bearing. Removing any one of them changes the nature of what's being experienced.

The clearest example: **humor**. Humor requires fear (the tension/threat), surprise (the incongruity), and joy (the release when the threat proves safe). Pull any one and it stops working. F.I.N.E. detects this, names it, and routes to a voice assembly instead of a single voice. RhythmKeeper is always the tempo spine for humor — timing IS the mechanism.

Known configurations: `humor`, `tragicomic`, `bittersweet`, `anxious-excitement`, `righteous-grief`

---

## Growth reporting

When F.I.N.E. hits territory the voice library doesn't cover — a routing fallback, a failed landing, a compound pattern it can't name — it writes a growth report to `reports/growth/` and generates a draft Fort Kit skeleton for the potentially missing voice. Reports stay local, gitignored. Review them, promote to `assets/voices/` if the territory is real.

This is how the library grows. The system documents its own edges.

---

## Using as an MCP tool

F.I.N.E. does not ship with an MCP server — you build yours, for your sovereignty. Full setup guide in `skills/mcp_setup_guide.md`. Once wrapped, any MCP-compatible client (Claude Desktop, Cursor, etc.) can call `compile_feeling()` as a tool.

---

## Architecture

```
manifest.json          plugin identity, permissions, sovereignty declaration
fine.py                CLI entry point
assets/voices/         32 voice JSON files (Fort Kit v2.0 schema) — embedded
connectors/            LLM connection config — bring your own endpoint
skills/                routing guide, configuration patterns, MCP setup
growth/                gap detection and growth reporting
reports/growth/        growth reports land here (local only, gitignored)
voices_pending/        draft voices awaiting human review (gitignored)
core/                  state types, LLM client
look_in/               LOOK IN pass — emotional signature extraction
spiral_up/             SPIRAL UP pass — routing
flow_out/              FLOW OUT pass — generation
return_to/             RETURN pass — integration and feedback
```

---

## Philosophy

Emotion is not secondary to "real" systems — logic, economics, science. That framing is backwards. Emotion is part of the deeper relational architecture that living systems use to organize themselves. Fear organizes groups differently than hope. Trust builds different societies than humiliation.

Logic tells you *how* to pursue a goal. Emotion tells a system *what's worth protecting, dangerous, beautiful, worth sacrificing for.*

F.I.N.E. is built on this premise. The 32-voice library is a working map of that layer. The "nonliteral" in F.I.N.E. is precisely the emotional layer that underlies the rational surface — the thing people mean when they say "I'm fine" and mean something else entirely.

---

## License

MIT. Fork it, extend it, wrap it in whatever you're building. Add voices. Name new configurations. If you hit something the library doesn't cover and write a new voice for it, the growth reporter was designed for exactly that moment.
