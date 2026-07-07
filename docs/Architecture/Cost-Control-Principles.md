# Cost Control Principles

Version: v0.1  
Project: TURVIS Cinematic OS

---

## 1. Purpose

This document defines how TURVIS Cinematic OS controls AI operating cost.

The goal is to build a powerful AI documentary production system without becoming dependent on expensive continuous API usage.

---

## 2. Cost Philosophy

TURVIS should spend money only where it creates lasting value.

Temporary AI outputs are less valuable than reusable knowledge.

Reusable knowledge includes:

- TCL manuals
- AME metadata
- Director rules
- Story beat templates
- Footage memory
- Remotion components
- Project briefs

---

## 3. Analyze Once, Reuse Forever

Footage analysis should not be repeated unnecessarily.

Once a clip has been analyzed, store the result in:

```text
knowledge/footage/[project]/[episode]/[clip_id].md
knowledge/footage/[project]/[episode]/[clip_id].json
```

Future Directors should search this memory instead of re-analyzing the clip.

---

## 4. Manual Review Beats Automation Waste

If a human can quickly confirm location, route, or usage value, do not spend repeated AI calls guessing.

Use AI for structure and scale.
Use human expertise for final truth.

---

## 5. Avoid Large Video API Uploads

Large video files should not be sent to API services by default.

Preferred low-cost workflow:

```text
Raw Video
↓
Local thumbnails / keyframes
↓
AI-assisted analysis of selected frames
↓
Human correction
↓
Stored memory
```

---

## 6. Use Existing Subscriptions First

Before using paid API calls, prefer:

- ChatGPT Pro interactive sessions
- Cowork
- Codex
- VS Code local workflows
- Manual metadata input

---

## 7. API Budget Gates

Before adding any API-dependent feature, answer:

1. Can this be done locally?
2. Can this be done with existing subscriptions?
3. Is this output reusable?
4. How often will this run?
5. What is the monthly cost risk?
6. Can users disable it?

If these questions are not answered, do not build the API feature yet.

---

## 8. Good API Use Cases

API may be justified for:

- Batch summarizing already-extracted metadata
- Staff-facing shared workflows
- Automated script generation
- Short text classification
- Project brief generation
- Future web dashboard orchestration

---

## 9. Bad API Use Cases

Avoid API for:

- Repeatedly analyzing the same footage
- Uploading large raw video files without filtering
- Generating temporary outputs that are not stored
- Replacing local rendering
- Running expensive multi-agent loops without review

---

## 10. Final Rule

> If the output is not reusable, think twice before paying for it.
