import yt_dlp
# import json

ydl_opts = {
    "cookiefile": "sessions/instagram_cookies.txt",
}

def get_reel_info(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)
    

# def store_reel_info():  
#     with open("reels_links.json", "r") as f:
#         links = json.load(f)
#         for link in links:
#             info = get_reel_info(link)
#             with open("reels_metadata.json", "a") as f:
#                 json.dump(info, f, indent=4)
#                 f.write("\n")  # Add a newline after each entry for better readability


# store_reel_info()
