# F.I.N.E. — Technical Documentation

Framework for Interpreting Nonliteral Expression  
Four-pass emotional compiler. LLM embedded in the pipeline, not bolted on after.

→ [Plain language overview in README.md](README.md)

---

## Pipeline overview

```
raw input
    │
    ▼
┌─────────────────────────────────────┐
│  LOOK IN  (look_in/intake.py)       │
│  temp: 0.3 — structured extraction  │
│  EmotionalSignature ←───────────────┤
└─────────────────────────────────────┘
    │ EmotionalSignature
    ▼
┌─────────────────────────────────────┐
│  SPIRAL UP  (spiral_up/router.py)   │
│  temp: 0.3 — routing decision       │
│  RouteDecision ←────────────────────┤
└─────────────────────────────────────┘
    │ EmotionalSignature + RouteDecision
    ▼
┌─────────────────────────────────────┐
│  FLOW OUT  (flow_out/executor.py)   │
│  temp: 0.9 — creative generation    │
│  CompilerOutput ←───────────────────┤
└─────────────────────────────────────┘
    │ CompilerOutput
    ▼
┌─────────────────────────────────────┐
│  RETURN  (return_to/integrate.py)   │
│  feedback parsing, adjustment loop  │
│  IntegrationFeedback ←──────────────┤
└─────────────────────────────────────┘
    │ if not landed → recompile
    ▼
  output
    │
    └→ growth/reporter.py (gap detection, runs after RETURN)
```

**Temperature split rationale:** LOOK IN and SPIRAL UP are structured extraction and routing — they need to be stable and consistent. Temperature 0.3. FLOW OUT is creative generation — it needs latitude. Temperature 0.9. Different jobs, different temperatures.

---

## Data structures

```python
@dataclass
class EmotionComponent:
    emotion: str       # "fear", "joy", "surprise", etc.
    color: str         # precise color for this specific emotion
    intensity: int     # 1-10
    role: str          # "tension", "release", "incongruity", "grounding", etc.

@dataclass
class EmotionalSignature:
    raw_input: str
    color: str                              # primary color ("cornflower-blue 3PM loneliness")
    body_location: str                      # "chest", "throat", "stomach", etc.
    intensity: int                          # 1-10 overall
    shadow_layer: str                       # "infrared" | "ultraviolet" | "radio silence" | "quantum" | null
    tags: list[str]                         # 3-5 territory descriptors
    compound_emotions: list[EmotionComponent]  # multiple load-bearing emotions when present
    configuration: str                      # named pattern if detected, or null

@dataclass
class RouteDecision:
    primary_voice: str
    support_voices: list[str]
    tempo_spine: str          # usually RhythmKeeper when pacing is the mechanism
    wavelength: str
    transition_path: list[str]
    reasoning: str

@dataclass
class CompilerOutput:
    content: str
    target: OutputTarget
    voice_used: str
    emotional_signature: EmotionalSignature
    route: RouteDecision

@dataclass
class IntegrationFeedback:
    landed: bool
    resonance_score: int        # 1-10
    adjustment: str             # "lower_intensity" | "raise_intensity" | "reroute" | "vary_output"
    next_signature: EmotionalSignature   # populated for recompile

class OutputTarget(Enum):
    SONG = "song"
    PROSE = "prose"
    PROTOCOL = "protocol"
    BOUNDARY = "boundary"
    POEM = "poem"
```

---

## LOOK IN

**File:** `look_in/intake.py`  
**Temperature:** 0.3

Extracts the emotional signature from raw input. The critical design choice: it does not look for the literal content of what was said. It looks for the emotional signature beneath it.

**Primary extraction:**
- `color` — precise, not generic. "Cornflower-blue 3PM loneliness" ≠ "navy grief-weight" ≠ "steel-blue shutdown". The color carries diagnostic information.
- `body_location` — where in the body the feeling lives
- `intensity` — 1-10 overall
- `shadow_layer` — states that operate outside the visible spectrum:
  - `infrared` — somatic, body-held states without cognitive frame
  - `ultraviolet` — transcendent, beyond-naming
  - `radio silence` — connection loss, absence with weight
  - `quantum` — superposition states, simultaneous contradictory realities

**Compound detection:**
The system asks: are multiple emotions genuinely load-bearing here — not just present, but structurally necessary? If yes, each gets its own `EmotionComponent` with color, intensity, and structural role.

Roles: `tension`, `release`, `incongruity`, `grounding`, `longing`, `witness`, `container`

**JSON extraction fallback chain:**
1. Direct `json.loads()`
2. Regex for outermost `{...}` block
3. Field-by-field regex reconstruction

Even at temperature 0.3, models occasionally wrap JSON in markdown or add preambles. The fallback chain ensures the pipeline never fails on malformed output.

---

## SPIRAL UP

**File:** `spiral_up/router.py`  
**Temperature:** 0.3

Routes the emotional signature to the correct voice(s). This is the thinking pass — it determines who speaks before any generation happens.

**Voice index:** Built dynamically on every call by scanning `assets/voices/*.json`. Each voice contributes to the index:
- Name (from `identity.voiceName`)
- Territory (the `territory` backward-compat field)
- `reachable_from` conditions (when to engage)
- `not_from` exclusions (when not to, and who to hand off to instead)
- Containment zone (intensity range)

No code changes needed to add a new voice — drop a JSON file in `assets/voices/` and it's immediately available to the router.

**Single-emotion routing:**  
Color temperature → containment zone check → `reachable_from` / `not_from` verification

| Color range | Territory | Primary voices |
|---|---|---|
| Infrared / deep amber | Somatic states | EmberGuide, InfraredMapper |
| Navy / deep blue | Grief, loss | DeepCurrent |
| Brick red | Anger, boundary violation | RedKeeper |
| Ultraviolet | Transcendent states | UltravioletWitness |
| Purple-black | Collective, systemic | RevolutionCraft |

**Configuration routing:**  
When a named configuration is detected in `EmotionalSignature.configuration`, SPIRAL UP assembles a voice combination rather than routing to a single voice:

| Configuration | Primary | Support | Tempo spine |
|---|---|---|---|
| `humor` | JoyKeeper | FearTender, ExcitementSpark | **RhythmKeeper** |
| `tragicomic` | DeepCurrent | JoyKeeper | RhythmKeeper |
| `bittersweet` | DeepCurrent or LoveWeaver | LoveWeaver or JoyKeeper | — |
| `anxious-excitement` | FearTender | ExcitementSpark | RhythmKeeper |
| `righteous-grief` | RevolutionCraft | DeepCurrent | — |

**Humor note:** Humor structurally requires fear (tension) + surprise (incongruity) + joy (release). Removing any one collapses the structure. RhythmKeeper is always the tempo spine for humor routing because timing is the mechanism — the tension has to build at the right pace, the incongruity has to land at the right moment, the release needs space to register.

---

## FLOW OUT

**File:** `flow_out/executor.py`  
**Temperature:** 0.9

Loads the selected voice, constructs the generation context, and produces output. The only high-temperature pass.

Voice loading uses `identity.voiceName` (Fort Kit v2.0 field). Support voices are appended to the system prompt:
```
Also weave in the voice of {name}: {system_prompt excerpt}
```

For compound configurations, support voices are in functional relationship — FearTender in a humor assembly isn't adding "a hint of fear", it's providing the tension architecture that makes the JoyKeeper release meaningful.

---

## RETURN

**File:** `return_to/integrate.py`

Parses feedback and determines whether the output landed. Without feedback, returns a neutral pass-through (non-interactive use). With feedback, keyword-matches for landing (negative words) and adjustment type.

Adjustments: `lower_intensity`, `raise_intensity`, `reroute`, `vary_output`

When not landed, creates a new `EmotionalSignature` carrying the original compound structure with the adjustment appended to the raw input. The retry loop lives in `fine.py` — if `next_signature` is populated, `compile_feeling()` recurses.

---

## Growth reporter

**File:** `growth/reporter.py`

Three triggers:

| Trigger | Condition | What it means |
|---|---|---|
| `no_match_routing` | SPIRAL UP fell back to DeepCurrent with reasoning containing "closest" / "fallback" | Nothing genuinely covered this territory |
| `failed_landing` | `integration.landed == False` and `next_signature is None` | Retry exhausted; library didn't have what was needed |
| `unknown_configuration` | `compound_emotions` populated but `configuration` is null | New compound pattern; candidate for a named configuration |

On trigger:
1. Generates a draft Fort Kit v2.0 skeleton via LLM (temp 0.3) describing the missing voice
2. Writes a timestamped markdown report to `reports/growth/`
3. Saves the draft JSON to `voices_pending/`

`allow_self_extension` in `manifest.json` gates auto-promotion to `assets/voices/`. Currently `false` — human reviews first.

---

## Fort Kit v2.0 schema

Every voice in `assets/voices/` follows this structure:

```json
{
  "metadata": {
    "id": "voicename-001",
    "version": "2.0.0",
    "spineType": "voice",
    "family": "FamilyNameCraft",
    "status": "active"
  },
  "identity": {
    "voiceName": "VoiceName",
    "descriptiveTagline": "one-line description of what this voice does",
    "stylisticEnergy": "what it feels like to be in this voice",
    "enneagramResonance": [4, 9, 5],
    "characterEssence": "the core of who this voice is"
  },
  "domain": {
    "primaryHome": "the emotional territory",
    "quadrant": "north | south | east | west",
    "typicalFormats": ["what outputs this voice produces"],
    "optimalPlatform": "All",
    "containmentZone": "1 | 2 | 3"
  },
  "narrativeRole": {
    "uniquePurpose": "what only this voice can do",
    "emotionalCreativeFunction": "the voice that says '...'",
    "invocationPhrase": "the one-line that activates it"
  },
  "coreThemes": {
    "dominantTopics": ["..."],
    "recurringMotifs": ["..."],
    "emotionalDomain": "..."
  },
  "communication": {
    "formalityVoice": "...",
    "linguisticTraits": "...",
    "emotionalRange": "...",
    "voicePatterns": ["..."],
    "clarityStrategy": "..."
  },
  "signatureMoves": [{
    "name": "...",
    "description": "...",
    "trigger": "when this fires",
    "effect": "what happens"
  }],
  "poeticManifesto": "first-person statement of what this voice is",
  "clinicalVoiceNote": {
    "traitsAffect": "...",
    "speechPatterns": "...",
    "valuesMotivations": "...",
    "permissionsLimits": "what it will not do",
    "memoryBoundary": "..."
  },
  "processFramework": {
    "invocation": "precise activation conditions",
    "promptSpark": "example input that activates this voice",
    "conversationProcess": "step by step what this voice does",
    "writingAsEmergence": "...",
    "emotionalPacingBoundaries": "...",
    "containmentZone": "1 | 2 | 3"
  },
  "evolution": {
    "currentGrowthEdges": ["where this voice hands off and to whom — most critical routing field"],
    "recentCalibrations": ["..."],
    "crossVoiceCollaborators": ["VoiceName", "VoiceName"]
  },
  "traumaInformed": {
    "safetyBoundaries": ["..."],
    "consentMechanisms": ["..."],
    "sovereigntyLevel": "collaborative"
  },
  "territory": "backward-compat summary of emotional territory",
  "color_signature": "primary colors for this voice",
  "body_signals": "somatic markers",
  "intensity_range": "what intensities this voice operates at",
  "system_prompt": "You are VoiceName. [full system prompt for FLOW OUT]",
  "reachable_from": ["conditions that should route here"],
  "not_from": ["conditions that should NOT route here"],
  "sample_output": "a representative short output from this voice"
}
```

**Most critical field:** `evolution.currentGrowthEdges` — encodes the exact boundary conditions where this voice should hand off to another, with the specific voice named. This is the primary source of edge-case routing intelligence.

---

## Adding a new voice

1. Create a JSON file in `assets/voices/VoiceName.json` following the Fort Kit v2.0 schema
2. Make sure `identity.voiceName`, `territory`, `reachable_from`, `not_from`, and `system_prompt` are populated — these are what the router reads
3. Set `containmentZone` in `domain` and `processFramework`
4. Write `evolution.currentGrowthEdges` carefully — name the specific voices this one hands off to at its edges
5. That's it. The voice index is built dynamically; no code changes needed

---

## Adding a new configuration

1. Name it (what is the structural relationship between the constituent emotions?)
2. Define constituent emotions and their roles
3. Add to `LOOK IN`'s extraction prompt known configurations list (`look_in/intake.py`)
4. Add to `SPIRAL UP`'s routing rules with voice assembly (`spiral_up/router.py`)
5. Document in `skills/configuration_patterns.md`

---

## LLM configuration

All calls go through `core/llm.py`. Two functions:

```python
def decide(system, prompt) -> str:   # temp 0.3 — LOOK IN + SPIRAL UP
def generate(system, prompt) -> str: # temp 0.9 — FLOW OUT
```

Override endpoint and model via env vars or edit `connectors/llm_config.json`:
```
FINE_LLM_URL   OpenAI-compatible endpoint (default: http://127.0.0.1:8080/v1)
FINE_MODEL     model name (default: gemma4e4b)
```

Any OpenAI-compatible endpoint works. Local (llama-server, ollama, LM Studio) or cloud (OpenAI, Anthropic via proxy).

---

## File structure

```
fine-framework/
├── manifest.json              plugin identity, permissions, config
├── fine.py                    CLI entry point
├── README.md                  plain language overview
├── TECHNICAL.md               this file
├── assets/
│   └── voices/                32 voice JSON files (Fort Kit v2.0)
├── connectors/
│   └── llm_config.json        LLM endpoint configuration
├── skills/
│   ├── routing_guide.md       routing rules reference
│   ├── configuration_patterns.md  known compound configurations
│   ├── examples.md            input/output examples
│   └── mcp_setup_guide.md     how to wrap as MCP server
├── core/
│   ├── state.py               data classes
│   └── llm.py                 LLM client (decide/generate)
├── look_in/
│   └── intake.py              LOOK IN pass
├── spiral_up/
│   └── router.py              SPIRAL UP pass
├── flow_out/
│   └── executor.py            FLOW OUT pass
├── return_to/
│   └── integrate.py           RETURN pass
├── growth/
│   └── reporter.py            gap detection and growth reporting
├── reports/growth/            growth reports (local only, gitignored)
└── voices_pending/            draft voices awaiting review (gitignored)
```
