from llm import final_job_data
from reel_operations import (
    download_reels,
    visit_account,
    save_reel_info,
)
from process_reel import (
    extract_text_from_frames,
    execute_frame_extraction,
    transcribe_video,
)
from config import connectDB, create_table

def main():
    DB_INSTANCE = connectDB()

    # check for existing tables
    result = DB_INSTANCE.list_table_names()
    print("Existing tables in the database:", result)
    if "reels_id" not in result:
        create_table(DB_INSTANCE)
    
    table = DB_INSTANCE.get_table("reels_id")

    # login to instagram and visit account for jobs-related reels
    visit_account()
    # save reel info to db
    save_reel_info(table)
    # download reels that are not downloaded yet
    download_reels(table)
    # extract frames from downloaded reels
    execute_frame_extraction()
    # perform ocr on frames and save text to db
    extract_text_from_frames(table)
    # transcribe reels and save transcript to db
    transcribe_video(table)
    # extract final job data and save to db
    final_job_data(table)


if __name__ == "__main__":
    main()