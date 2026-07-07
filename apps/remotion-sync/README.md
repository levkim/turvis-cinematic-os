# Remotion Sync

Version: v0.1

Remotion Sync converts a project `timeline.remotion.json` into the TypeScript data file used by the Remotion app.

## Usage

```bash
python apps/remotion-sync/sync_timeline.py \
  --project-folder projects/current
```

Output:

```text
remotion/src/data/turvis.timeline.ts
```

This keeps the Remotion engine universal while allowing each project to provide its own timeline data.
