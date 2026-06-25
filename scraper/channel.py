import scrapetube
from config import MAX_VIDEOS


def get_channel_videos(channel_input: str, limit: int = MAX_VIDEOS) -> list[str]:
    """
    Returns a list of video IDs from a channel.
    channel_input can be a handle (@mkbhd), channel name, or full channel URL.
    Videos are returned sorted by view count (most viewed first).
    """
    kwargs = {"limit": limit * 2, "sort_by": "popular"}  # fetch extra, then trim

    if channel_input.startswith("http"):
        kwargs["channel_url"] = channel_input
    elif channel_input.startswith("@"):
        kwargs["channel_username"] = channel_input
    else:
        # treat as handle without @
        kwargs["channel_username"] = f"@{channel_input}"

    try:
        videos = scrapetube.get_channel(**kwargs)
        ids = [v["videoId"] for v in videos]
        return ids[:limit]
    except Exception as e:
        raise RuntimeError(f"Could not fetch channel '{channel_input}': {e}")
