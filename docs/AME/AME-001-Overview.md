# AME-001 Adventure Memory Engine Overview

**Adventure Memory Engine (AME)**  
Version: v0.1  
Status: Draft  
Project: TURVIS Cinematic OS

---

## 1. Purpose

Adventure Memory Engine, or AME, converts raw footage into searchable cinematic memory.

TURVIS does not treat footage as anonymous files.
Each clip becomes a memory object with location, emotion, story purpose, camera language, quality score, and best usage.

This allows the Documentary Director to search for meaning, not filenames.

---

## 2. Core Idea

Traditional editing starts with files:

```text
clip001.mp4
clip002.mp4
clip003.mp4
```

TURVIS editing starts with memory:

```text
Bozzhyra / Drone Orbit / Golden Hour / Wonder / Arrival / Hero Shot
```

The Director should not ask:

> Which file should I use?

The Director should ask:

> Which memory best carries this story beat?

---

## 3. AME Pipeline

```text
Raw Footage
↓
Footage Analyst
↓
Clip Metadata
↓
Emotion Tags
↓
Story Tags
↓
Camera Tags
↓
Quality Score
↓
Adventure Memory
↓
Director Search
↓
Remotion Timeline
```

---

## 4. Memory Object

Each clip should produce two memory records:

1. Human-readable Markdown file
2. Machine-readable JSON file

Example:

```text
knowledge/footage/mangystau/day3/MG-D3-0001.md
knowledge/footage/mangystau/day3/MG-D3-0001.json
```

---

## 5. What AME Must Capture

Each clip memory should capture:

- Clip ID
- Original filename
- Project / destination / region
- Location
- GPS if known
- Shot type
- Camera type
- Camera movement
- Time of day
- Weather
- Light quality
- Landscape type
- Human presence
- Vehicle presence
- Emotion tags
- Story beat tags
- Best usage
- Quality scores
- Director notes

---

## 6. Director Search Examples

The Documentary Director should be able to search:

```text
Find a lonely golden-hour drone pull-back for an isolation beat.
```

```text
Find a high-quality geological texture shot for Kyzylkup.
```

```text
Find a hero shot for a cosmic ending.
```

```text
Find a vehicle journey shot that feels like leaving civilization.
```

---

## 7. AME Is a Company Asset

AME is not temporary project metadata.

It is the long-term cinematic memory of TURVIS.

Over time, AME should contain the visual intelligence of:

- Mangystau
- Kyrgyzstan
- Japan ski regions
- Kazakhstan
- Georgia
- Patagonia
- Alaska
- Future expedition footage

---

## 8. Rule

> Raw footage is storage.  
> Tagged footage is memory.  
> Searchable memory is creative power.
