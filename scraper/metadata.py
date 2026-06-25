import yt_dlp


def fetch_metadata(video_id: str) -> dict:
    url = f"https://www.youtube.com/watch?v={video_id}"
    opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extract_flat": False,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return {
        "video_id": video_id,
        "title": info.get("title", ""),
        "channel": info.get("uploader", ""),
        "views": info.get("view_count", 0),
        "upload_date": info.get("upload_date", ""),
        "duration_seconds": info.get("duration", 0),
        "url": url,
        "description": (info.get("description") or "")[:500],
    }
