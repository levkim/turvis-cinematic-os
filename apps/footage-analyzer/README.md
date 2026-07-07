# Footage Analyzer CLI

Version: v0.3  
Project: TURVIS Studio / Adventure Memory Engine

---

## Purpose

Footage Analyzer CLI is the first local-first executable tool for TURVIS Studio.

It scans a local footage folder, extracts basic video metadata, extracts review keyframes, creates placeholder Adventure Memory records, and prepares clips for later AI-assisted or human review.

This tool does not require paid AI API calls.

---

## What v0.3 Does

- Scans a local folder for video files
- Creates stable TURVIS clip IDs
- Extracts basic metadata with `ffprobe` if available
- Extracts review keyframes with `ffmpeg`
- Creates Markdown memory files
- Creates JSON memory files
- Creates a batch summary
- Marks clips as `needs_review: true`
- Generates a review queue from clips needing visual review

---

## What v0.3 Does Not Do Yet

- It does not visually understand the clip by itself
- It does not call any AI API
- It does not select final documentary shots
- It does not generate Remotion timelines automatically

---

## Requirements

- Python 3.10+
- FFmpeg installed and available in PATH

Check FFmpeg:

```bash
ffmpeg -version
ffprobe -version
```

---

## Step 1 — Analyze Footage

From repository root:

```bash
python apps/footage-analyzer/footage_analyzer.py \
  --input "D:/Mangystau/Day3" \
  --project mangystau \
  --episode day3 \
  --prefix MG-D3 \
  --country Kazakhstan \
  --region Mangystau \
  --destination "Zhanaozen to Bozzhyra" \
  --output knowledge/footage/mangystau/day3 \
  --keyframes assets/mangystau/day3/keyframes
```

Skip keyframe extraction:

```bash
python apps/footage-analyzer/footage_analyzer.py \
  --input "D:/Mangystau/Day3" \
  --project mangystau \
  --episode day3 \
  --prefix MG-D3 \
  --output knowledge/footage/mangystau/day3 \
  --skip-keyframes
```

---

## Step 2 — Generate Review Queue

```bash
python apps/footage-analyzer/review_queue.py \
  --memory knowledge/footage/mangystau/day3
```

This creates:

```text
knowledge/footage/mangystau/day3/review-queue.md
```

To include clips already marked as reviewed:

```bash
python apps/footage-analyzer/review_queue.py \
  --memory knowledge/footage/mangystau/day3 \
  --include-reviewed
```

---

## Output

```text
knowledge/footage/mangystau/day3/
├── MG-D3-0001.md
├── MG-D3-0001.json
├── MG-D3-0002.md
├── MG-D3-0002.json
├── batch-summary.md
└── review-queue.md

assets/mangystau/day3/keyframes/
├── MG-D3-0001/
│   ├── MG-D3-0001_05.jpg
│   ├── MG-D3-0001_25.jpg
│   ├── MG-D3-0001_50.jpg
│   ├── MG-D3-0001_75.jpg
│   └── MG-D3-0001_95.jpg
```

---

## Review Workflow

1. Run Footage Analyzer CLI.
2. Generate `review-queue.md`.
3. Open generated keyframes.
4. Use `prompts/keyframe-review-prompt-v0.1.md` with Cowork, Codex, ChatGPT, or manual review.
5. Update each `.md` and `.json` memory file with visual analysis.
6. Set `needs_review` to false only when confident.
7. Director can then search Adventure Memory.

---

## Local First Rule

This tool prepares structured memory locally.
AI review can happen later through Cowork, Codex, ChatGPT Pro, or manual review.
