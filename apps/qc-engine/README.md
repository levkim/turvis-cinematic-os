# QC Engine

Version: v0.1

QC Engine validates TURVIS project outputs before Remotion preview or render.

## Usage

```bash
python apps/qc-engine/qc_project.py \
  --project-folder projects/current
```

It checks:

- required project files
- timeline JSON existence
- Remotion timeline schema
- clip timing validity
- composition fields
- audio generation rules

Output:

```text
projects/current/qc-report.md
```
