# F.I.N.E. — Examples

These show what the system actually does across different inputs, output types, and emotional configurations. Outputs are representative — your LLM will produce its own variation.

---

## Grief — prose output

**Input:**
```
three years and I still don't know how to talk about it
I thought it would get easier and in some ways it has
but then something small happens and it's like no time has passed at all
```

**Terminal:**
```
[LOOK IN]   color: deep navy | intensity: 7/10 | tags: grief, time, unresolved

[SPIRAL UP] voice: DeepCurrent | three years is still early for this kind of loss

[FLOW OUT]  generating prose...
```

**Output:**
```
Three years is not a long time. I know we say it differently — we say time heals,
we say it gets easier, and in the body of it, that is sometimes true. But grief
does not move in one direction. It spirals. You can be further from it and closer
to it in the same week. The small things — the smell of something, a particular
quality of afternoon light — they don't observe the timeline you've built.

This is not regression. This is grief doing what grief does: returning to what it
has not yet finished. Three years means you've carried it long enough that the
carrying has become familiar. It doesn't mean it's done. It means you've gotten
stronger — and the weight didn't get lighter, you did.
```

---

## Anger — boundary output

**Input:**
```
I need to tell my manager I can't keep doing this
every week it's more on my plate and nothing comes off
I've said something once and it didn't change anything
```

**Terminal:**
```
[LOOK IN]   color: brick-dust red | intensity: 7/10 | tags: boundary, overload, unheard

[SPIRAL UP] voice: RedKeeper | clear violation with specific pattern — boundary script needed

[FLOW OUT]  generating boundary...
```

**Output:**
```
I need to have a direct conversation with you about my workload.

Over the past [timeframe], my responsibilities have expanded significantly without
any corresponding reduction elsewhere. When I raised this [previously], nothing
changed. I need that to change now.

Here's what I need specifically: [list the specific items]. I cannot continue
absorbing additional work without something coming off my plate. This isn't a
preference — it's a capacity issue.

I want to work with you on a solution. I'm not willing to continue at this level
without one.
```

---

## Humor — poem output (compound routing)

**Input:**
```
my therapist asked me what my inner child needs
and my inner child needs about forty thousand dollars
and a nap
and maybe for capitalism to end
```

**Terminal:**
```
[LOOK IN]   color: warm gold over charcoal | intensity: 5/10 | tags: absurdist, exhausted, self-aware
            config: humor | compound: 3 emotions
            — fear(tension, intensity 4), surprise(incongruity, intensity 6), joy(release, intensity 5)

[SPIRAL UP] voice: JoyKeeper + FearTender, ExcitementSpark | spine: RhythmKeeper | humor config

[FLOW OUT]  generating poem...
```

**Output:**
```
My inner child
needs forty thousand dollars

She needs a nap that lasts
approximately one geological era

She needs someone to tell her
that the thing she is feeling
has a name
that is longer than "fine"

She has been very patient
she has been doing her best
she has been capitalisming
as hard as she can

She would like to stop now
if that's okay
if there's a form for that
she will fill it out
```

---

## Unknown / inarticulate — song output

**Input:**
```
I don't know what I'm feeling
something is wrong but I can't get to it
I've been numb for like three weeks and I don't know
if that's better or worse than the thing before
```

**Terminal:**
```
[LOOK IN]   color: flat grey-green | intensity: 5/10 | shadow: infrared | tags: numb, dissociated, unreachable

[SPIRAL UP] voice: InfraredMapper + EmberGuide | somatic numbness with infrared shadow

[FLOW OUT]  generating song...
```

**Output:**
```
Something below the words
Something before the name
I have been standing at the edge of it
for three weeks now

The numb is not nothing
The numb is the body
deciding to hold the door

I don't need to know what it is
I just need to know
it knows where to find me

I am here
I am not going anywhere
I am standing at the edge
with my hands open
```

---

## Collective / systemic anger — protocol output

**Input:**
```
I'm so tired of being the only one in every room who sees it
it's not just me being sensitive it's an actual pattern
and I'm exhausted from trying to explain it to people who benefit from not seeing it
```

**Terminal:**
```
[LOOK IN]   color: purple-black | intensity: 8/10 | tags: systemic, isolation, exhausted, witness

[SPIRAL UP] voice: RevolutionCraft + DeepCurrent | systemic isolation with grief dimension

[FLOW OUT]  generating protocol...
```

**Output:**
```
Protocol: When you are the only witness in the room

Step 1 — Name what is happening internally
You are not wrong. You are early. There is a difference. Acknowledge the exhaustion
of being ahead of a room that has incentives to stay behind.

Step 2 — Separate the seeing from the convincing
Your job is not to make others see. Your job is to see accurately and act from
what you know. These are different tasks. You have been doing both. You can
stop doing one.

Step 3 — Locate your people
You are not the only one who sees this. Find the ones who already know. This
is not about building a coalition to convince the unconvinced — it's about
finding the people you don't have to spend energy explaining to.

Step 4 — Choose your investment
You have a finite amount of energy to spend on this. Decide what it goes toward.
Explaining to people who benefit from not understanding is a low-return investment.
Acting from your understanding — with people who share it — is not.

Step 5 — Rest is political
The exhaustion you feel is accurate. It is the weight of carrying knowledge in a
room that refuses it. Rest is not abandoning the work. It is what makes the work
sustainable.
```

---

## Bittersweet — song output (compound routing)

**Input:**
```
my kid started kindergarten today
I watched her walk in and she didn't look back
and I was so proud I couldn't breathe
and also I cried in the parking lot for twenty minutes
```

**Terminal:**
```
[LOOK IN]   color: warm gold over navy | intensity: 8/10 | tags: pride, grief, milestone, love
            config: bittersweet | compound: 2 emotions
            — joy(love+pride, intensity 8), grief(letting go, intensity 7)

[SPIRAL UP] voice: LoveWeaver + DeepCurrent | bittersweet — joy slightly heavier

[FLOW OUT]  generating song...
```

**Output:**
```
She walked in and didn't look back
and I am so proud of her
for that

For the way she went
without a backward glance
the way I raised her to

The parking lot held me
for twenty minutes
while I finished

This is what it costs
to raise someone brave —
you watch them leave
and call it good

I would not change
a single thing
about the way she walked away from me

and I reserve the right
to cry about it anyway
```

---

## Notes on variation

The output you get will differ from these examples — different LLMs generate differently, and that's by design. The FLOW OUT pass runs at temperature 0.9. The voice and routing will be consistent; the exact language will vary. That's not a bug. Emotional expression has range. The voice family defines the register; the generation fills it.

If it doesn't land, pass feedback with `--feedback` and rerun. The RETURN pass will adjust and recompile.
