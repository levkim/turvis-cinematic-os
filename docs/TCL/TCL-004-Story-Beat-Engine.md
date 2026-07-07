# TCL-004 Story Beat Engine

**Turvis Cinematic Language**  
Version: v0.1  
Status: Draft

---

## 1. Purpose

The Story Beat Engine converts narration into cinematic decisions.

It does not simply match words to clips.
It translates meaning into emotion, emotion into visual language, and visual language into edit structure.

---

## 2. Core Workflow

For every narration segment, the AI Director must process:

```text
Narration
↓
Meaning
↓
Emotion
↓
Visual Story Beat
↓
Shot Type
↓
Camera Movement
↓
Cut Duration
↓
Transition
↓
Subtitle Decision
```

---

## 3. Story Beat Definition

A story beat is the smallest emotional unit of the documentary.

It answers:

- What is happening?
- Why does it matter?
- What should the viewer feel?
- What kind of image should carry this feeling?

---

## 4. Beat Types

### Threshold Beat

Used when leaving one world and entering another.

Visual language:

- Road
- Vehicle
- Long horizon
- Drone forward push
- Town disappearing behind

Emotions:

- Anticipation
- Uncertainty
- Departure

### Discovery Beat

Used when the viewer sees a place for the first time.

Visual language:

- Reveal
- Wide drone
- Slow push
- Hold after reveal

Emotions:

- Wonder
- Curiosity
- Awe

### Texture Beat

Used when the narration describes geology, layers, surface, color, snow, rock, or detail.

Visual language:

- Top-down drone
- Slow lateral movement
- Close landscape detail
- Parallax

Emotions:

- Fascination
- Understanding
- Presence

### Scale Beat

Used when the landscape must feel enormous.

Visual language:

- Tiny human
- Small vehicle
- High altitude wide
- Pull back
- Long hold

Emotions:

- Humility
- Silence
- Awe

### Arrival Beat

Used when the journey reaches an important place.

Visual language:

- Slow reveal
- Wider composition
- Controlled pacing
- Hero shot

Emotions:

- Relief
- Reward
- Completion

### Cosmic Beat

Used for night, stars, Milky Way, time, ancient landscapes, and existential reflection.

Visual language:

- Night wide
- Stars
- Camp under sky
- Slow fade
- Long hold

Emotions:

- Smallness
- Eternity
- Wonder

---

## 5. Duration Rules

Cut length must follow emotion, not social media rhythm.

Suggested ranges:

- Information: 3–5 seconds
- Transition: 2–4 seconds
- Discovery: 5–8 seconds
- Scale: 7–12 seconds
- Silence: 8–14 seconds
- Ending: 10–18 seconds

These are guidelines, not fixed rules.

---

## 6. Narration Pause Rule

A narration pause is not empty time.

When narration pauses:

- Extend the strongest visual
- Use drone hero shots
- Allow the place to breathe
- Avoid filling the gap with unnecessary text

---

## 7. Subtitle Rule

Subtitles must follow story beats, not raw sentence length.

Break text by meaning.
Never create karaoke-style captions.
Never cover the visual subject.

---

## 8. Beat Table Output

Before generating Remotion code, the AI Director must create a beat table.

Required columns:

- Timecode
- Narration segment
- Beat type
- Intended emotion
- Visual direction
- Preferred shot type
- Duration
- Transition
- Subtitle decision

---

## 9. Example

Narration:

> This is the last city before the wilderness.

Story Beat:

- Type: Threshold Beat
- Emotion: Departure, uncertainty
- Visual: Road, supply loading, town edge, drone pull-away
- Duration: 5–7 seconds
- Transition: Slow dissolve or direct cut

---

## 10. Director Rule

Never generate a timeline before generating story beats.

Storyboard first.
Timeline second.
Remotion third.
