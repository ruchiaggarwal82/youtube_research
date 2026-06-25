from youtube_transcript_api import YouTubeTranscriptApi
import re


def extract_video_id(url_or_id: str) -> str:
    patterns = [
        r"(?:v=|youtu\.be/|embed/|shorts/)([A-Za-z0-9_-]{11})",
        r"^([A-Za-z0-9_-]{11})$",
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url_or_id}")


def fetch_transcript(video_id: str) -> str:
    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        return " ".join(entry.text for entry in transcript)
    except Exception:
        return ""
