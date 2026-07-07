# Render Runner

Version: v0.1

Render Runner standardizes Remotion preview and render commands for TURVIS projects.

It assumes the project pipeline has already synced `timeline.remotion.json` into:

```text
remotion/src/data/turvis.timeline.ts
```

## Preview

```bash
python apps/render-runner/render_project.py --preview
```

## Render

```bash
python apps/render-runner/render_project.py --render
```

## Output

```text
remotion/out/turvis-documentary.mp4
```
