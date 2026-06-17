from .main import extract_job_info

def final_job_data(table):
    reels = table.find({"downloaded": True, "processed": False})
    for reel in reels:
        if reel.get("final_job_data"):
            print(
                f"Final job data already exists for "
                f"reel {reel['id']}, skipping."
            )
            continue
        try:
            job_json = extract_job_info(
                reel.get("description", ""),
                reel.get("ocr_text", ""),
                reel.get("transcript", "")
                )

            table.update_one(
                {"id": reel["id"]},
                {
                    "$set": {
                        "final_job_data": job_json,
                        "processed": True
                    }
                }
            )
            print(
                f"Successfully processed "
                f"{reel['id']}"
            )
        except Exception as error:
            print(
                f"Error processing reel "
                f"{reel['id']}: {error}"
            )