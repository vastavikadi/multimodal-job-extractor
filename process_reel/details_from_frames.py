import easyocr
import os
import re

reader = easyocr.Reader(["en"])

frames_root = "frames"

def normalize(text):
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text

def extract_text_from_frames(table):
    if not os.path.exists(frames_root):
        print(f"Frames directory '{frames_root}' does not exist.")
        return
    for reel_id in os.listdir(frames_root):
        reel_dir = os.path.join(frames_root, reel_id)

        if not os.path.isdir(reel_dir):
            continue
        try:
            reel = table.find_one({"id": reel_id})
        except Exception as e:
            print(f"Database lookup failed for {reel_id}: {e}")
            continue
        
        if not reel:
            print(f"Reel {reel_id} not found in DB.")
            continue
        
        # Skip already processed reels
        if reel.get("ocr_text"):
            print(f"OCR text already exists for {reel_id}, skipping frame processing.")
            continue
        frame_files = sorted(
            f for f in os.listdir(reel_dir)
            if f.lower().endswith(".jpg")
        )

        if not frame_files:
            print(f"No frames found for {reel_id}")
        
            try:
                table.update_one(
                    {"id": reel_id},
                    {
                        "$set": {
                            "ocr_text": "",
                            "ocr_processed": True
                        }
                    }
                )
            except Exception as e:
                print(
                    f"Failed to mark empty reel "
                    f"{reel_id}: {e}"
                )

            continue
        
        print(f"\nProcessing reel: {reel_id}")

        reel_text = []
        seen = set()

        frame_files = sorted(
            f for f in os.listdir(reel_dir)
            if f.endswith(".jpg")
        )

        print(f"\nProcessing reel: {reel_id}")

        for frame_file in frame_files:
            frame_path = os.path.join(reel_dir, frame_file)

            try:
                results = reader.readtext(frame_path)

                for _, text, confidence in results:

                    # Skip low-confidence OCR
                    if confidence < 0.50:
                        continue

                    text = text.strip()

                    if not text:
                        continue

                    normalized = normalize(text)

                    if normalized not in seen:
                        seen.add(normalized)
                        reel_text.append(text)

            except Exception as e:
                print(f"Error processing {frame_path}: {e}")

        ocr_text = "\n".join(reel_text)

        try:
            table.update_one(
                {"id": reel_id},
                {
                    "$set": {
                        "ocr_text": ocr_text,
                    }
                }
            )

            print(
                f"Processed {reel_id} | "
                f"{len(reel_text)} unique text lines"
            )

        except Exception as e:
            print(
                f"Error updating database "
                f"for {reel_id}: {e}"
            )