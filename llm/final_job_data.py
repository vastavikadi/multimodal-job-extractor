import json
from .main import extract_job_info

def final_job_data(table):
    reels = table.find({"downloaded": True, "processed": False})
    for reel in reels:
        final_data = table.find_one({"id": reel["id"]}, {"final_job_data": 1}).get("final_job_data", "")
        if final_data:
            print(f"Final job data already exists for reel {reel['id']}, skipping.")
            continue
        job_json = extract_job_info(
            reel["description"],
            reel["ocr_text"],
            reel["transcript"]
            )

        table.update_one(
            {"id": reel["id"]},
            {
                "$set": {
                    "final_job_data": json.dumps(job_json),
                    "processed": True
                }
            }
        )