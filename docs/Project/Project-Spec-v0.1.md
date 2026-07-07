# Project Spec v0.1

Version: v0.1  
Project: TURVIS Studio

---

## 1. Purpose

`project.yaml` is the single source of truth for a TURVIS production project.

Apps should read this file instead of relying on hard-coded project names or destination-specific commands.

---

## 2. Required File

Every project folder must contain:

```text
project.yaml
```

Example:

```text
projects/current/project.yaml
projects/mangystau-day3/project.yaml
projects/japan-ski/project.yaml
```

---

## 3. Minimal Structure

```yaml
project:
  id: current-project
  title: Untitled Project
  type: documentary
  status: draft

output:
  aspect_ratio: "16:9"
  resolution: "3840x2160"
  target_duration_seconds: 240
  language: ko

style:
  references:
    - Netflix Documentary
    - BBC Earth
    - National Geographic
  mood:
    - cinematic
    - quiet
    - immersive

locations:
  country: unknown
  region: unknown
  destination: unknown
  route: unknown

paths:
  footage: assets/current/raw
  keyframes: assets/current/keyframes
  memory: knowledge/footage/current
  narration: projects/current/narration.md
  director_handoff: projects/current/director-handoff.md

rules:
  generate_audio: false
  generate_music: false
  generate_sound_effects: false
  local_first: true
```

---

## 4. Project Types

Allowed project types:

- documentary
- brand-film
- reels
- shorts
- youtube
- presentation
- product-promo

---

## 5. Path Rules

All paths are relative to repository root unless absolute paths are provided.

Apps should support both:

```text
projects/current/project.yaml
```

and

```text
D:/Turvis/projects/current/project.yaml
```

---

## 6. App Rule

Apps should accept:

```bash
--project-folder projects/current
```

or:

```bash
--project-spec projects/current/project.yaml
```

Apps should avoid project-specific required flags whenever possible.

---

## 7. Final Rule

> A project is data.  
> An app is an engine.  
> The engine reads the data.  
> The data never rewrites the engine.
