# System Doctor

Version: v0.1

System Doctor checks whether the local computer is ready to run TURVIS Studio.

## Usage

```bash
python apps/system-doctor/doctor.py
```

It checks:

- Python version
- FFmpeg
- FFprobe
- Node.js
- npm
- Remotion folder
- package.json
- core app folders

Use this before running the full pipeline for the first time.
