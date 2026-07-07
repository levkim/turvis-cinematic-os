# TURVIS Studio CLI

Version: v0.1

Unified command entry for TURVIS Studio.

## Commands

Create project:

```bash
python apps/turvis-studio/turvis.py create \
  --title "Kazakhstan Mangystau Documentary" \
  --id kazakhstan-mangystau-documentary
```

Run pipeline:

```bash
python apps/turvis-studio/turvis.py pipeline \
  --project-folder projects/current \
  --include-review
```

Preview:

```bash
python apps/turvis-studio/turvis.py preview --install
```

Render:

```bash
python apps/turvis-studio/turvis.py render
```
