import re
from config import MAX_CHUNK_TOKENS, RELEVANT_CHUNKS_PER_VIDEO


def _split_into_chunks(text: str, words_per_chunk: int = 400) -> list[str]:
    words = text.split()
    return [
        " ".join(words[i : i + words_per_chunk])
        for i in range(0, len(words), words_per_chunk)
    ]


def _score_chunk(chunk: str, goal: str) -> int:
    goal_words = set(re.findall(r"\w+", goal.lower()))
    chunk_words = re.findall(r"\w+", chunk.lower())
    return sum(1 for w in chunk_words if w in goal_words)


def select_relevant_chunks(transcript: str, goal: str) -> str:
    if not transcript:
        return ""
    chunks = _split_into_chunks(transcript)
    if len(chunks) <= RELEVANT_CHUNKS_PER_VIDEO:
        return transcript
    scored = sorted(enumerate(chunks), key=lambda x: _score_chunk(x[1], goal), reverse=True)
    top = sorted(scored[:RELEVANT_CHUNKS_PER_VIDEO], key=lambda x: x[0])
    return "\n...\n".join(c for _, c in top)
