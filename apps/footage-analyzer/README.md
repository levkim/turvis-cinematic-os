# Footage Analyzer CLI

Version: v0.4  
Project: TURVIS Studio / Adventure Memory Engine

---

## Purpose

Footage Analyzer CLI is the first local-first executable tool for TURVIS Studio.

It scans a local footage folder, extracts basic video metadata, extracts review keyframes, creates placeholder Adventure Memory records, prepares clips for later AI-assisted or human review, and searches reviewed footage memory.

This tool does not require paid AI API calls.

---

## What v0.4 Does

- Scans a local folder for video files
- Creates stable TURVIS clip IDs
- Extracts basic metadata with `ffprobe` if available
- Extracts review keyframes with `ffmpeg`
- Creates Markdown memory files
- Creates JSON memory files
- Creates a batch summary
- Marks clips as `needs_review: true`
- Generates a review queue from clips needing visual review
- Searches Adventure Memory by query, emotion, story, shot type, location, score, and hero flag

---

## What v0.4 Does Not Do Yet

- It does not visually understand the clip by itself
- It does not call any AI API
- It does not select final documentary shots automatically
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

## Step 3 — Search Adventure Memory

Search by emotion:

```bash
python apps/footage-analyzer/footage_search.py \
  --memory knowledge/footage/mangystau/day3 \
  --emotion isolation \
  --limit 5
```

Search by story and shot type:

```bash
python apps/footage-analyzer/footage_search.py \
  --memory knowledge/footage/mangystau/day3 \
  --story arrival \
  --shot drone-reveal \
  --min-score 75
```

Search for hero shots only:

```bash
python apps/footage-analyzer/footage_search.py \
  --memory knowledge/footage/mangystau/day3 \
  --hero-only \
  --exclude-avoid
```

Write search results to Markdown:

```bash
python apps/footage-analyzer/footage_search.py \
  --memory knowledge/footage/mangystau/day3 \
  --query "golden hour desert" \
  --output knowledge/footage/mangystau/day3/search-results.md
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
├── review-queue.md
└── search-results.md

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
7. Use `footage_search.py` to find clips by emotion, story, and cinematic purpose.
8. Director can then build storyboard and timeline from Adventure Memory.

---

## Local First Rule

This tool prepares structured memory locally.
AI review can happen later through Cowork, Codex, ChatGPT Pro, or manual review.
