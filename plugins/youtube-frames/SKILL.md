# YouTube Frames Extraction

Extract diagrams, code snippets, and slides from YouTube videos. Use this skill when:

- User wants to capture visuals from a tech video
- User asks for "screenshots" or "diagrams" from a video
- User wants to extract slides from a presentation
- User mentions "important frames" or "key visuals"

## Available Actions

| Action | Description | Usage |
|--------|-------------|-------|
| `extract` | Full pipeline with classification | `pais run youtube-frames extract <url>` |
| `quick` | Fast extraction (no classification) | `pais run youtube-frames quick <url>` |
| `chapters` | One frame per chapter | `pais run youtube-frames chapters <url>` |
| `classify` | Classify existing frames | `pais run youtube-frames classify <dir>` |
| `clean` | Remove cached videos | `pais run youtube-frames clean` |
| `list` | List extracted frame sets | `pais run youtube-frames list` |

## Extraction Strategies

| Strategy | Description | Best For |
|----------|-------------|----------|
| `hybrid` | Scene change + chapters + dedup (default) | General use |
| `scene-change` | Detect visual changes | Videos with clear transitions |
| `interval` | Fixed time intervals | Long videos, uniform content |
| `keyframe` | I-frames only | Fast extraction |
| `chapters` | One per chapter | Well-structured videos |

## Examples

```bash
# Full extraction with smart filtering
pais run youtube-frames extract "https://youtube.com/watch?v=..."

# Quick extraction (no classification, faster)
pais run youtube-frames quick "https://youtube.com/watch?v=..."

# Extract chapter thumbnails only
pais run youtube-frames chapters "https://youtube.com/watch?v=..."

# Use Claude for classification (more accurate, costs API)
pais run youtube-frames extract "URL" --classifier=claude

# Custom output directory
pais run youtube-frames extract "URL" --output-dir=./my-frames
```

## Output Structure

```
~/.config/pais/research/youtube-frames/<video-id>/
├── metadata.json       # Full extraction metadata
├── summary.md          # Human-readable summary
└── frames/
    ├── 02_15_diagram.png
    ├── 05_30_code.png
    └── 12_45_slide.png
```

## Frame Classifications

| Type | Description |
|------|-------------|
| `diagram` | Architecture, flowchart, system design |
| `code` | Code snippet, terminal, IDE |
| `slide` | Presentation slide with text |
| `chart` | Graph, plot, data visualization |
| `talking_head` | Person speaking (filtered out) |
| `other` | Unclassified |

## Classifiers

| Classifier | Description | Cost |
|------------|-------------|------|
| `ocr` | Text-based heuristics (default) | Free |
| `claude` | Claude vision model | API cost |
| `gpt4v` | GPT-4V vision model | API cost |
| `none` | Skip classification | Free |

## Dependencies

**Required:**
- `ffmpeg` (system)
- `yt-dlp` (Python)
- `Pillow` (Python)
- `imagehash` (Python)

**Optional:**
- `easyocr` - For OCR-based classification
- `anthropic` - For Claude classification
- `openai` - For GPT-4V classification

## Installation

```bash
# Install plugin dependencies
cd ~/.config/pais/plugins/youtube-frames
uv venv
uv pip install -e .

# For OCR classification
uv pip install -e ".[ocr]"

# For vision model classification
uv pip install -e ".[claude]"  # or [openai] or [all]
```

## Typical Workflow

1. **Extract frames from video:**
   ```bash
   pais run youtube-frames extract "https://youtube.com/watch?v=abc123"
   ```

2. **Review extracted frames:**
   ```bash
   open ~/.config/pais/research/youtube-frames/abc123/frames/
   ```

3. **Use with transcript for full context:**
   ```bash
   pais run youtube transcript "URL" > transcript.txt
   # Now have both transcript and key visuals
   ```

## Limitations

- Requires video to be downloadable (not DRM-protected)
- OCR classification is heuristic-based, not perfect
- Vision model classification incurs API costs
- Large videos take time to process
