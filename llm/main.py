import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

SYSTEM_PROMPT = """
You are a job information extraction system.

Extract job-related information from the provided text.

Return ONLY valid JSON.

Schema:

{
  "is_job_posting": true,
  "company": null,
  "role": null,
  "location": null,
  "salary": null,
  "experience": null,
  "employment_type": null,
  "skills": [],
  "apply_link": null,
  "confidence": 0.0
}

If information is missing, use null.
"""

def extract_job_info(
    description,
    ocr_text,
    transcript
):
    combined_text = f"""
CAPTION:
{description}

OCR:
{ocr_text}

TRANSCRIPT:
{transcript}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            SYSTEM_PROMPT,
            combined_text
        ]
    )

    text = response.text.strip()

    # Gemini sometimes wraps JSON
    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    return json.loads(text)