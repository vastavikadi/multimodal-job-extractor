import random

from .reels_metadata import get_reel_info
import json
import time
from datetime import datetime, UTC

def extract_reel_id(url):
    # Example URL: https://www.instagram.com/username/reel/Cr9n2X8s1aP/
    parts = url.strip("/").split("/")
    if "reel" in parts:
        reel_index = parts.index("reel")
        if reel_index + 1 < len(parts):
            print(f"Extracted reel ID: {parts[reel_index + 1]} from URL: {url}")
            return parts[reel_index + 1]
    return None

def save_reel_info(table):
    with open("jsons/reels_links.json", "r") as f:
        links = json.load(f)
        for link in links:
            # check if reel ID already exists in the database
            reel_id = extract_reel_id(link)
            if table.find_one({"id": reel_id}):
                print(f"Reel ID {reel_id} already exists in the database. Skipping.")
                continue
            try:
                reel_info = get_reel_info(link)
                if not reel_id:
                    continue
                doc = {
                    "id": reel_info["id"],
                    "title": reel_info["title"],
                    "description": reel_info["description"],
                    "channel": reel_info["channel"],
                    "uploader": reel_info["uploader"],
                    "uploader_id": reel_info["uploader_id"],
                    "uploaded_at": datetime.fromtimestamp(reel_info["timestamp"],tz=UTC),
                    "duration": reel_info["duration"],
                    "like_count": reel_info["like_count"],
                    "comment_count": reel_info["comment_count"],
                    "downloaded": False,
                    "processed": False,
                }
                table.insert_one(doc)
            except Exception as e:
                print(f"Failed to process link {link}: {e}")
            sleep_time = random.uniform(8, 20)
            print(f"Sleeping for {sleep_time:.1f}s")
            time.sleep(sleep_time)