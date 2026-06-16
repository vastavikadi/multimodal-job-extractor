import yt_dlp
import os
import random
import time


def download_reels(table):
    processed_count = 0
    reels = table.find({"downloaded": False}).limit(20)
    for reel in reels:
        reel_id = reel["id"]

        url = f"https://www.instagram.com/reel/{reel_id}/"

        os.makedirs("videos", exist_ok=True)
        video_path = f"videos/{reel_id}.%(ext)s"
        try:
            ydl_opts = {
                "outtmpl": video_path,
                "cookiefile": "sessions/instagram_cookies.txt",
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if os.path.exists(f"videos/{reel_id}.mp4"):
                    print(f"Reel {reel_id} already downloaded. Skipping.")
                    table.update_one({"id": reel_id}, {"$set": {"downloaded": True, "video_path": f"videos/{reel_id}.mp4"}})
                    continue
                ydl.download([url])
            
            # find the downloaded file (since yt_dlp might add an extension)
            for file in os.listdir("videos"):
                if file.startswith(reel_id):
                    video_path = os.path.join("videos", file)
                    break

            table.update_one({"id": reel_id}, {"$set": {"downloaded": True, "video_path": video_path}})
            print(f"Downloaded and updated reel {reel_id} successfully.")

        except Exception as e:
            print(f"Failed {reel_id}: {e}")

        processed_count += 1
        sleep_time = random.uniform(8, 20)
        print(f"Sleeping for {sleep_time:.1f}s")
        time.sleep(sleep_time)
        if processed_count % 20 == 0:
            break_time = random.uniform(60, 180)

            print(
                f"Taking a long break "
                f"for {break_time:.1f}s"
            )

            time.sleep(break_time)