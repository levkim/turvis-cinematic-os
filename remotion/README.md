# Remotion Engine

This folder contains the Remotion implementation layer for TURVIS Cinematic OS.

The Remotion Engine must not make creative decisions by itself. It executes the plan created by the Documentary Director.

---

## Core Rule

> Storyboard first.  
> Timeline second.  
> Remotion third.  
> Quality control always.

---

## v0.1 Goal

The v0.1 Remotion Engine provides:

- A documentary composition shell
- Timeline data structure
- Cinematic subtitle component
- Basic transition components
- Sample Mangystau Day 3 timeline data
- Render-ready project conventions

---

## Folder Structure

```text
remotion/
├── package.json
├── tsconfig.json
├── remotion.config.ts
├── src/
│   ├── Root.tsx
│   ├── compositions/
│   │   └── DocumentaryComposition.tsx
│   ├── components/
│   │   ├── CinematicSubtitle.tsx
│   │   ├── CinematicTitleCard.tsx
│   │   └── FilmFade.tsx
│   ├── data/
│   │   └── mangystau-day3.timeline.ts
│   └── types.ts
```

---

## Restrictions

Unless explicitly requested, this engine must not generate:

- Narration audio
- Background music
- Sound effects

The first target output is silent documentary video with cinematic subtitles.
