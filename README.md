# F.I.N.E. — Framework for Interpreting Nonliteral Expression

> "I'm fine." is always a complete sentence. It is rarely a complete truth. F.I.N.E. reads the gap.

---

## What is this

You know when you're feeling something and you can't quite name it? Or you know exactly what you're feeling but you don't know what to *do* with it?

F.I.N.E. is a tool you give that to.

You type what you're carrying — messy, half-formed, a wall of text at 2am, whatever — and it figures out what's actually going on underneath the words. Then it gives it back to you in a form that helps. A song. A poem. A script for a hard conversation. A set of steps to actually process it.

It's not a chatbot. It doesn't ask you questions. You put the feeling in, you get something useful out.

---

## What you get out

You pick the format:

- **song** — something lyrical that holds the feeling in rhythm and sound *(default)*
- **poem** — a shorter, more shaped piece
- **prose** — paragraphs that say the thing you couldn't say
- **protocol** — actual steps for working through what you're feeling
- **boundary** — language for a hard conversation you need to have with someone

---

## A real example

Someone typed this:

```
everything is fine and I hate that everything is fine and I don't know
what I'm supposed to do with that
```

F.I.N.E. read it, noticed the grief and the absurdity sitting right next to each other, and gave back this poem:

```
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
```

---

## More examples

See `skills/examples.md` for six full examples — anger, grief, humor, not knowing what you're feeling, collective exhaustion, and the specific kind of crying you do in a parking lot after dropping your kid off at kindergarten for the first time.

---

## How it works (the short version)

When you give it input, it runs four steps:

1. **Reads the feeling** — finds the emotional color, where it lives in the body, how intense it is, whether multiple feelings are working together
2. **Picks the right voice** — routes to one of 32 emotional voice families, or a combination if the feeling is layered
3. **Generates the output** — writes in that voice at the format you asked for
4. **Checks if it landed** — if it didn't, adjusts and tries again

The 32 voices each cover specific emotional territory. Grief sounds different from guilt. Anger at a system is different from anger at a person. Shame is different from sadness. The system knows the difference and routes accordingly.

---

## Setup

You need Python and an AI model running somewhere. That's it.

```bash
git clone https://github.com/TheFortThatHolds/fine-framework
cd fine-framework
pip install openai
```

Then tell it where your AI model is:

```bash
# If you're running a local model (ollama, LM Studio, etc.)
export FINE_LLM_URL="http://127.0.0.1:11434/v1"
export FINE_MODEL="your-model-name"

# If you're using OpenAI
export FINE_LLM_URL="https://api.openai.com/v1"
export FINE_MODEL="gpt-4o"
```

---

## Using it

```bash
# Basic — gives you a song by default
python fine.py "I don't know what I'm feeling but something is wrong"

# Pick a format
python fine.py "I am so angry I can't breathe" --target poem
python fine.py "I need to tell my manager I can't keep doing this" --target boundary
python fine.py "I can't stop thinking about my dad" --target prose

# If it didn't quite land, add feedback
python fine.py "I keep circling the same grief" --target prose --feedback "too fast, needs more space"
```

---

## The voice library

There are 32 voices. Each one covers a specific slice of the emotional landscape.

A few:

| Voice | What it handles |
|---|---|
| DeepCurrent | Grief, loss, the weight that doesn't lift |
| FearTender | Fear — tells the difference between real threat and anxious spiral |
| JoyKeeper | Full-body joy, permission to actually feel it |
| RedKeeper | Anger at a specific thing — clear, grounded, protective |
| RevolutionCraft | When what you're feeling isn't just personal — it's part of something bigger |
| ShameHistorian | The "I am bad" feeling, not the "I did something bad" feeling |
| EmberGuide | When your body knows something your brain hasn't caught up to yet |
| RhythmKeeper | Pacing — slows things down to the speed the feeling actually moves at |
| SilenceBearer | The kind of alone that has weight |
| QuantumFamily | When you feel two completely opposite things at the same time and both are true |

All 32 are in `assets/voices/` as plain JSON files. You can read them, modify them, or add your own.

---

## When the library doesn't cover something

If F.I.N.E. hits a feeling it doesn't have the right voice for, it writes a report in `reports/growth/` and drafts a sketch of what that missing voice might look like. You review it, decide if the territory is real, and add it to the library if it is.

The system documents its own gaps. That's how it grows.

---

## Using it with Claude Desktop or other AI tools

F.I.N.E. can be wrapped as an MCP tool so you can call it from Claude Desktop, Cursor, or any AI app that supports tool use. You set that up yourself — full instructions in `skills/mcp_setup_guide.md`. Your install, your data, your control.

---

## The idea behind it

Most people are taught to treat emotions as noise — the thing you manage so you can get back to the real work. F.I.N.E. is built on the opposite assumption: emotion is the infrastructure. It's the layer that tells any living system what matters, what to protect, what's worth the cost.

"I'm fine" is the most common nonliteral expression in the language. It almost never means what it says. F.I.N.E. reads what it actually means.

---

## Going deeper

→ [TECHNICAL.md](TECHNICAL.md) — pipeline architecture, data structures, schema spec, how to add voices and configurations

---

## License

MIT. Use it, fork it, build on it. Add voices. If you find emotional territory the library doesn't cover, the growth reporter was built for exactly that.
