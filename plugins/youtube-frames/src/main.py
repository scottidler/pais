#!/usr/bin/env python3
"""
YouTube Frames extraction plugin for PAIS.

Extracts useful visual content (diagrams, code, slides) from YouTube videos.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any


# Frame classification types
FRAME_TYPES = ["diagram", "code", "slide", "chart", "talking_head", "other"]


@dataclass
class ExtractedFrame:
    """Metadata for an extracted frame."""
    filename: str
    timestamp: float
    timestamp_formatted: str
    classification: str | None = None
    confidence: float | None = None
    ocr_text: str | None = None
    phash: str | None = None


@dataclass
class ExtractionResult:
    """Result of frame extraction."""
    success: bool
    video_id: str
    title: str | None = None
    output_dir: str | None = None
    strategy: str | None = None
    frames: list[ExtractedFrame] | None = None
    error: str | None = None
    stats: dict | None = None


def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from URL or return as-is if already an ID."""
    if len(url_or_id) == 11 and re.match(r"^[\w-]+$", url_or_id):
        return url_or_id

    patterns = [
        r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/)([^&\n?#]+)",
        r"youtube\.com/shorts/([^&\n?#]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)

    raise ValueError(f"Could not extract video ID from: {url_or_id}")


def format_timestamp(seconds: float) -> str:
    """Format seconds as HH:MM:SS or MM:SS."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}_{minutes:02d}_{secs:02d}"
    return f"{minutes:02d}_{secs:02d}"


def format_timestamp_display(seconds: float) -> str:
    """Format seconds as H:MM:SS or M:SS for display."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def get_cache_dir() -> Path:
    """Get cache directory for downloaded videos."""
    cache_dir = Path.home() / ".cache" / "pais" / "youtube-frames"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def get_output_dir(video_id: str, base_dir: str | None = None) -> Path:
    """Get output directory for extracted frames."""
    if base_dir:
        output_dir = Path(base_dir).expanduser()
    else:
        output_dir = Path.home() / ".config" / "pais" / "research" / "youtube-frames"

    output_dir = output_dir / video_id
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def check_ffmpeg() -> bool:
    """Check if ffmpeg is available."""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_video_info(video_id: str) -> dict[str, Any] | None:
    """Get video metadata using yt-dlp."""
    try:
        import yt_dlp
    except ImportError:
        return None

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}",
                download=False
            )
            return {
                "id": info.get("id"),
                "title": info.get("title"),
                "channel": info.get("channel"),
                "duration": info.get("duration"),
                "chapters": info.get("chapters", []),
            }
    except Exception:
        return None


def download_video(video_id: str, max_height: int = 1080) -> Path | None:
    """Download video using yt-dlp."""
    try:
        import yt_dlp
    except ImportError:
        return None

    cache_dir = get_cache_dir()
    video_path = cache_dir / f"{video_id}.mp4"

    # Return cached video if exists
    if video_path.exists():
        return video_path

    ydl_opts = {
        "format": f"best[height<={max_height}][ext=mp4]/best[height<={max_height}]/best",
        "outtmpl": str(video_path),
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
        return video_path if video_path.exists() else None
    except Exception:
        return None


def extract_frames_scene_change(
    video_path: Path,
    output_dir: Path,
    threshold: float = 0.3
) -> list[tuple[Path, float]]:
    """Extract frames using scene change detection."""
    frames_dir = output_dir / "raw_frames"
    frames_dir.mkdir(exist_ok=True)

    # Use ffmpeg to detect scene changes and extract frames
    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-vf", f"select='gt(scene,{threshold})',showinfo",
        "-vsync", "vfr",
        str(frames_dir / "frame_%04d.png"),
        "-y"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Parse timestamps from ffmpeg output
    frames = []
    frame_files = sorted(frames_dir.glob("frame_*.png"))

    # Extract timestamps from showinfo output
    timestamps = []
    for line in result.stderr.split("\n"):
        if "pts_time:" in line:
            match = re.search(r"pts_time:(\d+\.?\d*)", line)
            if match:
                timestamps.append(float(match.group(1)))

    # Match frames to timestamps
    for i, frame_path in enumerate(frame_files):
        timestamp = timestamps[i] if i < len(timestamps) else i * 10.0
        frames.append((frame_path, timestamp))

    return frames


def extract_frames_interval(
    video_path: Path,
    output_dir: Path,
    interval_seconds: int = 10
) -> list[tuple[Path, float]]:
    """Extract frames at fixed intervals."""
    frames_dir = output_dir / "raw_frames"
    frames_dir.mkdir(exist_ok=True)

    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-vf", f"fps=1/{interval_seconds}",
        str(frames_dir / "frame_%04d.png"),
        "-y"
    ]

    subprocess.run(cmd, capture_output=True)

    frames = []
    for i, frame_path in enumerate(sorted(frames_dir.glob("frame_*.png"))):
        timestamp = i * interval_seconds
        frames.append((frame_path, timestamp))

    return frames


def extract_frames_keyframe(
    video_path: Path,
    output_dir: Path
) -> list[tuple[Path, float]]:
    """Extract only keyframes (I-frames)."""
    frames_dir = output_dir / "raw_frames"
    frames_dir.mkdir(exist_ok=True)

    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-vf", "select='eq(pict_type,I)',showinfo",
        "-vsync", "vfr",
        str(frames_dir / "frame_%04d.png"),
        "-y"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    frames = []
    frame_files = sorted(frames_dir.glob("frame_*.png"))

    timestamps = []
    for line in result.stderr.split("\n"):
        if "pts_time:" in line:
            match = re.search(r"pts_time:(\d+\.?\d*)", line)
            if match:
                timestamps.append(float(match.group(1)))

    for i, frame_path in enumerate(frame_files):
        timestamp = timestamps[i] if i < len(timestamps) else i * 5.0
        frames.append((frame_path, timestamp))

    return frames


def extract_frame_at_timestamp(
    video_path: Path,
    timestamp: float,
    output_path: Path
) -> bool:
    """Extract a single frame at a specific timestamp."""
    cmd = [
        "ffmpeg",
        "-ss", str(timestamp),
        "-i", str(video_path),
        "-frames:v", "1",
        "-q:v", "2",
        str(output_path),
        "-y"
    ]

    result = subprocess.run(cmd, capture_output=True)
    return output_path.exists()


def extract_frames_chapters(
    video_path: Path,
    output_dir: Path,
    chapters: list[dict]
) -> list[tuple[Path, float]]:
    """Extract one frame per chapter."""
    frames_dir = output_dir / "raw_frames"
    frames_dir.mkdir(exist_ok=True)

    frames = []
    for i, chapter in enumerate(chapters):
        timestamp = chapter.get("start_time", 0)
        frame_path = frames_dir / f"chapter_{i:02d}.png"

        if extract_frame_at_timestamp(video_path, timestamp + 1, frame_path):
            frames.append((frame_path, timestamp))

    return frames


def compute_phash(image_path: Path) -> str | None:
    """Compute perceptual hash of an image."""
    try:
        import imagehash
        from PIL import Image

        img = Image.open(image_path)
        h = imagehash.phash(img)
        return str(h)
    except Exception:
        return None


def dedupe_frames(
    frames: list[tuple[Path, float]],
    threshold: int = 10
) -> list[tuple[Path, float]]:
    """Remove near-duplicate frames using perceptual hashing."""
    try:
        import imagehash
        from PIL import Image
    except ImportError:
        # If imagehash not available, return all frames
        return frames

    unique = []
    hashes: dict[str, Any] = {}

    for frame_path, timestamp in frames:
        try:
            img = Image.open(frame_path)
            h = imagehash.phash(img)

            is_duplicate = False
            for existing_hash in hashes.values():
                if h - existing_hash < threshold:
                    is_duplicate = True
                    break

            if not is_duplicate:
                hashes[str(frame_path)] = h
                unique.append((frame_path, timestamp))

        except Exception:
            # If we can't process a frame, keep it
            unique.append((frame_path, timestamp))

    return unique


def score_by_text_density(frame_path: Path) -> tuple[float, str]:
    """Score frame by text content using OCR."""
    try:
        import easyocr
    except ImportError:
        return 0.0, ""

    try:
        reader = easyocr.Reader(["en"], verbose=False)
        results = reader.readtext(str(frame_path))

        # Combine all detected text
        text = " ".join(r[1] for r in results)
        # Score based on text length
        score = min(len(text) / 100, 1.0)

        return score, text
    except Exception:
        return 0.0, ""


def classify_frame_ocr(frame_path: Path) -> tuple[str, float, str]:
    """Classify frame based on OCR text patterns."""
    score, text = score_by_text_density(frame_path)
    text_lower = text.lower()

    # Code indicators
    code_patterns = [
        "def ", "class ", "import ", "function", "const ", "let ", "var ",
        "return ", "if (", "for (", "while ", "=>", "->", "::", "//", "/*",
        "{", "}", "[];", "();", "pip install", "npm ", "cargo ", "git "
    ]

    # Diagram indicators
    diagram_patterns = [
        "database", "server", "client", "api", "service", "load balancer",
        "cache", "queue", "gateway", "container", "kubernetes", "docker",
        "aws", "azure", "gcp", "microservice", "architecture"
    ]

    # Check for code
    code_matches = sum(1 for p in code_patterns if p in text_lower or p in text)
    if code_matches >= 3:
        return "code", min(0.5 + code_matches * 0.1, 0.95), text

    # Check for diagrams
    diagram_matches = sum(1 for p in diagram_patterns if p in text_lower)
    if diagram_matches >= 2:
        return "diagram", min(0.5 + diagram_matches * 0.1, 0.95), text

    # High text density likely means slide
    if score > 0.3:
        return "slide", score, text

    # Low text density likely means talking head or other
    if score < 0.1:
        return "talking_head", 0.7, text

    return "other", 0.5, text


def classify_frame_vision(
    frame_path: Path,
    model: str = "claude"
) -> tuple[str, float]:
    """Classify frame using vision model."""
    prompt = """Classify this video frame based on its PRIMARY content.
If there's a person in a small corner but the main area shows something else, classify by the main content.

Categories:
- diagram: Architecture diagram, flowchart, system design, UML, boxes with arrows
- code: Code snippet, terminal output, IDE screenshot, command line
- slide: Presentation slide, document, article, text with bullet points
- chart: Graph, plot, data visualization
- talking_head: ONLY if person's face dominates >50% of frame with no other content
- other: None of the above

Reply with exactly one word: diagram, code, slide, chart, talking_head, or other"""

    try:
        if model == "claude":
            return _classify_with_claude(frame_path, prompt)
        elif model == "gpt4v":
            return _classify_with_gpt4v(frame_path, prompt)
    except Exception:
        pass

    return "other", 0.5


def _classify_with_claude(frame_path: Path, prompt: str) -> tuple[str, float]:
    """Classify using Claude vision."""
    import anthropic
    import base64

    client = anthropic.Anthropic()

    with open(frame_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=50,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data,
                    },
                },
                {"type": "text", "text": prompt}
            ],
        }],
    )

    response = message.content[0].text.strip().lower()

    # Check for exact match first
    if response in FRAME_TYPES:
        return response, 0.9

    # Check if any frame type is mentioned in response
    for frame_type in FRAME_TYPES:
        if frame_type in response:
            return frame_type, 0.85

    return "other", 0.5


def _classify_with_gpt4v(frame_path: Path, prompt: str) -> tuple[str, float]:
    """Classify using GPT-4V."""
    import openai
    import base64

    client = openai.OpenAI()

    with open(frame_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=50,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{image_data}"}
                },
            ],
        }],
    )

    result = response.choices[0].message.content.strip().lower()

    if result in FRAME_TYPES:
        return result, 0.9
    return "other", 0.5


def filter_useful_frames(
    frames: list[tuple[Path, float, str, float, str]],
    max_frames: int = 50
) -> list[tuple[Path, float, str, float, str]]:
    """Filter to keep only useful frames (not talking_head)."""
    useful = [f for f in frames if f[2] != "talking_head"]

    # Sort by confidence, keep top N
    useful.sort(key=lambda x: x[3], reverse=True)

    return useful[:max_frames]


def run_extraction(
    video_id: str,
    output_base: str | None = None,
    strategy: str = "hybrid",
    scene_threshold: float = 0.3,
    interval_seconds: int = 10,
    dedup_threshold: int = 10,
    classifier: str = "ocr",
    max_frames: int = 50,
    keep_video: bool = False,
    max_resolution: int = 1080,
) -> ExtractionResult:
    """Run the full extraction pipeline."""

    # Check dependencies
    if not check_ffmpeg():
        return ExtractionResult(
            success=False,
            video_id=video_id,
            error="ffmpeg not found. Please install ffmpeg."
        )

    # Get video info
    info = get_video_info(video_id)
    title = info.get("title") if info else None
    chapters = info.get("chapters", []) if info else []

    # Download video
    video_path = download_video(video_id, max_resolution)
    if not video_path:
        return ExtractionResult(
            success=False,
            video_id=video_id,
            title=title,
            error="Failed to download video"
        )

    output_dir = get_output_dir(video_id, output_base)

    try:
        # Stage 1: Extract frames based on strategy
        if strategy == "scene-change":
            raw_frames = extract_frames_scene_change(video_path, output_dir, scene_threshold)
        elif strategy == "interval":
            raw_frames = extract_frames_interval(video_path, output_dir, interval_seconds)
        elif strategy == "keyframe":
            raw_frames = extract_frames_keyframe(video_path, output_dir)
        elif strategy == "chapters":
            if not chapters:
                return ExtractionResult(
                    success=False,
                    video_id=video_id,
                    title=title,
                    error="No chapters found for this video"
                )
            raw_frames = extract_frames_chapters(video_path, output_dir, chapters)
        else:  # hybrid
            # Use scene change as primary
            raw_frames = extract_frames_scene_change(video_path, output_dir, scene_threshold)

            # Add chapter frames if available
            if chapters:
                chapter_frames = extract_frames_chapters(video_path, output_dir, chapters)
                raw_frames.extend(chapter_frames)

            # Sort by timestamp
            raw_frames.sort(key=lambda x: x[1])

        initial_count = len(raw_frames)

        # Stage 2: Deduplicate
        deduped_frames = dedupe_frames(raw_frames, dedup_threshold)
        dedup_count = len(deduped_frames)

        # Stage 3: Classify
        classified_frames = []
        for frame_path, timestamp in deduped_frames:
            if classifier == "none":
                classification, confidence, ocr_text = "unknown", 0.0, ""
            elif classifier in ("claude", "gpt4v"):
                classification, confidence = classify_frame_vision(frame_path, classifier)
                ocr_text = ""
            else:  # ocr
                classification, confidence, ocr_text = classify_frame_ocr(frame_path)

            phash = compute_phash(frame_path)
            classified_frames.append((frame_path, timestamp, classification, confidence, ocr_text, phash))

        # Stage 4: Filter useful frames
        useful_frames = [f for f in classified_frames if f[2] != "talking_head"]
        useful_frames.sort(key=lambda x: x[3], reverse=True)
        useful_frames = useful_frames[:max_frames]

        # Stage 5: Rename and organize final frames
        frames_dir = output_dir / "frames"
        frames_dir.mkdir(exist_ok=True)

        final_frames = []
        for frame_path, timestamp, classification, confidence, ocr_text, phash in useful_frames:
            ts_str = format_timestamp(timestamp)
            new_name = f"{ts_str}_{classification}.png"
            new_path = frames_dir / new_name

            shutil.copy2(frame_path, new_path)

            final_frames.append(ExtractedFrame(
                filename=new_name,
                timestamp=timestamp,
                timestamp_formatted=format_timestamp_display(timestamp),
                classification=classification,
                confidence=confidence,
                ocr_text=ocr_text[:500] if ocr_text else None,
                phash=phash,
            ))

        # Clean up raw frames
        raw_frames_dir = output_dir / "raw_frames"
        if raw_frames_dir.exists():
            shutil.rmtree(raw_frames_dir)

        # Clean up video if not keeping
        if not keep_video and video_path.exists():
            video_path.unlink()

        # Write metadata
        metadata = {
            "video_id": video_id,
            "title": title,
            "extracted_at": datetime.now().isoformat(),
            "strategy": strategy,
            "stats": {
                "initial_frames": initial_count,
                "after_dedup": dedup_count,
                "final_frames": len(final_frames),
            },
            "frames": [asdict(f) for f in final_frames],
        }

        with open(output_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        # Write summary markdown
        summary_lines = [
            f"# Extracted Frames: {title or video_id}",
            "",
            f"**Video ID:** {video_id}",
            f"**Extracted:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"**Strategy:** {strategy}",
            f"**Frames:** {len(final_frames)} (from {initial_count} initial)",
            "",
            "## Frames",
            "",
        ]

        for frame in final_frames:
            summary_lines.append(
                f"- **{frame.timestamp_formatted}** [{frame.classification}] "
                f"`{frame.filename}`"
            )

        with open(output_dir / "summary.md", "w") as f:
            f.write("\n".join(summary_lines))

        return ExtractionResult(
            success=True,
            video_id=video_id,
            title=title,
            output_dir=str(output_dir),
            strategy=strategy,
            frames=final_frames,
            stats={
                "initial_frames": initial_count,
                "after_dedup": dedup_count,
                "final_frames": len(final_frames),
            },
        )

    except Exception as e:
        return ExtractionResult(
            success=False,
            video_id=video_id,
            title=title,
            error=str(e)
        )


def cmd_extract(args: list[str]) -> None:
    """Handle extract command."""
    if not args:
        print(json.dumps({
            "success": False,
            "error": "Usage: extract <url> [--output-dir=DIR] [--strategy=hybrid] [--classifier=ocr]"
        }))
        sys.exit(1)

    url = args[0]
    output_dir = None
    strategy = "hybrid"
    classifier = "ocr"

    # Parse optional args
    for arg in args[1:]:
        if arg.startswith("--output-dir="):
            output_dir = arg.split("=", 1)[1]
        elif arg.startswith("--strategy="):
            strategy = arg.split("=", 1)[1]
        elif arg.startswith("--classifier="):
            classifier = arg.split("=", 1)[1]

    try:
        video_id = extract_video_id(url)
        result = run_extraction(
            video_id,
            output_base=output_dir,
            strategy=strategy,
            classifier=classifier,
        )

        output = {
            "success": result.success,
            "video_id": result.video_id,
            "title": result.title,
        }

        if result.success:
            output["output_dir"] = result.output_dir
            output["strategy"] = result.strategy
            output["stats"] = result.stats
            output["frames"] = [asdict(f) for f in result.frames] if result.frames else []
        else:
            output["error"] = result.error

        print(json.dumps(output, indent=2))

    except ValueError as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)


def cmd_quick(args: list[str]) -> None:
    """Handle quick command - fast extraction without classification."""
    if not args:
        print(json.dumps({
            "success": False,
            "error": "Usage: quick <url> [output-dir]"
        }))
        sys.exit(1)

    url = args[0]
    output_dir = args[1] if len(args) > 1 else None

    try:
        video_id = extract_video_id(url)
        result = run_extraction(
            video_id,
            output_base=output_dir,
            strategy="scene-change",
            classifier="none",
        )

        output = {
            "success": result.success,
            "video_id": result.video_id,
            "title": result.title,
        }

        if result.success:
            output["output_dir"] = result.output_dir
            output["frame_count"] = len(result.frames) if result.frames else 0
        else:
            output["error"] = result.error

        print(json.dumps(output, indent=2))

    except ValueError as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)


def cmd_chapters(args: list[str]) -> None:
    """Handle chapters command - extract one frame per chapter."""
    if not args:
        print(json.dumps({
            "success": False,
            "error": "Usage: chapters <url> [output-dir]"
        }))
        sys.exit(1)

    url = args[0]
    output_dir = args[1] if len(args) > 1 else None

    try:
        video_id = extract_video_id(url)
        result = run_extraction(
            video_id,
            output_base=output_dir,
            strategy="chapters",
            classifier="ocr",
        )

        output = {
            "success": result.success,
            "video_id": result.video_id,
            "title": result.title,
        }

        if result.success:
            output["output_dir"] = result.output_dir
            output["frame_count"] = len(result.frames) if result.frames else 0
        else:
            output["error"] = result.error

        print(json.dumps(output, indent=2))

    except ValueError as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)


def cmd_classify(args: list[str]) -> None:
    """Handle classify command - classify existing frames."""
    if not args:
        print(json.dumps({
            "success": False,
            "error": "Usage: classify <frames-dir> [--classifier=ocr]"
        }))
        sys.exit(1)

    frames_dir = Path(args[0]).expanduser()
    classifier = "ocr"

    for arg in args[1:]:
        if arg.startswith("--classifier="):
            classifier = arg.split("=", 1)[1]

    if not frames_dir.exists():
        print(json.dumps({
            "success": False,
            "error": f"Directory not found: {frames_dir}"
        }))
        sys.exit(1)

    results = []
    for frame_path in sorted(frames_dir.glob("*.png")):
        if classifier in ("claude", "gpt4v"):
            classification, confidence = classify_frame_vision(frame_path, classifier)
            ocr_text = ""
        else:
            classification, confidence, ocr_text = classify_frame_ocr(frame_path)

        results.append({
            "filename": frame_path.name,
            "classification": classification,
            "confidence": confidence,
            "ocr_text": ocr_text[:200] if ocr_text else None,
        })

    print(json.dumps({
        "success": True,
        "frames_dir": str(frames_dir),
        "classifier": classifier,
        "results": results,
    }, indent=2))


def cmd_clean(args: list[str]) -> None:
    """Handle clean command - remove cached videos."""
    cache_dir = get_cache_dir()

    if args:
        # Clean specific video
        video_id = args[0]
        video_path = cache_dir / f"{video_id}.mp4"
        if video_path.exists():
            video_path.unlink()
            print(json.dumps({
                "success": True,
                "message": f"Removed cached video: {video_id}"
            }))
        else:
            print(json.dumps({
                "success": True,
                "message": f"No cached video found: {video_id}"
            }))
    else:
        # Clean all
        count = 0
        for video_file in cache_dir.glob("*.mp4"):
            video_file.unlink()
            count += 1

        print(json.dumps({
            "success": True,
            "message": f"Removed {count} cached videos"
        }))


def cmd_list(args: list[str]) -> None:
    """Handle list command - list extracted frame sets."""
    base_dir = Path.home() / ".config" / "pais" / "research" / "youtube-frames"

    if not base_dir.exists():
        print(json.dumps({
            "success": True,
            "extractions": [],
            "message": "No extractions found"
        }))
        return

    extractions = []
    for video_dir in sorted(base_dir.iterdir()):
        if video_dir.is_dir():
            metadata_path = video_dir / "metadata.json"
            if metadata_path.exists():
                with open(metadata_path) as f:
                    metadata = json.load(f)
                extractions.append({
                    "video_id": metadata.get("video_id"),
                    "title": metadata.get("title"),
                    "extracted_at": metadata.get("extracted_at"),
                    "frame_count": len(metadata.get("frames", [])),
                    "path": str(video_dir),
                })

    print(json.dumps({
        "success": True,
        "extractions": extractions,
    }, indent=2))


def cmd_view(args: list[str]) -> None:
    """Handle view command - render frames in terminal with chafa."""
    if not args:
        print("Usage: view <video_id> [--size=WxH] [--filter=TYPE]")
        print("  --size=80x30   Image size (default: 80x30)")
        print("  --filter=code  Only show frames of this type")
        sys.exit(1)

    video_id = args[0]
    size = "80x30"
    filter_type = None

    for arg in args[1:]:
        if arg.startswith("--size="):
            size = arg.split("=", 1)[1]
        elif arg.startswith("--filter="):
            filter_type = arg.split("=", 1)[1]

    # Check for chafa
    if shutil.which("chafa") is None:
        print("Error: chafa not installed. Install with: sudo apt install chafa")
        sys.exit(1)

    # Find extraction directory
    base_dir = Path.home() / ".config" / "pais" / "research" / "youtube-frames"
    video_dir = base_dir / video_id

    if not video_dir.exists():
        print(f"Error: No extraction found for video ID: {video_id}")
        print(f"Run: pais run youtube-frames extract <url>")
        sys.exit(1)

    metadata_path = video_dir / "metadata.json"
    if not metadata_path.exists():
        print(f"Error: No metadata.json in {video_dir}")
        sys.exit(1)

    with open(metadata_path) as f:
        metadata = json.load(f)

    title = metadata.get("title", video_id)
    frames = metadata.get("frames", [])

    # Filter frames if requested
    if filter_type:
        frames = [f for f in frames if f.get("classification") == filter_type]

    if not frames:
        print(f"No frames found" + (f" matching filter '{filter_type}'" if filter_type else ""))
        sys.exit(0)

    # Print header
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"  Video ID: {video_id}")
    print(f"  Frames: {len(frames)}" + (f" (filtered: {filter_type})" if filter_type else ""))
    print(f"{'=' * 80}\n")

    frames_dir = video_dir / "frames"

    for i, frame in enumerate(frames):
        filename = frame.get("filename")
        timestamp = frame.get("timestamp_formatted", "?")
        classification = frame.get("classification", "unknown")
        confidence = frame.get("confidence", 0)

        frame_path = frames_dir / filename
        if not frame_path.exists():
            print(f"[{i+1}/{len(frames)}] {timestamp} - {classification} (file missing)")
            continue

        # Print frame header
        print(f"┌{'─' * 78}┐")
        print(f"│ [{i+1}/{len(frames)}] {timestamp} │ {classification} (conf: {confidence:.0%}) │ {filename}")
        print(f"├{'─' * 78}┤")

        # Render with chafa
        try:
            result = subprocess.run(
                ["chafa", f"--size={size}", str(frame_path)],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(result.stdout)
            else:
                print(f"  (chafa error: {result.stderr.strip()})")
        except Exception as e:
            print(f"  (render error: {e})")

        print(f"└{'─' * 78}┘")
        print()

    # Print summary
    print(f"{'=' * 80}")
    print(f"  Total: {len(frames)} frames")
    if not filter_type:
        # Show breakdown by type
        by_type: dict[str, int] = {}
        for f in frames:
            t = f.get("classification", "unknown")
            by_type[t] = by_type.get(t, 0) + 1
        breakdown = ", ".join(f"{k}: {v}" for k, v in sorted(by_type.items()))
        print(f"  Types: {breakdown}")
    print(f"{'=' * 80}\n")


def main() -> None:
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "Usage: main.py <action> [args...]",
            "actions": ["extract", "quick", "chapters", "classify", "clean", "list"],
        }))
        sys.exit(1)

    action = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        "extract": cmd_extract,
        "quick": cmd_quick,
        "chapters": cmd_chapters,
        "classify": cmd_classify,
        "clean": cmd_clean,
        "list": cmd_list,
        "view": cmd_view,
    }

    if action not in commands:
        print(json.dumps({
            "success": False,
            "error": f"Unknown action: {action}",
            "available": list(commands.keys()),
        }))
        sys.exit(1)

    commands[action](args)


if __name__ == "__main__":
    main()
