# Footage Analysis Runbook

Version: v0.1  
Project: TURVIS Adventure Memory Engine

---

## 1. Purpose

This runbook explains how to analyze a batch of raw footage and create Adventure Memory records.

It is designed for Cowork, Codex, or any AI-assisted workflow that can inspect footage files, thumbnails, metadata, or extracted frames.

---

## 2. Recommended Workflow

```text
Step 1 — Create project folder
Step 2 — Place raw footage in source folder
Step 3 — Generate thumbnails or keyframes
Step 4 — Run Footage Analyst
Step 5 — Create Markdown memory files
Step 6 — Create JSON memory files
Step 7 — Review uncertain clips
Step 8 — Build batch summary
Step 9 — Director uses memory for edit planning
```

---

## 3. Folder Convention

Recommended structure:

```text
assets/
  mangystau/
    day3/
      raw/
      selected/
      thumbnails/

knowledge/
  footage/
    mangystau/
      day3/
        MG-D3-0001.md
        MG-D3-0001.json
```

---

## 4. Keyframe Strategy

When full video analysis is expensive, extract representative frames:

- first frame
- 25% point
- 50% point
- 75% point
- final frame

For drone movement, also inspect motion direction if possible.

---

## 5. Minimum Metadata

Each clip must have at least:

- clip_id
- original_filename
- asset_path
- visible description
- camera type
- shot type
- movement
- emotion tags
- story tags
- scores
- best usage
- needs_review flag

---

## 6. Review Levels

### Auto Approved

Clear location, stable image, obvious story value.

### Needs Human Review

Uncertain location, unknown landmark, unclear story value, possible duplicate.

### Avoid

Poor quality, severe shake, no meaningful story value, or unusable exposure.

---

## 7. Batch Summary File

Each analyzed folder should include:

```text
knowledge/footage/[project]/[episode]/batch-summary.md
```

The summary must include:

- total clips analyzed
- strongest clips
- hero shots
- journey shots
- texture shots
- scale shots
- ending candidates
- avoid clips
- needs review clips

---

## 8. Director Handoff

After AME analysis, the Documentary Director should search the memory files before building the storyboard.

The Director must not blindly use filenames.

---

## 9. Final Rule

Analyze once. Reuse forever.
