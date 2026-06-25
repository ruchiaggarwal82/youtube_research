import json
import uuid
from datetime import datetime
from pathlib import Path
from config import SESSIONS_DIR


def save_session(goal: str, video_results: list[dict], collation: str) -> str:
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:6]
    data = {
        "id": session_id,
        "created_at": datetime.now().isoformat(),
        "goal": goal,
        "video_count": len(video_results),
        "videos": video_results,
        "collation": collation,
    }
    path = SESSIONS_DIR / f"{session_id}.json"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    return session_id


def list_sessions() -> list[dict]:
    sessions = []
    for f in sorted(SESSIONS_DIR.glob("*.json"), reverse=True):
        try:
            data = json.loads(f.read_text())
            sessions.append({
                "id": data["id"],
                "created_at": data["created_at"],
                "goal": data["goal"],
                "video_count": data["video_count"],
            })
        except Exception:
            continue
    return sessions


def load_session(session_id: str) -> dict:
    path = SESSIONS_DIR / f"{session_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Session not found: {session_id}")
    return json.loads(path.read_text())
