# Cowork Remotion Command — Mangystau Day 3 v0.1

Copy and paste this command into Cowork when starting the Mangystau Day 3 Remotion edit.

---

## Command

You are operating inside the `levkim/turvis-cinematic-os` repository.

Act as the TURVIS Documentary Director and Remotion production operator.

Your task is to create a cinematic 16:9 documentary edit for:

```text
Project: Mangystau Day 3 — Layers of Color and The Fangs
Target Duration: Approximately 4 minutes
Aspect Ratio: 16:9
Resolution: 3840x2160
Style: Netflix Documentary / BBC Earth / National Geographic
Output: Silent documentary video with premium broadcast-style subtitles
```

---

## Required Reading

Before modifying files, read:

```text
README.md
prompts/director-prompt-v0.1.md
docs/Cowork/Cowork-Runbook-v0.1.md
docs/TCL/TCL-001-Foundation.md
docs/TCL/TCL-002-Adventure-DNA.md
docs/TCL/TCL-003-Camera-Drone-Language.md
docs/TCL/TCL-004-Story-Beat-Engine.md
docs/TCL/TCL-005-Documentary-Director.md
docs/Director/Director-Core.md
projects/mangystau/day3/project-brief.md
remotion/README.md
```

Then inspect:

```text
remotion/src/data/mangystau-day3.timeline.ts
remotion/src/compositions/DocumentaryComposition.tsx
remotion/src/components/CinematicSubtitle.tsx
remotion/src/components/CinematicTitleCard.tsx
remotion/src/components/FilmFade.tsx
```

---

## Restrictions

Do not generate narration audio.
Do not generate music.
Do not generate sound effects.
Do not create vlog-style captions.
Do not use flashy transitions.
Do not turn this into a social media montage.

---

## Required Workflow

First, produce a Director Plan:

1. Project interpretation
2. Emotional arc
3. Narration segmentation
4. Story beat table
5. Required footage classification
6. Shot selection strategy
7. Timeline plan
8. Subtitle plan
9. Transition plan
10. QC checklist

Only after the Director Plan is complete, update the Remotion files.

---

## Footage Handling

If the actual footage folder is available, inspect it and map clips into the timeline.

If actual clips are not yet available, keep placeholder paths but create a `required-footage-list.md` file under:

```text
projects/mangystau/day3/required-footage-list.md
```

The list must include:

- Required clip name
- Location
- Shot type
- Emotional purpose
- Suggested duration
- Priority level

---

## Remotion Tasks

Ensure that:

- `MangystauDay3` composition is available in `Root.tsx`
- Timeline duration is approximately 4 minutes
- Subtitle style remains premium and broadcast-like
- Title cards are elegant and restrained
- Transitions are documentary-style only
- Placeholder paths are clearly documented
- Render command works from the `remotion/` directory

Use:

```bash
npm install
npm run start
npm run render:day3
```

---

## Final Report

After implementation, report:

```text
Files read:
Files modified:
Footage mapped:
Placeholder footage still needed:
Timeline duration:
Render command:
Known issues:
QC result:
```

---

## Final Rule

Storyboard first.
Timeline second.
Remotion third.
Quality control always.
