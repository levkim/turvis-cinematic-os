# Project Wizard CLI

Version: v0.1  
Project: TURVIS Studio

---

## Purpose

Project Wizard creates a new TURVIS project folder.

It prevents engines from knowing project names directly.

Projects are data. Apps are engines.

---

## Usage

```bash
python apps/project-wizard/create_project.py \
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

## Next Steps

Validate:

```bash
python apps/common/validate_project.py \
  --project-folder projects/kazakhstan-mangystau-documentary
```

Analyze footage:

```bash
python apps/footage-analyzer/analyze_project.py \
  --project-folder projects/kazakhstan-mangystau-documentary
```

Create Director handoff:

```bash
python apps/footage-analyzer/handoff_project.py \
  --project-folder projects/kazakhstan-mangystau-documentary \
  --include-review
```

---

## Rule

Do not create project-specific apps.

Create project folders.
