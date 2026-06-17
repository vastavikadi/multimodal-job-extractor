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

Analyze the caption, OCR text, and transcript.

Return ONLY valid JSON.

{
  "is_job_posting": false,

  "company": null,
  "role": null,

  "location": null,
  "work_mode": null,

  "salary": null,
  "salary_min": null,
  "salary_max": null,
  "salary_currency": null,

  "experience": null,
  "experience_min_years": null,
  "experience_max_years": null,

  "employment_type": null,

  "skills": [],

  "education": null,

  "apply_link": null,
  "contact_email": null,
  "contact_phone": null,

  "application_deadline": null,

  "source_platform": "instagram",

  "job_description": null,

  "benefits": [],

  "confidence": 0.0
}

Rules:

- is_job_posting must be true only if the content is actually advertising a job, internship, hiring opportunity, walk-in drive, recruitment event, freelance role, contract role, apprenticeship, or campus hiring.
- work_mode must be one of:
  ["remote", "hybrid", "onsite", null]

- employment_type must be one of:
  ["full_time", "part_time", "internship", "contract", "freelance", "temporary", null]

- skills must be a list of unique skills.

- benefits must be a list of perks or benefits.

- confidence must be between 0 and 1.

- If information is missing, use null.

Return JSON only.
"""

DEFAULT_RESPONSE = {
  "is_job_posting": false,

  "company": null,
  "role": null,

  "location": null,
  "work_mode": null,

  "salary": null,
  "salary_min": null,
  "salary_max": null,
  "salary_currency": null,

  "experience": null,
  "experience_min_years": null,
  "experience_max_years": null,

  "employment_type": null,

  "skills": [],

  "education": null,

  "apply_link": null,
  "contact_email": null,
  "contact_phone": null,

  "application_deadline": null,

  "source_platform": "instagram",

  "job_description": null,

  "benefits": [],

  "confidence": 0.0
}

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
    try:
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

        data = json.loads(text)

        # Fill missing keys
        result = DEFAULT_RESPONSE.copy()
        result.update(data)
        return result

    except Exception as e:
        print(f"Gemini extraction failed: {e}")
        return DEFAULT_RESPONSE.copy()