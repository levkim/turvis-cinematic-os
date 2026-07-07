# TURVIS Studio Operator Manual

Version: v0.1

This manual explains the standard operating sequence for TURVIS Studio.

---

## 1. Check System

Before the first run:

```bash
python apps/turvis-studio/turvis.py doctor
```

Confirm:

- Python 3.10+
- FFmpeg
- FFprobe
- Node.js
- npm
- Remotion folder

---

## 2. Create Project

```bash
python apps/turvis-studio/turvis.py create \
  --title "Project Title" \
  --id project-id \
  --type documentary \
  --country "Country" \
  --region "Region" \
  --destination "Destination" \
  --duration 240 \
  --aspect "16:9"
```

---

## 3. Edit Project Files

Edit:

```text
projects/[project-id]/project.yaml
projects/[project-id]/narration.md
```

Set footage path in `project.yaml`:

```yaml
paths:
  footage: D:/Your/Footage/Folder
```

Paste narration into `narration.md`.

---

## 4. Run Pipeline

For early testing:

```bash
python apps/turvis-studio/turvis.py pipeline \
  --project-folder projects/[project-id] \
  --include-review
```

For stricter production:

```bash
python apps/turvis-studio/turvis.py pipeline \
  --project-folder projects/[project-id] \
  --exclude-avoid \
  --min-score 70 \
  --strict-qc
```

---

## 5. Review Outputs

Check:

```text
projects/[project-id]/review-queue.md
projects/[project-id]/director-handoff.md
projects/[project-id]/director-prep.md
projects/[project-id]/story-beats.md
projects/[project-id]/storyboard.md
projects/[project-id]/timeline-draft.md
projects/[project-id]/timeline.remotion.json
projects/[project-id]/qc-report.md
```

---

## 6. Preview

```bash
python apps/turvis-studio/turvis.py preview --install
```

After first install:

```bash
python apps/turvis-studio/turvis.py preview
```

---

## 7. Render

```bash
python apps/turvis-studio/turvis.py render
```

Output:

```text
remotion/out/turvis-documentary.mp4
```

---

## 8. Rule

Never edit engine code for a specific project.

Edit project data instead:

```text
projects/[project-id]/project.yaml
projects/[project-id]/narration.md
knowledge/footage/[project-id]/
```

---

## 9. Local First Reminder

TURVIS Studio does not require paid AI API calls for the current pipeline.

Use AI interactively only for:

- reviewing keyframes
- improving story beats
- refining storyboard
- final creative direction
