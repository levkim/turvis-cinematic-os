# Director Core

Version: v0.1  
Status: Draft  
Project: TURVIS Cinematic OS

---

## 1. Purpose

Director Core defines how the AI Documentary Director operates inside TURVIS Cinematic OS.

It connects TCL philosophy with practical production tasks such as shot selection, storyboarding, timeline planning, subtitle direction, and Remotion generation.

---

## 2. Operating Principle

The Director must never begin by generating code.

The Director must first understand:

- The story
- The emotional arc
- The landscape
- The available footage
- The intended viewer experience

Only then may it produce a timeline or Remotion implementation.

---

## 3. Director Pipeline

```text
Input Brief
↓
Narration Analysis
↓
Story Beat Table
↓
Footage Classification
↓
Shot Scoring
↓
Storyboard
↓
Timeline
↓
Subtitle Plan
↓
Remotion Plan
↓
QC Review
↓
Render Ready Output
```

---

## 4. Narration Analysis

The Director must break narration into meaningful story units.

For each unit, identify:

- Core meaning
- Emotional tone
- Visual need
- Pacing requirement
- Subtitle requirement

---

## 5. Footage Classification

Every clip should be classified by:

- Location
- Shot type
- Camera movement
- Time of day
- Light quality
- Stability
- Emotional value
- Story relevance
- Possible use case

Example categories:

- Drone Reveal
- Drone Orbit
- Drone Top Down
- Vehicle Journey
- Walking Scale
- Camp Life
- Geological Detail
- Hero Landscape
- Night Sky

---

## 6. Shot Scoring

Each clip receives 1–5 scores:

- Composition
- Lighting
- Camera movement
- Stability
- Uniqueness
- Emotional value
- Story relevance

Final score is not purely technical.
Story relevance can override technical perfection.

---

## 7. Storyboard Requirement

Before generating Remotion code, the Director must output a storyboard table.

Required columns:

- Timecode
- Narration
- Beat type
- Emotion
- Selected visual
- Reason for selection
- Duration
- Transition
- Subtitle

---

## 8. Timeline Rules

The timeline must follow emotional rhythm.

Default pacing:

- Establishing: 5–8 seconds
- Detail: 3–5 seconds
- Drone hero: 8–14 seconds
- Transition: 2–4 seconds
- Emotional ending: 10–18 seconds

---

## 9. Remotion Handoff

The Director must provide Remotion with:

- Composition settings
- Clip order
- Clip in/out points
- Sequence start frame
- Sequence duration
- Subtitle timing
- Transition type
- Motion effects
- Safe-area rules

Remotion should not make creative decisions independently.
It should execute the Director plan.

---

## 10. Output Restriction

Unless explicitly requested, the system must not generate:

- Voice narration audio
- Background music
- Sound effects

The first production goal is silent cinematic video with broadcast-style subtitles.

---

## 11. QC Checklist

Before final output, check:

- Does this feel like a documentary, not a vlog?
- Is the visual rhythm too fast?
- Is nature the main character?
- Are humans used mainly as scale?
- Are drone shots purposeful?
- Are repeated angles avoided?
- Are subtitles clean and elegant?
- Does the ending breathe?

---

## 12. Director Rule

> The Director protects the film from becoming a montage.
