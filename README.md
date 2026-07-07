# TURVIS Studio / Cinematic OS

**Local-first AI Adventure Documentary Production System**

TURVIS Studio is a local-first production workflow for creating cinematic adventure documentaries with structured project data, footage memory, story beats, Remotion timelines, and QC.

This is not a prompt collection.
It is an AI-assisted documentary studio architecture.

---

## Core Principle

> Local first.  
> API optional.  
> Projects are data.  
> Apps are engines.  
> Remotion renders locally.

---

## What It Does Now

Current Build Mode pipeline:

```text
Project Wizard
↓
project.yaml
↓
Project Pipeline
↓
Validate
↓
Footage Analyzer
↓
Review Queue
↓
Director Handoff
↓
Director Prep
↓
Story Beats / Storyboard
↓
Timeline Draft
↓
Remotion Bridge
↓
Remotion Sync
↓
QC Report
↓
Preview / Render
```

---

## Quickstart

### 1. Create a project

```bash
python apps/turvis-studio/turvis.py create \
  --title "Kazakhstan Mangystau Documentary" \
  --id kazakhstan-mangystau-documentary \
  --type documentary \
  --country Kazakhstan \
  --region Mangystau \
  --destination "Bozzhyra" \
  --duration 240 \
  --aspect "16:9"
```

This creates:

```text
projects/kazakhstan-mangystau-documentary/
├── project.yaml
├── narration.md
└── README.md
```

---

### 2. Edit project.yaml

Set your footage folder:

```yaml
paths:
  footage: D:/Your/Footage/Folder
  keyframes: assets/kazakhstan-mangystau-documentary/keyframes
  memory: knowledge/footage/kazakhstan-mangystau-documentary
  narration: projects/kazakhstan-mangystau-documentary/narration.md
  director_handoff: projects/kazakhstan-mangystau-documentary/director-handoff.md
```

---

### 3. Paste narration

Edit:

```text
projects/kazakhstan-mangystau-documentary/narration.md
```

---

### 4. Run the full pipeline

```bash
python apps/turvis-studio/turvis.py pipeline \
  --project-folder projects/kazakhstan-mangystau-documentary \
  --include-review
```

Generated outputs include:

```text
director-prep.md
story-beats.md
storyboard.md
timeline-draft.md
timeline-draft.json
timeline.remotion.json
qc-report.md
```

The pipeline also syncs the project timeline into:

```text
remotion/src/data/turvis.timeline.ts
```

---

### 5. Preview in Remotion

```bash
python apps/turvis-studio/turvis.py preview --install
```

After first install:

```bash
python apps/turvis-studio/turvis.py preview
```

---

### 6. Render

```bash
python apps/turvis-studio/turvis.py render
```

Output:

```text
remotion/out/turvis-documentary.mp4
```

---

## Main Apps

```text
apps/
├── turvis-studio/       unified CLI
├── project-wizard/      project creation
├── project-pipeline/    full local pipeline
├── footage-analyzer/    footage scan, keyframes, memory, search, handoff
├── director-prep/       director prep package
├── director-engine/     story beat and storyboard draft
├── timeline-builder/    timeline draft generation
├── remotion-bridge/     timeline.remotion.json builder
├── remotion-sync/       sync project timeline into Remotion app
├── qc-engine/           project output validation
└── render-runner/       Remotion preview/render runner
```

---

## Architecture Rule

```text
apps/       universal engines
projects/   active project data
examples/   sample projects only
docs/       system manuals
knowledge/  reusable memory
remotion/   local render engine
```

If a project name appears inside engine code, the architecture is wrong.

---

## Remotion

The Remotion app is universal.
It reads:

```text
remotion/src/data/turvis.timeline.ts
```

That file is generated from each project's:

```text
projects/[project]/timeline.remotion.json
```

---

## Target Style

TURVIS documentaries should feel closer to:

- Netflix Documentary
- BBC Earth
- National Geographic
- Patagonia Films
- DJI cinematic aerial films

They should not feel like:

- Travel vlog
- Random montage
- Low-end tourism promotion

---

## Rule Zero

> Good is not enough.  
> Only cinematic.
