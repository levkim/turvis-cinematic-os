# Engine / Data / Example Separation

Version: v0.1  
Project: TURVIS Studio

---

## 1. Purpose

This document defines a non-negotiable architecture rule for TURVIS Studio.

Apps must not know specific projects.
Projects must be data.
Examples must live separately.

This keeps TURVIS scalable, reusable, and clean.

---

## 2. Core Rule

> Applications never know projects.  
> Projects are data.  
> Examples are examples.  
> Engines are universal.

---

## 3. Definitions

### Engine

Reusable software that works for any project.

Examples:

```text
apps/footage-analyzer/
apps/director/
apps/story-engine/
apps/remotion-builder/
```

Engines must not contain hard-coded project names such as:

```text
Mangystau
Day 3
Kyrgyzstan
Japan
```

### Data

Project-specific information.

Examples:

```text
projects/[project-slug]/project.yaml
projects/[project-slug]/narration.md
projects/[project-slug]/assets.yaml
projects/[project-slug]/director-notes.md
```

### Example

Sample project used for testing, demonstration, or documentation.

Examples:

```text
examples/mangystau-day3/
examples/japan-ski/
examples/kyrgyzstan-winter/
```

Examples must never be required for the engine to work.

---

## 4. Repository Rule

Use this separation:

```text
apps/       universal executable tools
projects/   active user/company project data
examples/   sample projects and demos
docs/       system knowledge and manuals
knowledge/  reusable memory and indexed knowledge
```

---

## 5. Anti-Pattern

Bad:

```bash
python director_handoff.py --project "Mangystau Day 3"
```

Better:

```bash
python director_handoff.py --project-spec projects/current/project.yaml
```

Best:

```bash
python director_handoff.py --project-folder projects/current
```

The app reads project configuration from data files.

---

## 6. Project Spec Rule

Every project should have:

```text
project.yaml
```

The app must read `project.yaml` instead of relying on hard-coded CLI values.

---

## 7. Why This Matters

Without this separation, TURVIS becomes a collection of one-off scripts.

With this separation, TURVIS becomes an operating system.

---

## 8. Final Rule

> If a project name appears inside engine code, the architecture is wrong.
