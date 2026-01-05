---
name: youtube
description: Extract transcripts, chapters, comments, and summaries from YouTube videos. Use when the user provides a YouTube URL or asks to analyze/summarize a video.
triggers:
  - youtube
  - video
  - transcript
  - watch
  - youtu.be
---

# YouTube Extraction

Extract transcripts, chapters, comments, metadata, and generate summaries from YouTube videos. Use this skill when:

- User provides a YouTube URL (youtube.com/watch?v=..., youtu.be/..., etc.)
- User asks to "summarize this video"
- User wants the transcript of a video
- User asks about video chapters or timestamps
- User wants to analyze video content or comments

## Available Actions

| Action | Description | Usage |
|--------|-------------|-------|
| `transcript` | Extract video transcript | `pais run youtube transcript <url> [format]` |
| `chapters` | Get video chapters/timestamps | `pais run youtube chapters <url>` |
| `info` | Get video metadata | `pais run youtube info <url>` |
| `comments` | Get video comments (needs API key) | `pais run youtube comments <url> [max]` |
| `summarize` | Get transcript for LLM analysis | `pais run youtube summarize <url> [pattern]` |
| `pipe` | Plain text output for fabric piping | `pais run youtube pipe <url>` |
| `all` | Extract everything | `pais run youtube all <url>` |

## Fabric Integration

The `pipe` action enables direct integration with Daniel Miessler's Fabric:

```bash
# Pipe transcript directly to fabric pattern
pais run youtube pipe "https://youtube.com/watch?v=..." | fabric -p extract_wisdom

# With streaming
pais run youtube pipe "https://youtube.com/watch?v=..." | fabric --stream -p summarize
```

This matches the workflow of Fabric's native `yt` command.

## Comments (Requires API Key)

The `comments` action requires a YouTube Data API key. Set it in one of:

1. Environment: `export YOUTUBE_API_KEY="your-key"`
2. Fabric config: `~/.config/fabric/.env` with `YOUTUBE_API_KEY=your-key`
3. PAIS config: `~/.config/pais/.env` with `YOUTUBE_API_KEY=your-key`

Get a free API key from [Google Cloud Console](https://console.cloud.google.com/apis/credentials).

```bash
# Get top 100 comments
pais run youtube comments "https://youtube.com/watch?v=..."

# Get top 50 comments
pais run youtube comments "https://youtube.com/watch?v=..." 50
```

## Transcript Formats

- `text` (default) - Plain text, sentences joined
- `json` - Array of {start, duration, text} objects with timestamps
- `srt` - SubRip subtitle format

```bash
# Plain text
pais run youtube transcript "URL"

# Timed JSON
pais run youtube transcript "URL" json

# SRT subtitles
pais run youtube transcript "URL" srt
```

## Typical Workflow

### Quick Analysis (Fabric piping)

```bash
pais run youtube pipe "URL" | fabric -p extract_wisdom
```

### Full Research

```bash
# Get everything formatted for analysis
pais run youtube summarize "URL"

# Then apply Fabric pattern manually or save for later
```

### Comment Sentiment

```bash
# Get comments for sentiment analysis
pais run youtube comments "URL" | jq '.comments[].text'
```

## Fabric Patterns for Video Analysis

Recommended patterns from `~/repos/danielmiessler/Fabric/data/patterns/`:

| Pattern | Best For |
|---------|----------|
| `extract_wisdom` | Comprehensive extraction (ideas, insights, quotes, recommendations) |
| `summarize` | Quick summary |
| `create_summary` | Structured summary with key points |
| `extract_main_idea` | Core concept extraction |
| `analyze_presentation` | Presentation/talk analysis |
| `extract_recommendations` | Actionable takeaways |
| `create_keynote` | Turn video into presentation outline |

## Output Storage

Save research to:
```
~/.config/pais/research/youtube/<video-slug>/<date>.md
```

## Dependencies

Installed in plugin venv (`~/.config/pais/plugins/youtube/.venv/`):

- `youtube-transcript-api` - Transcript extraction (no API key needed)
- `yt-dlp` - Video metadata and chapters
- `google-api-python-client` - Comments API (needs API key)

## Comparison with Fabric's `yt`

| Feature | Fabric `yt` | PAIS `youtube` |
|---------|-------------|----------------|
| Transcript | Yes | Yes |
| Comments | Yes | Yes |
| Chapters | No | Yes |
| Rich metadata | No | Yes |
| API key needed | Yes (all) | Only comments |
| Fabric piping | Native | Via `pipe` action |
| Timed transcript | No | Yes (json format) |
| SRT output | No | Yes |

## Limitations

- Requires video to have captions (auto-generated or manual)
- Some videos disable transcript access
- Private/age-restricted videos may not be accessible
- Comments require YouTube API key
- Rate limiting may occur with many requests
