# Footage Analyzer CLI

Version: v0.1  
Project: TURVIS Studio / Adventure Memory Engine

---

## Purpose

Footage Analyzer CLI is the first local-first executable tool for TURVIS Studio.

It scans a local footage folder, extracts basic video metadata, creates placeholder Adventure Memory records, and prepares clips for later AI-assisted review.

This tool does not require paid AI API calls.

---

## What v0.1 Does

- Scans a local folder for video files
- Creates stable TURVIS clip IDs
- Extracts basic metadata with `ffprobe` if available
- Creates Markdown memory files
- Creates JSON memory files
- Creates a batch summary
- Marks clips as `needs_review: true`

---

## What v0.1 Does Not Do Yet

- It does not visually understand the clip
- It does not call any AI API
- It does not select final documentary shots
- It does not generate Remotion timelines automatically

---

## Requirements

- Python 3.10+
- FFmpeg installed and available in PATH for metadata extraction

Check FFmpeg:

```bash
ffmpeg -version
ffprobe -version
```

---

## Usage

From repository root:

```bash
python apps/footage-analyzer/footage_analyzer.py \
  --input "D:/Mangystau/Day3" \
  --project mangystau \
  --episode day3 \
  --prefix MG-D3 \
  --output knowledge/footage/mangystau/day3
```

---

## Output

```text
knowledge/footage/mangystau/day3/
├── MG-D3-0001.md
├── MG-D3-0001.json
├── MG-D3-0002.md
├── MG-D3-0002.json
└── batch-summary.md
```

---

## Local First Rule

This tool prepares structured memory locally.
AI review can happen later through Cowork, Codex, ChatGPT Pro, or manual review.
