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
    for reel_id in os.listdir(frames_root):
        ocr_text = table.find_one({"id": reel_id}, {"ocr_text": 1}).get("ocr_text", "")
        if ocr_text:
            print(f"OCR text already exists for {reel_id}, skipping frame processing.")
            continue
        reel_dir = os.path.join(frames_root, reel_id)

        if not os.path.isdir(reel_dir):
            continue

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