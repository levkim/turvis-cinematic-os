# Cowork Runbook v0.1

This runbook explains how to use TURVIS Cinematic OS inside Cowork with the Remotion skill.

---

## 1. Purpose

Cowork should act as the production operator.

It must read the TURVIS manuals, interpret the project brief, update the Remotion timeline, and prepare a render-ready documentary edit.

Cowork should not behave like a generic coding assistant.
It should follow the Documentary Director workflow.

---

## 2. Required Files

Before starting a project, Cowork must read:

```text
README.md
prompts/director-prompt-v0.1.md
docs/TCL/TCL-001-Foundation.md
docs/TCL/TCL-002-Adventure-DNA.md
docs/TCL/TCL-003-Camera-Drone-Language.md
docs/TCL/TCL-004-Story-Beat-Engine.md
docs/TCL/TCL-005-Documentary-Director.md
docs/Director/Director-Core.md
projects/mangystau/day3/project-brief.md
remotion/README.md
```

For Remotion implementation, Cowork must inspect:

```text
remotion/src/Root.tsx
remotion/src/compositions/DocumentaryComposition.tsx
remotion/src/components/CinematicSubtitle.tsx
remotion/src/components/CinematicTitleCard.tsx
remotion/src/components/FilmFade.tsx
remotion/src/data/mangystau-day3.timeline.ts
remotion/src/types.ts
```

---

## 3. Cowork Operating Rules

### Rule 1 — Do not start with code

Cowork must first generate a Director analysis:

1. Project interpretation
2. Narration segmentation
3. Story beat table
4. Footage classification
5. Timeline plan
6. Remotion implementation plan

Only after this may Cowork modify code.

### Rule 2 — Use actual footage paths

When the user provides footage files, Cowork must replace placeholder paths in:

```text
remotion/src/data/mangystau-day3.timeline.ts
```

Example placeholder:

```text
/assets/mangystau/day3/kyzylkup-reveal-01.mp4
```

Replace with the real asset path used in the Remotion project.

### Rule 3 — No audio generation

Unless explicitly requested, Cowork must not generate:

- voice narration audio
- background music
- sound effects

### Rule 4 — Broadcast subtitle style only

Cowork may adjust `CinematicSubtitle.tsx`, but it must preserve:

- maximum two-line style
- lower safe area
- fade in/out
- dark bottom gradient
- elegant documentary tone

### Rule 5 — Remotion follows the Director

Remotion code is an execution layer.
Creative decisions come from the Documentary Director plan.

---

## 4. Standard Cowork Workflow

```text
Step 1 — Read project manuals
Step 2 — Read project brief
Step 3 — Inspect footage folder
Step 4 — Classify footage
Step 5 — Build story beat table
Step 6 — Update timeline data
Step 7 — Verify Remotion composition
Step 8 — Run Remotion preview
Step 9 — Fix TypeScript/runtime errors
Step 10 — Render output
Step 11 — Run Director QC checklist
```

---

## 5. Required Cowork Report

After completing work, Cowork must report:

```text
1. Files read
2. Footage classification summary
3. Timeline changes
4. Subtitle changes
5. Remotion files modified
6. Known issues
7. Render command
8. QC result
```

---

## 6. Render Commands

From the `remotion/` directory:

```bash
npm install
npm run start
npm run render:day3
```

The expected output path is:

```text
remotion/out/mangystau-day3.mp4
```

---

## 7. Quality Standard

The final video must feel like:

- Netflix Documentary
- BBC Earth
- National Geographic
- Apple TV+ Nature

It must not feel like:

- Travel vlog
- TikTok montage
- Tourism advertisement
- Random drone compilation

---

## 8. Final Rule

Cowork must protect the film from becoming a montage.
