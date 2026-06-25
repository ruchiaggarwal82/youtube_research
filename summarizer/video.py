import anthropic
from config import SUMMARY_MODEL
from summarizer.chunker import select_relevant_chunks

client = anthropic.Anthropic()


def summarize_video(meta: dict, transcript: str, goal: str) -> dict:
    relevant = select_relevant_chunks(transcript, goal)

    if not relevant:
        return {
            "short": "No transcript available.",
            "long": "No transcript available for this video.",
        }

    prompt = f"""You are analyzing a YouTube video to help with the following research goal:
GOAL: {goal}

VIDEO: "{meta['title']}" by {meta['channel']} ({meta['views']:,} views)
DESCRIPTION: {meta['description']}

TRANSCRIPT EXCERPT:
{relevant}

Provide two summaries:

SHORT (3-5 bullet points, goal-aligned, be specific):
-

LONG (150-250 words covering: key claims, relevant insights, notable quotes, how it relates to the goal):
"""

    message = client.messages.create(
        model=SUMMARY_MODEL,
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = message.content[0].text.strip()

    short, long = "", raw
    if "LONG" in raw:
        parts = raw.split("LONG", 1)
        short = parts[0].replace("SHORT", "").strip()
        long = parts[1].strip().lstrip("(150-250 words covering: key claims, relevant insights, notable quotes, how it relates to the goal):").strip()
    elif "SHORT" in raw:
        short = raw.replace("SHORT", "").strip()

    return {"short": short, "long": long}
