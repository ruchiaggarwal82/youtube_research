import anthropic
from config import COLLATE_MODEL

client = anthropic.Anthropic()


def collate_summaries(goal: str, video_results: list[dict]) -> str:
    if not video_results:
        return "No videos to collate."

    videos_text = ""
    for i, r in enumerate(video_results, 1):
        videos_text += f"\n[{i}] {r['meta']['title']} — {r['meta']['channel']}\n"
        videos_text += r["summaries"]["long"] + "\n"

    prompt = f"""You analyzed {len(video_results)} YouTube videos for this research goal:
GOAL: {goal}

Here are the per-video summaries:
{videos_text}

Write a collated research brief (300-400 words) covering:
1. Main themes and consensus across videos
2. Contrasting views or disagreements
3. Most important insights relevant to the goal
4. Which videos are most worth watching in full (and why)
"""

    message = client.messages.create(
        model=COLLATE_MODEL,
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()
