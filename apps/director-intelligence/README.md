# Director Intelligence

Version: v0.1

Director Intelligence is Phase 2 of TURVIS Studio.

It analyzes narration into director decisions:

- emotion
- rhythm
- visual intention
- shot preference
- silence need
- subtitle strategy
- reasoning

## Usage

```bash
python apps/director-intelligence/analyze_narration.py \
  --project-folder projects/current
```

Output:

```text
projects/current/director-decisions.json
projects/current/director-decisions.md
```

This is local-first and rule-based in v0.1.
No paid AI API calls are required.
