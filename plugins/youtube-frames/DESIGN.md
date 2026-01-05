# YouTube Frames Plugin Design

## Overview

Extract useful visual content (diagrams, code, architecture, slides) from YouTube videos, filtering out talking-head shots and other non-informative frames.

## Problem Statement

Tech videos often contain valuable diagrams, code snippets, and architecture drawings that are lost when only extracting transcripts. Manual screenshot capture is tedious and incomplete.

## Goals

1. **Automated extraction** - No manual intervention required
2. **Smart filtering** - Only keep useful frames (diagrams, code, slides)
3. **Deduplication** - Remove near-duplicate frames
4. **Timestamped output** - Link frames to video timestamps
5. **Classification** - Label frame types (diagram, code, slide, etc.)

## Non-Goals

- Real-time processing during video playback
- Video editing or modification
- Perfect accuracy (80%+ useful frames is acceptable)

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        youtube-frames                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────────┐ │
│  │ Download │ → │ Extract  │ → │  Filter  │ → │  Classify    │ │
│  │ (yt-dlp) │   │ (ffmpeg) │   │ (phash)  │   │ (vision/ocr) │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────────┘ │
│                                                                  │
│  Strategies:                                                     │
│  ├── scene-change  - ffmpeg scene detection                     │
│  ├── interval      - fixed interval (every N seconds)           │
│  ├── keyframe      - I-frames only                              │
│  ├── chapters      - one frame per chapter                      │
│  └── hybrid        - scene + dedup + classification (default)   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Pipeline Stages

### Stage 1: Download

```python
def download_video(url: str, max_height: int = 1080) -> Path:
    """Download video using yt-dlp, limiting resolution for speed."""
    # yt-dlp -f 'best[height<=1080]' -o video.mp4 URL
```

- Skip if video already downloaded (cache by video_id)
- Limit resolution to 1080p max (4K unnecessary for diagrams)
- Store in temp directory, cleaned up after processing

### Stage 2: Frame Extraction

Multiple strategies available:

**Scene Change Detection** (default)
```bash
ffmpeg -i video.mp4 -vf "select='gt(scene,0.3)',showinfo" -vsync vfr frames/%04d.png
```
- Threshold 0.3 = moderate sensitivity
- Catches slide transitions, diagram appearances

**Interval Sampling**
```bash
ffmpeg -i video.mp4 -vf "fps=1/10" frames/%04d.png
```
- One frame every N seconds
- Simple but generates many duplicates

**Keyframe Extraction**
```bash
ffmpeg -i video.mp4 -vf "select='eq(pict_type,I)'" -vsync vfr frames/%04d.png
```
- Only I-frames (keyframes)
- Fast, but may miss important moments

**Chapter-Based**
```python
# Extract one frame at each chapter timestamp
for chapter in chapters:
    ffmpeg -ss {chapter.start_time} -i video.mp4 -frames:v 1 frame.png
```

### Stage 3: Deduplication

Use perceptual hashing to remove near-duplicates:

```python
import imagehash
from PIL import Image

def dedupe_frames(frames: list[Path], threshold: int = 10) -> list[Path]:
    """Remove frames with perceptual hash distance < threshold."""
    hashes = {}
    unique = []

    for frame in frames:
        h = imagehash.phash(Image.open(frame))
        is_duplicate = any(h - existing < threshold for existing in hashes.values())

        if not is_duplicate:
            hashes[frame] = h
            unique.append(frame)

    return unique
```

### Stage 4: Scoring / Classification

**OCR-based scoring** (fast, local)
```python
import easyocr

def score_text_density(frame: Path) -> float:
    """Score frame by text content - higher = likely diagram/code."""
    reader = easyocr.Reader(['en'])
    result = reader.readtext(str(frame))

    # Calculate text density
    total_text = sum(len(r[1]) for r in result)
    return total_text / 100  # Normalize
```

**Vision model classification** (accurate, API cost)
```python
def classify_frame(frame: Path, model: str = "claude") -> FrameClass:
    """Use vision model to classify frame type."""
    prompt = """Classify this video frame into ONE category:
    - diagram: Architecture, flowchart, system diagram
    - code: Code snippet, terminal output, IDE
    - slide: Presentation slide with text
    - chart: Graph, plot, data visualization
    - talking_head: Person speaking to camera
    - other: None of the above

    Respond with just the category name."""

    # Call Claude/GPT-4V with image
```

### Stage 5: Output

```
output-dir/
├── metadata.json           # Full extraction metadata
├── frames/
│   ├── 00_02_15_diagram.png
│   ├── 00_05_30_code.png
│   └── 00_12_45_slide.png
└── summary.md              # Human-readable summary
```

**metadata.json**
```json
{
  "video_id": "abc123",
  "title": "System Design Interview",
  "extracted_at": "2026-01-05T14:30:00Z",
  "strategy": "hybrid",
  "frames": [
    {
      "filename": "00_02_15_diagram.png",
      "timestamp": 135.0,
      "timestamp_formatted": "2:15",
      "classification": "diagram",
      "confidence": 0.92,
      "ocr_text": "Load Balancer → API Gateway → Services",
      "phash": "a1b2c3d4e5f6"
    }
  ]
}
```

## Actions

| Action | Description |
|--------|-------------|
| `extract` | Full pipeline: download → extract → filter → classify |
| `quick` | Fast extraction: scene-change + dedup only (no classification) |
| `classify` | Classify existing frames directory |
| `clean` | Remove cached videos and temp files |

## Configuration

```yaml
config:
  output-dir:
    type: string
    default: ~/.config/pais/research/youtube-frames

  strategy:
    type: string
    default: hybrid
    options: [scene-change, interval, keyframe, chapters, hybrid]

  scene-threshold:
    type: float
    default: 0.3
    description: Scene change sensitivity (0.1-0.5)

  interval-seconds:
    type: int
    default: 10
    description: Seconds between frames (interval strategy)

  dedup-threshold:
    type: int
    default: 10
    description: Perceptual hash distance threshold

  classifier:
    type: string
    default: ocr
    options: [ocr, claude, gpt4v, none]

  max-frames:
    type: int
    default: 50
    description: Maximum frames to keep after filtering

  keep-video:
    type: bool
    default: false
    description: Keep downloaded video after extraction
```

## Dependencies

```toml
[project]
dependencies = [
    "yt-dlp>=2024.0.0",
    "Pillow>=10.0.0",
    "imagehash>=4.3.0",
    "easyocr>=1.7.0",      # Optional: for OCR scoring
    "anthropic>=0.30.0",   # Optional: for Claude classification
    "openai>=1.0.0",       # Optional: for GPT-4V classification
]
```

System requirements:
- `ffmpeg` (required)
- GPU recommended for easyocr (CPU fallback available)

## Usage Examples

```bash
# Full extraction with defaults
pais run youtube-frames extract "https://youtube.com/watch?v=..."

# Quick extraction (no classification)
pais run youtube-frames quick "https://youtube.com/watch?v=..." ./output

# Use specific strategy
pais run youtube-frames extract "URL" --strategy=chapters

# Classify existing frames
pais run youtube-frames classify ./frames-dir

# Clean cache
pais run youtube-frames clean
```

## Integration with youtube plugin

Could consume from youtube plugin for metadata:

```yaml
consumes:
  youtube:
    contract: YouTubeProvider
    optional: true
```

## Future Enhancements

1. **Slide deck reconstruction** - Group related frames into logical slides
2. **Transcript alignment** - Link frames to transcript segments
3. **OCR extraction** - Extract text from diagrams for searchability
4. **Thumbnail generation** - Create video thumbnail grid
5. **Comparison mode** - Compare frames across multiple videos
