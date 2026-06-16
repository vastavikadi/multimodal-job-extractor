from faster_whisper import WhisperModel
import os
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

reel_dir = "videos"

def transcribe_video(table):
    try:
        for filename in os.listdir(reel_dir):
            transcript = table.find_one({"id": reel_id}, {"transcript": 1}).get("transcript", "")
            if transcript:
                print(f"Transcript already exists for {reel_id}, skipping transcription.")
                continue
            if filename.endswith(".mp4"):
                video_path = os.path.join(reel_dir, filename)
                reel_id = os.path.splitext(filename)[0]

                segments, info = model.transcribe(
                    video_path
                )

                transcript = ""

                for segment in segments:
                    transcript += segment.text + " "

                print(f"Transcript for {reel_id}: {transcript.strip()}")

                table.update_one(
                    {"id": reel_id},
                    {
                        "$set": {
                            "transcript": transcript.strip(),
                        }
                    }
                )

    except Exception as e:
        print(f"Error processing {video_path}: {e}")