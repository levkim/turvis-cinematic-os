# Local First Strategy

Version: v0.1  
Project: TURVIS Cinematic OS

---

## 1. Purpose

TURVIS Cinematic OS must be designed to minimize API cost and avoid unnecessary dependency on paid cloud inference.

The system should work first as a local-first AI production workflow using:

- GitHub
- Local files
- VS Code
- Cowork
- Codex
- ChatGPT Pro
- Local Remotion rendering

API usage is optional and should only be introduced when local workflows are no longer enough.

---

## 2. Core Principle

> Local first.  
> API optional.  
> Knowledge portable.  
> Cost controlled.

---

## 3. Why Local First

Adventure documentary production can generate heavy AI usage:

- Long narration analysis
- Large footage batch analysis
- Repeated storyboard revisions
- Subtitle generation
- Timeline generation
- Multiple render iterations

If every step uses paid API calls, cost can grow quickly.

Therefore, TURVIS must avoid API-first architecture during early development.

---

## 4. What Runs Locally

The following should run locally whenever possible:

- Remotion preview
- Remotion rendering
- Timeline editing
- Asset organization
- Metadata files
- Project briefs
- Manual footage tagging
- Markdown knowledge base
- JSON memory files
- Git commits

---

## 5. What Uses Existing AI Subscriptions

The following can be performed through existing interactive tools:

- ChatGPT Pro
- Codex
- Cowork
- VS Code AI tools

Use these for:

- Writing manuals
- Generating project plans
- Creating story beat tables
- Drafting timeline data
- Reviewing metadata
- Debugging Remotion code

This keeps TURVIS usable without a dedicated API bill.

---

## 6. When API Becomes Acceptable

API usage may be considered only when:

- Staff need shared automation
- Thousands of clips must be analyzed overnight
- A web dashboard requires server-side AI
- Mobile or remote workflows need automatic processing
- Manual AI interaction becomes a bottleneck

Until then, API is not the default.

---

## 7. Architecture Direction

Current phase:

```text
GitHub Knowledge
↓
Cowork / Codex / ChatGPT Pro
↓
Local Remotion
↓
Local Render
```

Future optional phase:

```text
Web UI
↓
Backend API
↓
AI Provider
↓
Memory DB
↓
Render Worker
```

The future API layer must not replace the knowledge base.
It should only automate it.

---

## 8. Cost Control Rules

1. Never design API as the default path.
2. Store reusable knowledge in Markdown and JSON.
3. Analyze once, reuse forever.
4. Prefer batch summaries over repeated full analysis.
5. Keep Director decisions transparent and editable.
6. Use local rendering whenever possible.
7. Avoid sending large video files to paid APIs unless necessary.

---

## 9. Repository Rule

Every core idea must be stored in the repository as reusable knowledge.

Do not hide important logic inside one-time prompts or API calls.

---

## 10. Final Rule

> API should accelerate TURVIS.  
> API must never become the foundation of TURVIS.
