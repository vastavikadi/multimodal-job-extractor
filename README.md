# Job Reels Pipeline

A multimodal data ingestion pipeline that converts Instagram job reels into structured job records using OCR, speech recognition, and LLM-powered information extraction.

## Overview

Job Reels Pipeline automates the collection and processing of job postings shared through Instagram Reels.

The system continuously discovers new reels from job-focused Instagram accounts, extracts information from captions, on-screen text, and spoken audio, and converts the content into structured job metadata suitable for search, analytics, and downstream applications.

- NOTE: This project is currently taking only one Instagram account for job reels. If you want it to take multiple accounts, you can modify the code in `reel_operations/visit_account.py` to loop through a list of accounts. Simply, add a list of accounts in the `.env` file and loop through them in the code. Make sure to handle rate limits and session management appropriately. If you are new to Python, you can reach out to me on LinkedIn (https://www.linkedin.com/in/vastavikadi/) for guidance or you can also use LLMs like Claude or ChatGPT to help you with the code modifications.

## Features

### Reel Discovery

* Automated Instagram account crawling using Playwright
* Session-based authentication
* Duplicate detection using reel IDs
* Incremental ingestion of newly published reels

### Metadata Collection

* Reel metadata extraction using yt-dlp
* Caption collection
* Engagement metrics collection
* Persistent storage in Astra DB

### Video Processing

* Automated reel downloading
* Local video storage management
* Frame extraction using OpenCV

### OCR Pipeline

* Text extraction from video frames using EasyOCR
* OCR deduplication and normalization
* Structured storage of extracted text

### Audio Processing

* Speech-to-text transcription using Faster-Whisper
* Transcript generation from reel audio

### LLM Extraction

* Job information extraction using Gemini 2.5 Flash
* Structured JSON generation
* Confidence scoring
* Job-specific entity extraction

### Database Storage

* Astra DB integration
* Reel metadata persistence
* OCR and transcript storage
* Final structured job records

## Architecture

Instagram Reels

↓ Playwright

Reel Discovery

↓ yt-dlp

Metadata Collection

↓ Astra DB

Reel Storage

↓ Video Download

OpenCV Frame Extraction

↓ EasyOCR

OCR Text

↓ Faster Whisper

Audio Transcript

↓ Gemini 2.5 Flash

Job Information Extraction

↓ Astra DB

Structured Job Records

## Extracted Fields

The pipeline extracts:

* Company Name
* Job Role
* Salary / CTC
* Location
* Experience Requirements
* Employment Type
* Skills
* Application Information
* Confidence Score

## Technology Stack

### Data Collection

* Python
* Playwright
* yt-dlp

### Data Storage

* Astra DB (Apache Cassandra)

### Computer Vision

* OpenCV
* EasyOCR

### Speech Recognition

* Faster-Whisper

### AI Processing

* Gemini 2.5 Flash

## Example Output

```json
{
  "company": "Wissen Technology",
  "role": "Associate Engineer",
  "location": "Bangalore, India",
  "salary": "6 - 10 LPA",
  "experience": "Fresher",
  "employment_type": "Full-time",
  "skills": [
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Angular"
  ],
  "confidence": 0.90
}
```

## Future Improvements

* Multi-account ingestion
* Job search API
* Semantic job search using embeddings
* Vector database integration
* Real-time processing queues
* Cloud storage support
* Job recommendation engine

## Setup Instructions
1. Clone the repository: `git clone https://github.com/vastavikadi/multimodal-job-extractor.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Astra DB
4. Configure environment variables in `.env`

```
ASTRA_DB_API_ENDPOINT=""
ASTRA_DB_APPLICATION_TOKEN=""
GEMINI_API_KEY=""
INSTA_USERNAME=""
INSTA_PASSWORD=""
INSTA_FOR_JOBS=""
```

5. Run the pipeline: `python main.py`

- You can use Database as per your choice, just make sure to update the database connection and query code in the respective files.


## Contribution

Contributions are welcome! Please fork the repository and submit a pull request with your improvements. For major changes, please open an issue first to discuss what you would like to change. Make sure to update tests as appropriate. Try to keep the code style consistent with the existing codebase. Main focus should be on meeting the future improvements and adding new features while ensuring the stability of the existing pipeline.

## Disclaimer

This project is intended for educational and research purposes. Users are responsible for complying with Instagram's Terms of Service and applicable laws when collecting or processing content.
