from faster_whisper import WhisperModel
import os

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

videos_root = "videos"


def transcribe_video(table):

    if not os.path.exists(videos_root):
        print(f"Directory '{videos_root}' does not exist.")
        return

    for filename in os.listdir(videos_root):

        if not filename.lower().endswith(".mp4"):
            continue

        reel_id = os.path.splitext(filename)[0]
        video_path = os.path.join(videos_root, filename)

        try:
            reel = table.find_one({"id": reel_id})

            if not reel:
                print(f"Reel {reel_id} not found in DB.")
                continue

            if reel.get("transcript_processed"):
                print(
                    f"Transcript already processed for "
                    f"{reel_id}, skipping."
                )
                continue

            print(f"Transcribing {reel_id}...")

            segments, info = model.transcribe(
                video_path,
                beam_size=5
            )

            transcript_parts = []

            for segment in segments:
                transcript_parts.append(segment.text.strip())

            transcript = " ".join(transcript_parts).strip()

            table.update_one(
                {"id": reel_id},
                {
                    "$set": {
                        "transcript": transcript,
                        "transcript_processed": True
                    }
                }
            )

            print(
                f"Completed {reel_id} | "
                f"{len(transcript)} characters"
            )

        except Exception as e:
            print(
                f"Error processing "
                f"{video_path}: {e}"
            )