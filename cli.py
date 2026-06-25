#!/usr/bin/env python3
import sys
from config import MAX_VIDEOS
from scraper.transcript import fetch_transcript, extract_video_id
from scraper.metadata import fetch_metadata
from scraper.channel import get_channel_videos
from summarizer.video import summarize_video
from summarizer.collate import collate_summaries
from storage.session import save_session, list_sessions, load_session


def print_divider(char="─", width=60):
    print(char * width)


def prompt(text: str, default: str = "") -> str:
    result = input(text).strip()
    return result if result else default


def run_research():
    print_divider("═")
    print("  YouTube Research Tool")
    print_divider("═")

    goal = prompt("\nWhat is your research goal?\n> ")
    if not goal:
        print("A goal is required.")
        return

    print("\nInput mode:")
    print("  1. Channel name(s)")
    print("  2. Specific video URL(s)")
    print("  3. Both")
    mode = prompt("Choose [1/2/3]: ", "1")

    channel_inputs = []
    url_inputs = []

    if mode in ("1", "3"):
        raw = prompt("\nEnter channel handle(s) or names, comma-separated (e.g. @mkbhd, @veritasium):\n> ")
        channel_inputs = [c.strip() for c in raw.split(",") if c.strip()]

    if mode in ("2", "3"):
        raw = prompt("\nEnter video URL(s), comma-separated:\n> ")
        url_inputs = [u.strip() for u in raw.split(",") if u.strip()]

    videos_per_channel = MAX_VIDEOS
    if channel_inputs:
        try:
            n = prompt(f"\nHow many videos per channel? (max {MAX_VIDEOS}, default {MAX_VIDEOS}): ", str(MAX_VIDEOS))
            videos_per_channel = min(int(n), MAX_VIDEOS)
        except ValueError:
            videos_per_channel = MAX_VIDEOS

    detail = prompt("\nSummary detail? [short/long/both] (default: both): ", "both").lower()
    if detail not in ("short", "long", "both"):
        detail = "both"

    # Collect all video IDs
    video_ids = []

    for ch in channel_inputs:
        print(f"\nFetching videos from channel: {ch} ...")
        try:
            ids = get_channel_videos(ch, limit=videos_per_channel)
            print(f"  Found {len(ids)} video(s)")
            video_ids.extend(ids)
        except RuntimeError as e:
            print(f"  ERROR: {e}")

    for url in url_inputs:
        try:
            vid = extract_video_id(url)
            video_ids.append(vid)
        except ValueError as e:
            print(f"  ERROR: {e}")

    if not video_ids:
        print("\nNo videos to process.")
        return

    # Deduplicate while preserving order
    seen = set()
    video_ids = [v for v in video_ids if not (v in seen or seen.add(v))]
    print(f"\nProcessing {len(video_ids)} video(s) total...")

    video_results = []
    for i, vid in enumerate(video_ids, 1):
        print(f"\n[{i}/{len(video_ids)}] Fetching metadata & transcript...")
        try:
            meta = fetch_metadata(vid)
            print(f"  {meta['title'][:60]}")
        except Exception as e:
            print(f"  ERROR fetching metadata: {e}")
            continue

        transcript = fetch_transcript(vid)
        if not transcript:
            print("  Warning: no transcript available")

        print(f"  Summarizing...")
        summaries = summarize_video(meta, transcript, goal)
        video_results.append({"meta": meta, "summaries": summaries})

    if not video_results:
        print("\nNo results to show.")
        return

    # Collate
    print(f"\nGenerating collated research brief...")
    collation = collate_summaries(goal, video_results)

    # Display results
    print_divider("═")
    print(f"\nRESEARCH GOAL: {goal}\n")
    print_divider()

    for r in video_results:
        m = r["meta"]
        print(f"\n▶ {m['title']}")
        print(f"  Channel: {m['channel']} | Views: {m['views']:,} | {m['url']}")
        if detail in ("short", "both"):
            print(f"\n  SHORT SUMMARY:")
            for line in r["summaries"]["short"].splitlines():
                print(f"    {line}")
        if detail in ("long", "both"):
            print(f"\n  DETAILED SUMMARY:")
            for line in r["summaries"]["long"].splitlines():
                print(f"    {line}")
        print_divider()

    print("\n COLLATED RESEARCH BRIEF:")
    print_divider()
    print(collation)
    print_divider()

    # Save
    save = prompt("\nSave this session? [y/n] (default: y): ", "y").lower()
    if save == "y":
        session_id = save_session(goal, video_results, collation)
        print(f"Saved as session: {session_id}")


def view_sessions():
    sessions = list_sessions()
    if not sessions:
        print("No saved sessions found.")
        return

    print(f"\nSaved sessions ({len(sessions)}):")
    print_divider()
    for s in sessions:
        date = s["created_at"][:10]
        print(f"  [{date}] {s['id']}")
        print(f"    Goal: {s['goal'][:70]}")
        print(f"    Videos: {s['video_count']}")
        print()

    session_id = prompt("Enter session ID to view (or press Enter to skip): ")
    if not session_id:
        return

    try:
        data = load_session(session_id)
    except FileNotFoundError as e:
        print(e)
        return

    print_divider("═")
    print(f"GOAL: {data['goal']}\n")
    for r in data["videos"]:
        m = r["meta"]
        print(f"\n▶ {m['title']}")
        print(f"  {m['url']}")
        print(f"  SHORT: {r['summaries']['short'][:200]}")
    print_divider()
    print("COLLATION:")
    print(data["collation"])
    print_divider()


def main():
    print("\nYouTube Research Tool")
    print("1. New research session")
    print("2. View saved sessions")
    print("3. Exit")
    choice = prompt("\nChoose [1/2/3]: ", "1")

    if choice == "1":
        run_research()
    elif choice == "2":
        view_sessions()
    elif choice == "3":
        sys.exit(0)
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
