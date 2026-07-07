# Footage Analyzer CLI

Version: v0.7  
Project: TURVIS Studio / Adventure Memory Engine

---

## Purpose

Footage Analyzer CLI is the first local-first executable tool for TURVIS Studio.

It scans a local footage folder, extracts basic video metadata, extracts review keyframes, creates placeholder Adventure Memory records, prepares clips for later AI-assisted or human review, searches reviewed footage memory, validates project configuration, and creates Director handoff packages.

This tool does not require paid AI API calls.

---

## Architecture Rule

Apps do not know projects.

Projects are data.

The preferred workflow is now:

```bash
--project-folder projects/current
```

The app reads:

```text
projects/current/project.yaml
```

---

## What v0.7 Does

- Reads project configuration from `project.yaml`
- Validates required project configuration before execution
- Scans a local folder for video files
- Creates stable TURVIS clip IDs
- Extracts basic metadata with `ffprobe` if available
- Extracts review keyframes with `ffmpeg`
- Creates Markdown memory files
- Creates JSON memory files
- Creates a batch summary
- Marks clips as `needs_review: true`
- Generates a review queue from clips needing visual review
- Searches Adventure Memory by query, emotion, story, shot type, location, score, and hero flag
- Creates a Director-ready footage handoff grouped by story purpose

---

## Requirements

- Python 3.10+
- FFmpeg installed and available in PATH

Check FFmpeg:

```bash
ffmpeg -version
ffprobe -version
```

---

## Step 0 — Create Project Folder

Create or copy a project spec:

```bash
mkdir -p projects/current
cp templates/project.yaml projects/current/project.yaml
```

Edit:

```text
projects/current/project.yaml
```

Set:

```yaml
paths:
  footage: D:/Your/Footage/Folder
  keyframes: assets/current/keyframes
  memory: knowledge/footage/current
  director_handoff: projects/current/director-handoff.md
```

---

## Step 1 — Validate Project

```bash
python apps/common/validate_project.py \
  --project-folder projects/current
```

Strict path checking:

```bash
python apps/common/validate_project.py \
  --project-folder projects/current \
  --strict-paths
```

---

## Step 2 — Analyze Footage From Project Folder

Preferred universal command:

```bash
python apps/footage-analyzer/analyze_project.py \
  --project-folder projects/current
```

Optional prefix override:

```bash
python apps/footage-analyzer/analyze_project.py \
  --project-folder projects/current \
  --prefix EXP-001
```

Skip keyframe extraction:

```bash
python apps/footage-analyzer/analyze_project.py \
  --project-folder projects/current \
  --skip-keyframes
```

---

## Step 3 — Generate Review Queue

```bash
python apps/footage-analyzer/review_queue.py \
  --memory knowledge/footage/current
```

---

## Step 4 — Search Adventure Memory

Search by emotion:

```bash
python apps/footage-analyzer/footage_search.py \
  --memory knowledge/footage/current \
  --emotion isolation \
  --limit 5
```

Search by story and shot type:

```bash
python apps/footage-analyzer/footage_search.py \
  --memory knowledge/footage/current \
  --story arrival \
  --shot drone-reveal \
  --min-score 75
```

---

## Step 5 — Create Director Handoff From Project Folder

Preferred universal command:

```bash
python apps/footage-analyzer/handoff_project.py \
  --project-folder projects/current \
  --min-score 70 \
  --exclude-avoid
```

Include clips still marked as `needs_review` when testing early:

```bash
python apps/footage-analyzer/handoff_project.py \
  --project-folder projects/current \
  --include-review
```

---

## Output

```text
knowledge/footage/current/
├── TV-CP-0001.md
├── TV-CP-0001.json
├── TV-CP-0002.md
├── TV-CP-0002.json
├── batch-summary.md
├── review-queue.md
├── search-results.md
└── director-handoff.md

assets/current/keyframes/
├── TV-CP-0001/
│   ├── TV-CP-0001_05.jpg
│   ├── TV-CP-0001_25.jpg
│   ├── TV-CP-0001_50.jpg
│   ├── TV-CP-0001_75.jpg
│   └── TV-CP-0001_95.jpg
```

---

## Legacy Direct Commands

The lower-level scripts still exist for power users:

- `footage_analyzer.py`
- `review_queue.py`
- `footage_search.py`
- `director_handoff.py`

But the recommended workflow is project-folder based.

---

## Review Workflow

1. Create or update `project.yaml`.
2. Validate the project with `validate_project.py`.
3. Run `analyze_project.py`.
4. Generate `review-queue.md`.
5. Open generated keyframes.
6. Use `prompts/keyframe-review-prompt-v0.1.md` with Cowork, Codex, ChatGPT, or manual review.
7. Update each `.md` and `.json` memory file with visual analysis.
8. Set `needs_review` to false only when confident.
9. Use `footage_search.py` to find clips by emotion, story, and cinematic purpose.
10. Use `handoff_project.py` to create a candidate pool for the Documentary Director.
11. Director builds storyboard and timeline from Adventure Memory.

---

## Local First Rule

This tool prepares structured memory locally.
AI review can happen later through Cowork, Codex, ChatGPT Pro, or manual review.
