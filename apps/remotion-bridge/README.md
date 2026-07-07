# Remotion Bridge

Version: v0.1

Remotion Bridge converts `timeline-draft.json` into a Remotion-ready timeline file.

## Usage

```bash
python apps/remotion-bridge/build_remotion_timeline.py \
  --project-folder projects/current
```

Output:

```text
projects/current/timeline.remotion.json
```

The generated file is designed to be consumed by the future Remotion composition.
