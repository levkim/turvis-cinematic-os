# No-API Development Loop

Version: v0.1  
Project: TURVIS Cinematic OS

---

## 1. Purpose

This workflow explains how TURVIS Cinematic OS should be developed and operated without relying on paid AI APIs.

It is designed for the current phase of the project:

> Personal / company internal AI studio using GitHub, Cowork, Codex, ChatGPT Pro, VS Code, and local Remotion.

---

## 2. Core Loop

```text
Write Knowledge
↓
Use Cowork / Codex interactively
↓
Update GitHub files
↓
Run Remotion locally
↓
Review output
↓
Improve Knowledge
```

This loop keeps cost low and improves the system over time.

---

## 3. Working With Footage

Recommended process:

```text
1. Copy footage to local project folder
2. Rename or organize clips roughly
3. Extract thumbnails/keyframes if needed
4. Use Footage Analyst Prompt interactively
5. Save metadata as Markdown and JSON
6. Correct metadata manually when needed
7. Director uses memory files to build storyboard
```

No API is required.

---

## 4. Working With Story

Recommended process:

```text
1. Write or paste narration
2. Create project brief
3. Use Documentary Director Prompt interactively
4. Generate story beat table
5. Review and correct the table
6. Convert story beat table into timeline data
```

No API is required.

---

## 5. Working With Remotion

Recommended process:

```text
1. Open repository in VS Code
2. Go to remotion/
3. Run npm install
4. Run npm run start
5. Preview composition
6. Fix timeline / subtitles / paths
7. Render locally
```

Rendering stays on the local computer.

---

## 6. When AI Is Used

AI is used interactively through existing tools:

- ChatGPT Pro
- Cowork
- Codex
- VS Code AI assistant

AI writes and updates files, but the repository remains the source of truth.

---

## 7. Source of Truth

The source of truth is always:

```text
GitHub repository files
```

Not chat history.
Not temporary prompts.
Not API responses.

---

## 8. Manual Approval Points

Human review is required for:

- Location accuracy
- Footage quality decisions
- Final hero shot selection
- Brand tone
- Final render approval

---

## 9. Future API Upgrade Path

If API is added later, it should automate this same loop.

It must not replace the knowledge system.

---

## 10. Final Rule

> Build the brain first.  
> Automate later.
