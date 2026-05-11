# F.I.N.E. Routing Guide

## How SPIRAL UP routes emotional signatures

### Color temperature heuristics

| Color range | Territory | Primary voices |
|---|---|---|
| Infrared / deep amber | Somatic, body-held states | EmberGuide, InfraredMapper |
| Navy / deep blue | Grief, weight, loss | DeepCurrent |
| Brick red / burgundy | Anger, betrayal, boundary | RedKeeper, RedWitness |
| Ultraviolet / white | Transcendent, beyond-naming | UltravioletWitness |
| Cornflower blue | Loneliness, quiet sadness | DeepCurrent |
| Gold / warm amber | Joy, relief, gratitude | JoyKeeper, ReliefBreath |
| Purple-black | Collective rage, systemic | RevolutionCraft |
| Earth tones | Grounding, body, somatic | EmberGuide |

### Containment zones

- Zone 1 — all intensities (1-10)
- Zone 2 — mid to high intensity (4-10)  
- Zone 3 — high intensity only (5-10); collective/systemic voices

### Single-emotion routing rules

1. Match color temperature first
2. Check `reachable_from` conditions
3. Verify intensity falls within containment zone
4. Check `not_from` exclusions — if triggered, route to the named handoff voice instead
5. Primary voice does the core work; 1-2 support voices add texture only

### Compound emotion routing

When `compound_emotions` is populated, route to voice assemblies:

| Configuration | Primary | Support | Tempo spine |
|---|---|---|---|
| `humor` | JoyKeeper | FearTender, ExcitementSpark | **RhythmKeeper** |
| `tragicomic` | DeepCurrent | JoyKeeper | RhythmKeeper |
| `bittersweet` | DeepCurrent or LoveWeaver | LoveWeaver or JoyKeeper | — |
| `anxious-excitement` | FearTender | ExcitementSpark | RhythmKeeper |
| `righteous-grief` | RevolutionCraft | DeepCurrent | — |

**Humor note:** RhythmKeeper is always the tempo spine for humor. Timing is the mechanism — fear builds tension, surprise delivers incongruity, joy releases. The timing between those three is what makes it land.

### Default fallback

If nothing genuinely fits: DeepCurrent (grief/witness territory is broadly applicable). A fallback route triggers a growth report.
