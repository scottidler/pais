# YouTube Frames Plugin - Detailed Documentation

## Overview

The `youtube-frames` plugin extracts useful visual content (diagrams, code snippets, slides, charts) from YouTube videos, filtering out talking head frames. It's designed for technical videos where capturing visual aids is valuable for research and note-taking.

## Location

```
~/.config/pais/plugins/youtube-frames/
├── plugin.yaml          # PAIS manifest
├── pyproject.toml       # Python dependencies
├── src/main.py          # Main implementation (~1100 lines)
├── SKILL.md             # Usage guide
├── DESIGN.md            # Architecture document
└── .venv/               # Python virtual environment
```

## Output Location

Extracted frames are saved to:
```
~/.config/pais/research/youtube-frames/<video-id>/
├── frames/              # Final classified frames
│   ├── 00_00_diagram.png
│   ├── 08_00_slide.png
│   ├── 37_15_code.png
│   └── ...
├── metadata.json        # Full extraction metadata
└── summary.md           # Human-readable summary
```

## Dependencies

- **yt-dlp** - Video download
- **ffmpeg** - Frame extraction (system package)
- **Pillow** - Image processing
- **imagehash** - Perceptual hashing for deduplication
- **anthropic** (optional) - Claude vision API for classification
- **chafa** (system) - Terminal image rendering

## Actions

### extract - Full Pipeline

```bash
pais run youtube-frames extract "https://youtube.com/watch?v=VIDEO_ID" \
    --strategy=hybrid \
    --classifier=claude
```

Options:
- `--strategy`: scene-change, interval, keyframe, chapters, hybrid (default)
- `--classifier`: none, ocr, claude, gpt4v
- `--output-dir`: Override output location

### quick - Fast Extraction (No Classification)

```bash
pais run youtube-frames quick "https://youtube.com/watch?v=VIDEO_ID"
```

Uses scene-change detection + deduplication only, no classification.

### chapters - One Frame Per Chapter

```bash
pais run youtube-frames chapters "https://youtube.com/watch?v=VIDEO_ID"
```

Extracts one frame at the start of each video chapter.

### classify - Classify Existing Frames

```bash
pais run youtube-frames classify /path/to/frames --classifier=claude
```

Re-classify frames in an existing directory.

### clean - Remove Cached Videos

```bash
pais run youtube-frames clean              # Clean all
pais run youtube-frames clean VIDEO_ID     # Clean specific video
```

Videos are cached in `~/.cache/pais/youtube-frames/`.

### list - List Extractions

```bash
pais run youtube-frames list
```

Shows all extracted video frame sets.

### view - View Frames in Terminal

```bash
# View all frames
pais run youtube-frames view VIDEO_ID

# Filter by type
pais run youtube-frames view VIDEO_ID --filter=diagram
pais run youtube-frames view VIDEO_ID --filter=code
pais run youtube-frames view VIDEO_ID --filter=slide

# Custom size
pais run youtube-frames view VIDEO_ID --size=100x40
```

Renders frames inline using `chafa`. In **Kitty/WezTerm**, renders actual pixels. In other terminals, renders as unicode text art.

## Pipeline Stages

1. **Download** - yt-dlp downloads video (cached for reuse)
2. **Extract** - ffmpeg extracts frames based on strategy
3. **Deduplicate** - Perceptual hashing removes near-duplicates
4. **Classify** - Vision API or OCR categorizes frames
5. **Filter** - Remove talking_head frames, keep top N useful frames
6. **Output** - Rename, organize, generate metadata and summary

## Extraction Strategies

| Strategy | Description | Best For |
|----------|-------------|----------|
| `scene-change` | Detects visual scene changes | General purpose |
| `interval` | Every N seconds | Consistent sampling |
| `keyframe` | Video I-frames only | Fast, codec-based |
| `chapters` | One per chapter | Structured videos |
| `hybrid` | Scene change + chapters | Most comprehensive |

## Classification Methods

| Method | Requirements | Speed | Accuracy |
|--------|--------------|-------|----------|
| `none` | - | Instant | N/A |
| `ocr` | easyocr (CUDA) | Slow | Medium |
| `claude` | ANTHROPIC_API_KEY | Medium | High |
| `gpt4v` | OPENAI_API_KEY | Medium | High |

## Frame Types

- **diagram** - Architecture diagrams, flowcharts, system designs, UML
- **code** - Code snippets, terminal output, IDE screenshots
- **slide** - Presentation slides, documents, bullet points
- **chart** - Graphs, plots, data visualizations
- **talking_head** - Person's face (filtered out)
- **other** - Unclassified content

## Example: Complete Workflow

```bash
# 1. Extract frames with Claude classification
pais run youtube-frames extract "https://youtube.com/watch?v=iKwRWwabkEc" --classifier=claude

# 2. List what was extracted
pais run youtube-frames list

# 3. View diagrams in terminal (best in Kitty)
pais run youtube-frames view iKwRWwabkEc --filter=diagram

# 4. View code screenshots
pais run youtube-frames view iKwRWwabkEc --filter=code

# 5. Open frames directory
xdg-open ~/.config/pais/research/youtube-frames/iKwRWwabkEc/frames/
```

## Test Extractions Done

### Video: Building Your Own Unified AI Assistant Using Claude Code
- **ID**: iKwRWwabkEc
- **Duration**: ~1 hour
- **Strategy**: hybrid
- **Classifier**: claude
- **Results**: 17 frames (5 diagrams, 3 code, 8 slides, 1 other)
- **Path**: `~/.config/pais/research/youtube-frames/iKwRWwabkEc/`

### Video: Blindsided at Work? (Dan O'Connor)
- **ID**: FFIwuEJC3mg
- **Strategy**: scene-change
- **Classifier**: none
- **Results**: 9 frames (mostly talking head - not ideal for this plugin)
- **Path**: `~/.config/pais/research/youtube-frames/FFIwuEJC3mg/`

## Terminal Image Support

The `view` command uses `chafa` which auto-detects terminal capabilities:

| Terminal | Protocol | Quality |
|----------|----------|---------|
| **Kitty** | Kitty graphics | Actual pixels |
| **WezTerm** | Kitty graphics | Actual pixels |
| **iTerm2** | iTerm2 protocol | Actual pixels |
| **Konsole** | Sixel | Actual pixels |
| **GNOME Terminal** | Unicode blocks | Text art |
| **Alacritty** | Unicode blocks | Text art |

For best results, use **Kitty** terminal:
```bash
sudo apt install kitty
kitty &
```

Then in Kitty:
```bash
pais run youtube-frames view iKwRWwabkEc --filter=diagram
```

## Key Files

- **src/main.py:428-498** - Claude vision classification
- **src/main.py:545-728** - Main extraction pipeline
- **src/main.py:975-1079** - View command implementation

## Environment Variables

- `ANTHROPIC_API_KEY` - Required for `--classifier=claude`
- `OPENAI_API_KEY` - Required for `--classifier=gpt4v`

## SSH and Remote Image Rendering

When SSH'd into a remote machine, you need special handling for kitty graphics to work.

### The Problem

Your local kitty terminal renders images, but the remote machine needs to send the correct escape sequences. Regular SSH doesn't forward kitty's graphics protocol capabilities.

### Solution 1: Kitty SSH Kitten (Recommended)

Use kitty's built-in SSH kitten instead of regular ssh:

```bash
# Instead of:
ssh desk.lan

# Use:
kitty +kitten ssh desk.lan
```

This properly forwards:
- Kitty graphics protocol
- Shell integration
- Clipboard
- Terminal capabilities

### Solution 2: Manual TERM Export

If using regular ssh, set TERM on the remote:

```bash
ssh desk.lan
export TERM=xterm-kitty
```

### Solution 3: SSH Config

Add to `~/.ssh/config` on your local machine:

```
Host desk.lan
    SetEnv TERM=xterm-kitty
```

Requires `AcceptEnv TERM` in remote's `/etc/ssh/sshd_config`.

### How It Works

```
┌─────────────────┐     SSH      ┌─────────────────┐
│  Local (lappy)  │◄────────────►│  Remote (desk)  │
│                 │              │                 │
│  Kitty Terminal │  ◄── escape  │  chafa/view cmd │
│  (renders imgs) │     sequences│  (sends data)   │
└─────────────────┘              └─────────────────┘
```

1. You run `pais run youtube-frames view ...` on remote
2. `chafa` detects TERM=xterm-kitty
3. `chafa` sends kitty graphics escape sequences over SSH
4. Your local kitty terminal receives and renders the pixels

### Testing

```bash
# On local machine (lappy), in kitty:
kitty +kitten ssh desk.lan

# On remote (desk):
chafa ~/.config/pais/research/youtube-frames/iKwRWwabkEc/frames/22_30_diagram.png

# Should render actual pixels, not text art
```

### Troubleshooting

**Still getting text art?**
```bash
# Check TERM on remote
echo $TERM
# Should be: xterm-kitty

# Check if kitty-terminfo is installed on remote
infocmp xterm-kitty >/dev/null && echo "OK" || echo "Missing terminfo"

# Install if missing
sudo apt install kitty-terminfo
```

**Force kitty protocol in chafa:**
```bash
chafa --format=kitty image.png
```

## Known Issues

1. **easyocr crashes on AMD GPUs** - No CUDA support. Use `--classifier=claude` instead.
2. **Talking head videos** - Plugin is designed for technical content with visual aids.
3. **API costs** - Claude classification costs ~$0.01-0.05 per video depending on frame count.

## Future Improvements

- [ ] Add `--dry-run` to preview frames before classification
- [ ] Support local vision models (LLaVA, etc.)
- [ ] Batch processing for multiple videos
- [ ] Integration with youtube skill for combined transcript + frames
