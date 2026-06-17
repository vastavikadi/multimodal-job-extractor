import os
import time
import random
from urllib import response
from playwright.sync_api import sync_playwright
import json
from dotenv import load_dotenv
from sessions.convert_cookies import convert_cookies

load_dotenv()

def visit_account():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) #headless for github actions, if running locally then try headless=False
        if "instagram_state.json" in os.listdir("sessions/"):
            with open("sessions/instagram_state.json", "r") as f:
                instagram_state = json.load(f)
            context = browser.new_context(storage_state=instagram_state)
            page = context.new_page()
        else:
            context = browser.new_context()
            page = context.new_page()
            try:
                response =page.goto("https://www.instagram.com/accounts/login/", wait_until="domcontentloaded")
                print("Status:", response.status if response else "No response")
                print("Current URL:", page.url)
            except Exception as e:
                print("Goto failed:", e)
            finally:
                page.screenshot(path="instagram_debug.png")
                with open("instagram_debug.html", "w", encoding="utf-8") as f:
                    f.write(page.content())
            page.locator('input[name="email"]').fill(os.getenv("INSTA_USERNAME"))
            page.locator('input[name="pass"]').fill(os.getenv("INSTA_PASSWORD"))
            page.locator('[aria-label="Log In"]').click()
            page.wait_for_timeout(5000)  # Wait for 5 seconds to ensure the page has loaded
            context.storage_state(path="sessions/instagram_state.json")
            print("Session saved!")
            try:
                convert_cookies()
            except Exception as e:
                print(f"Error occurred while converting cookies: {e}")

        page.wait_for_timeout(5000)  # Wait for 5 seconds to ensure the page has loaded
        page.goto(f"https://www.instagram.com/{os.getenv('INSTA_FOR_JOBS')}/reels/")
        

        for _ in range(10):
            page.mouse.wheel(0, 5000)
            time.sleep(random.uniform(1, 3))
            page.wait_for_timeout(1500)

        links = page.eval_on_selector_all(
            'a[href*="/reel/"]',
            "els => [...new Set(els.map(e => e.href))]"
        )

        with open("jsons/reels_links.json", "w") as f:
            json.dump(links, f, indent=4)

        print(f"Extracted {len(links)} reel links and saved to reels_links.json")
        browser.close()