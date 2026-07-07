# Project Pipeline CLI

Version: v0.1  
Project: TURVIS Studio

---

## Purpose

Project Pipeline runs the standard local-first production preparation workflow with one command.

It executes:

```text
validate
↓
analyze footage
↓
generate review queue
↓
create Director handoff
```

No AI API calls are required.

---

## Usage

```bash
python apps/project-pipeline/run_pipeline.py \
  --project-folder projects/current \
  --include-review
```

---

## Options

Skip keyframe extraction:

```bash
python apps/project-pipeline/run_pipeline.py \
  --project-folder projects/current \
  --skip-keyframes
```

Skip analysis and only recreate handoff:

```bash
python apps/project-pipeline/run_pipeline.py \
  --project-folder projects/current \
  --skip-analyze \
  --skip-review-queue \
  --include-review
```

Exclude avoid clips and require score:

```bash
python apps/project-pipeline/run_pipeline.py \
  --project-folder projects/current \
  --exclude-avoid \
  --min-score 70
```

---

## Rule

Pipeline reads project data.

Pipeline does not know specific projects.
