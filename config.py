import os
from pathlib import Path

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

SESSIONS_DIR = Path(__file__).parent / "sessions"
SESSIONS_DIR.mkdir(exist_ok=True)

SUMMARY_MODEL = "claude-haiku-4-5-20251001"
COLLATE_MODEL = "claude-sonnet-4-6"

MAX_VIDEOS = 10
MAX_CHUNK_TOKENS = 2000   # tokens per transcript chunk sent to LLM
RELEVANT_CHUNKS_PER_VIDEO = 4  # top chunks to keep per video
