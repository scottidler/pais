#!/usr/bin/env python3
"""
YouTube extraction plugin for PAIS.

Extracts transcripts, chapters, comments, and metadata from YouTube videos.
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Any


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


def get_youtube_api_key() -> str | None:
    """Get YouTube API key from environment or fabric config."""
    # Check environment first
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if api_key:
        return api_key

    # Check fabric's .env file
    fabric_env = Path.home() / ".config" / "fabric" / ".env"
    if fabric_env.exists():
        with open(fabric_env) as f:
            for line in f:
                if line.startswith("YOUTUBE_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")

    # Check pais config
    pais_env = Path.home() / ".config" / "pais" / ".env"
    if pais_env.exists():
        with open(pais_env) as f:
            for line in f:
                if line.startswith("YOUTUBE_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")

    return None


def get_transcript(video_id: str, fmt: str = "text") -> dict[str, Any]:
    """Fetch transcript using youtube-transcript-api."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api._errors import (
            NoTranscriptFound,
            TranscriptsDisabled,
            VideoUnavailable,
        )
    except ImportError:
        return {
            "success": False,
            "error": "youtube-transcript-api not installed. Run: uv pip install youtube-transcript-api",
        }

    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.list(video_id)

        # Try to get manually created transcript first, then auto-generated
        transcript = None
        for t in transcript_list:
            if not t.is_generated:
                transcript = t.fetch()
                break

        if transcript is None:
            transcript = transcript_list.find_generated_transcript(["en"]).fetch()

        # Convert FetchedTranscript to list of dicts for consistent handling
        snippets = [
            {"text": s.text, "start": s.start, "duration": s.duration}
            for s in transcript.snippets
        ]

        if fmt == "json":
            return {"success": True, "transcript": snippets}
        elif fmt == "srt":
            lines = []
            for i, entry in enumerate(snippets, 1):
                start = entry["start"]
                duration = entry.get("duration", 0)
                end = start + duration
                lines.append(str(i))
                lines.append(f"{format_timestamp(start)} --> {format_timestamp(end)}")
                lines.append(entry["text"])
                lines.append("")
            return {"success": True, "transcript": "\n".join(lines)}
        else:
            # Plain text
            text = " ".join(entry["text"] for entry in snippets)
            return {"success": True, "transcript": text}

    except VideoUnavailable:
        return {"success": False, "error": f"Video unavailable: {video_id}"}
    except TranscriptsDisabled:
        return {"success": False, "error": f"Transcripts disabled for video: {video_id}"}
    except NoTranscriptFound:
        return {"success": False, "error": f"No transcript found for video: {video_id}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def format_timestamp(seconds: float) -> str:
    """Format seconds as SRT timestamp."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def format_time_simple(seconds: float) -> str:
    """Format seconds as MM:SS or HH:MM:SS."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def get_video_info(video_id: str) -> dict[str, Any]:
    """Get video metadata using yt-dlp."""
    try:
        import yt_dlp
    except ImportError:
        return {
            "success": False,
            "error": "yt-dlp not installed. Run: uv pip install yt-dlp",
        }

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)

            return {
                "success": True,
                "info": {
                    "id": info.get("id"),
                    "title": info.get("title"),
                    "channel": info.get("channel"),
                    "channel_id": info.get("channel_id"),
                    "duration": info.get("duration"),
                    "duration_string": info.get("duration_string"),
                    "view_count": info.get("view_count"),
                    "upload_date": info.get("upload_date"),
                    "description": info.get("description"),
                    "tags": info.get("tags", []),
                    "categories": info.get("categories", []),
                    "chapters": info.get("chapters", []),
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                },
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_chapters(video_id: str) -> dict[str, Any]:
    """Extract chapters from video."""
    info_result = get_video_info(video_id)

    if not info_result["success"]:
        return info_result

    info = info_result["info"]
    chapters = info.get("chapters", [])

    # If no chapters from yt-dlp, try to parse from description
    if not chapters and info.get("description"):
        chapters = parse_chapters_from_description(info["description"])

    if not chapters:
        return {
            "success": True,
            "chapters": [],
            "message": "No chapters found for this video",
        }

    # Format chapters nicely
    formatted = []
    for ch in chapters:
        formatted.append({
            "title": ch.get("title", "Untitled"),
            "start_time": ch.get("start_time", 0),
            "start_time_formatted": format_time_simple(ch.get("start_time", 0)),
            "end_time": ch.get("end_time"),
        })

    return {"success": True, "chapters": formatted}


def parse_chapters_from_description(description: str) -> list[dict]:
    """Parse timestamp chapters from video description."""
    chapters = []
    lines = description.split("\n")

    # Pattern: timestamp followed by title
    # Examples: "0:00 Intro", "1:23:45 Main topic", "00:00 - Introduction"
    pattern = r"^(\d{1,2}:)?(\d{1,2}):(\d{2})\s*[-–—]?\s*(.+)$"

    for line in lines:
        line = line.strip()
        match = re.match(pattern, line)
        if match:
            hours = int(match.group(1).rstrip(":")) if match.group(1) else 0
            minutes = int(match.group(2))
            seconds = int(match.group(3))
            title = match.group(4).strip()

            total_seconds = hours * 3600 + minutes * 60 + seconds
            chapters.append({
                "title": title,
                "start_time": total_seconds,
            })

    return chapters


def get_comments(video_id: str, max_results: int = 100) -> dict[str, Any]:
    """Fetch video comments using YouTube Data API."""
    api_key = get_youtube_api_key()
    if not api_key:
        return {
            "success": False,
            "error": "YOUTUBE_API_KEY not found. Set it in environment, ~/.config/fabric/.env, or ~/.config/pais/.env",
        }

    try:
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError
    except ImportError:
        return {
            "success": False,
            "error": "google-api-python-client not installed. Run: uv pip install google-api-python-client",
        }

    try:
        youtube = build("youtube", "v3", developerKey=api_key)

        comments = []
        request = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video_id,
            textFormat="plainText",
            maxResults=min(max_results, 100),
        )
        response = request.execute()

        for item in response.get("items", []):
            top_comment = item["snippet"]["topLevelComment"]["snippet"]
            comment_data = {
                "author": top_comment.get("authorDisplayName"),
                "text": top_comment.get("textDisplay"),
                "likes": top_comment.get("likeCount", 0),
                "published": top_comment.get("publishedAt"),
                "replies": [],
            }

            # Get replies if any
            if item.get("replies"):
                for reply in item["replies"]["comments"]:
                    reply_snippet = reply["snippet"]
                    comment_data["replies"].append({
                        "author": reply_snippet.get("authorDisplayName"),
                        "text": reply_snippet.get("textDisplay"),
                        "likes": reply_snippet.get("likeCount", 0),
                        "published": reply_snippet.get("publishedAt"),
                    })

            comments.append(comment_data)

        return {
            "success": True,
            "comment_count": len(comments),
            "comments": comments,
        }

    except HttpError as e:
        error_reason = e.error_details[0]["reason"] if e.error_details else str(e)
        if "commentsDisabled" in str(e):
            return {"success": False, "error": "Comments are disabled for this video"}
        return {"success": False, "error": f"YouTube API error: {error_reason}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def cmd_transcript(args: list[str]) -> None:
    """Handle transcript command."""
    if not args:
        print(json.dumps({"success": False, "error": "Usage: transcript <url> [format]"}))
        sys.exit(1)

    url = args[0]
    fmt = args[1] if len(args) > 1 else "text"

    try:
        video_id = extract_video_id(url)
        result = get_transcript(video_id, fmt)
        print(json.dumps(result, indent=2))
    except ValueError as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)


def cmd_chapters(args: list[str]) -> None:
    """Handle chapters command."""
    if not args:
        print(json.dumps({"success": False, "error": "Usage: chapters <url>"}))
        sys.exit(1)

    try:
        video_id = extract_video_id(args[0])
        result = get_chapters(video_id)
        print(json.dumps(result, indent=2))
    except ValueError as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)


def cmd_info(args: list[str]) -> None:
    """Handle info command."""
    if not args:
        print(json.dumps({"success": False, "error": "Usage: info <url>"}))
        sys.exit(1)

    try:
        video_id = extract_video_id(args[0])
        result = get_video_info(video_id)
        print(json.dumps(result, indent=2))
    except ValueError as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)


def cmd_comments(args: list[str]) -> None:
    """Handle comments command."""
    if not args:
        print(json.dumps({"success": False, "error": "Usage: comments <url> [max_results]"}))
        sys.exit(1)

    url = args[0]
    max_results = int(args[1]) if len(args) > 1 else 100

    try:
        video_id = extract_video_id(url)
        result = get_comments(video_id, max_results)
        print(json.dumps(result, indent=2))
    except ValueError as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)


def cmd_summarize(args: list[str]) -> None:
    """Handle summarize command - outputs transcript formatted for LLM processing."""
    if not args:
        print(json.dumps({"success": False, "error": "Usage: summarize <url> [pattern]"}))
        sys.exit(1)

    url = args[0]
    pattern = args[1] if len(args) > 1 else "extract_wisdom"

    try:
        video_id = extract_video_id(url)

        # Get video info
        info_result = get_video_info(video_id)
        if not info_result["success"]:
            print(json.dumps(info_result))
            sys.exit(1)

        # Get transcript
        transcript_result = get_transcript(video_id, "text")
        if not transcript_result["success"]:
            print(json.dumps(transcript_result))
            sys.exit(1)

        # Get chapters
        chapters_result = get_chapters(video_id)

        info = info_result["info"]
        transcript = transcript_result["transcript"]
        chapters = chapters_result.get("chapters", [])

        # Format for LLM processing
        output = {
            "success": True,
            "video": {
                "title": info.get("title"),
                "channel": info.get("channel"),
                "url": info.get("url"),
                "duration": info.get("duration_string"),
            },
            "suggested_pattern": pattern,
            "chapters": chapters,
            "transcript": transcript,
            "prompt_hint": f"Apply the '{pattern}' Fabric pattern to analyze this transcript.",
        }

        print(json.dumps(output, indent=2))

    except ValueError as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)


def cmd_pipe(args: list[str]) -> None:
    """Handle pipe command - outputs plain text transcript for piping to fabric."""
    if not args:
        sys.stderr.write("Usage: pipe <url>\n")
        sys.exit(1)

    url = args[0]

    try:
        video_id = extract_video_id(url)
        result = get_transcript(video_id, "text")

        if not result["success"]:
            sys.stderr.write(f"Error: {result['error']}\n")
            sys.exit(1)

        # Output plain text only - no JSON wrapper
        print(result["transcript"])

    except ValueError as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


def cmd_all(args: list[str]) -> None:
    """Handle all command - extract everything."""
    if not args:
        print(json.dumps({"success": False, "error": "Usage: all <url>"}))
        sys.exit(1)

    try:
        video_id = extract_video_id(args[0])

        # Get all data
        info_result = get_video_info(video_id)
        transcript_result = get_transcript(video_id, "text")
        transcript_json = get_transcript(video_id, "json")
        chapters_result = get_chapters(video_id)
        comments_result = get_comments(video_id)

        result = {
            "success": True,
            "video_id": video_id,
        }

        if info_result["success"]:
            result["info"] = info_result["info"]
        else:
            result["info_error"] = info_result.get("error")

        if transcript_result["success"]:
            result["transcript_text"] = transcript_result["transcript"]
        else:
            result["transcript_error"] = transcript_result.get("error")

        if transcript_json["success"]:
            result["transcript_timed"] = transcript_json["transcript"]

        if chapters_result["success"]:
            result["chapters"] = chapters_result.get("chapters", [])

        if comments_result["success"]:
            result["comments"] = comments_result.get("comments", [])
        else:
            result["comments_error"] = comments_result.get("error")

        print(json.dumps(result, indent=2))

    except ValueError as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)


def main() -> None:
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "Usage: main.py <action> [args...]",
            "actions": ["transcript", "chapters", "info", "comments", "summarize", "pipe", "all"],
        }))
        sys.exit(1)

    action = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        "transcript": cmd_transcript,
        "chapters": cmd_chapters,
        "info": cmd_info,
        "comments": cmd_comments,
        "summarize": cmd_summarize,
        "pipe": cmd_pipe,
        "all": cmd_all,
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
